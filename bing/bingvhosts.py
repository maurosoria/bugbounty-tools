#!/usr/bin/env python3
import dns.resolver
import tldextract
import requests
import logging
import re
import sys
import urllib.parse as urlparse

requests.packages.urllib3.disable_warnings()

class BingSearch(object):
    url = 'http://www.bing.com/search?first={1}&go=&qs=n&FORM=PORE&q={0}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }

    def __init__(self, query):
        self.query = query
        self.index = 0
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def next_results(self):
        request_url = self.url.format(urlparse.quote(self.query), 1 + int(self.index) * 50)
        body = self.session.get(request_url).content
        result = self._parse_links(body)
        self.index += 1
        if len(result) == 0:
            result = None
        return result

    def _parse_links(self, html):
        if html is None:
            return None
        li_regexp = r'''<li class="b_algo">(.*?)</li>'''
        href_regexp = r'''href="(.*?)"'''
        result = []
        li_collection = re.findall(li_regexp, html.decode(), re.DOTALL)
        for li in li_collection:
            for href in re.findall(href_regexp, li, re.DOTALL):
                result.append(href)
        return result


class Resolver(object):
   def __init__(self, string):
       self.ip_addresses = []
       if Resolver._is_ip_addr(string):
           self.ip_addresses.append(string)
       else:
           resolved = Resolver._resolve(string)
           if resolved is None:
               raise Exception("Couldn't resolve domain name %s" % string)
           self.ip_addresses += resolved

   def is_domain_here(self, domain):
       ip_addresses = Resolver._resolve(domain)
       if ip_addresses is None: return False
       for ip_addr in ip_addresses:
           if ip_addr in self.ip_addresses:
               return True
       return False

   @staticmethod
   def _is_ip_addr(string):
       return re.match('''^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$''', string) is not None

   @staticmethod
   def _resolve(domain):
       try:
           return [str(ip_addr) for ip_addr in dns.resolver.query(domain, 'A')]
       except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer,dns.resolver.NoNameservers) as e:
           return None


def extract_domain(url):
   logging.getLogger("tldextract").setLevel(logging.CRITICAL)
   return '.'.join(part for part in tldextract.extract(url) if part)


def parse_arg():
   arg = sys.argv[1]
   if arg.startswith('http://') or arg.startswith('https://'):
       arg = urlparse.urlparse(arg).netloc
   elif arg.endswith('/'):
       arg = urlparse.urlparse('http://' + arg).netloc
   return arg


def main():
   if len(sys.argv) < 2:
       exit("Usage: %s [IP|DOMAIN]" % (sys.argv[0]))
   arg = parse_arg()
   resolver = Resolver(arg)
   checked = []
   for ip in resolver.ip_addresses:
       search = BingSearch('ip:%s' % ip)
       links = search.next_results()
       while links is not None:
           for link in links:
               hostname = extract_domain(link)
               if hostname in checked:
                   search = BingSearch("{0} -site:{1}".format(search.query, hostname))
                   continue
               else:
                   checked.append(hostname)
               if resolver.is_domain_here(hostname):
                   print(hostname)
           links = search.next_results()


if __name__ == '__main__':
   try:
       main()
   except (KeyboardInterrupt, SystemExit) as e:
       print("Canceled by the user: ", None, file=sys.stderr)
       exit()
