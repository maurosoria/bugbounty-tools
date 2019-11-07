#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

import requests

import tldextract
import logging
import re
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
        print("Usage: {0} [DOMAIN]".format(sys.argv[0]))
        exit(1)
    arg = parse_arg()

    checked = []

    search = BingSearch('site:{0}'.format(arg))
    links = search.next_results()
    while links is not None:
        for link in links:
            hostname = extract_domain(link)
            if hostname in checked:
                search = BingSearch("{0} -site:{1}".format(search.query, hostname))
                continue
            else:
                checked.append(hostname)

            print(hostname)
        links = search.next_results()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as ex:
        print("Canceled by the user: ", None, file=sys.stderr)
        exit(1)

