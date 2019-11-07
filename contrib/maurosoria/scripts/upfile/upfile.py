#!/usr/bin/env python3
import pkg_resources
import requests
import os.path
from urllib.parse import urlparse,parse_qs
from optparse import OptionParser, OptionGroup
import sys
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'


class Upfile(object):

    def __init__(self, url, file_path, name, file_name=None, mime_type=None, cookie=None, data='', headers=None,
                 proxy=None, timeout=None, allow_redirects=False, user_agent=USER_AGENT):
        self.url = url
        self.file = open(file_path, 'rb')
        self.name = name
        self.file_name = (file_name if file_name is not None else os.path.basename(file_path))
        self.mime_type = mime_type
        self.cookie = cookie
        self.data = parse_qs(data) if data is not None else None
        self.proxy = proxy
        self.timeout = timeout
        self.allow_redirects = allow_redirects
        self.user_agent = user_agent
        if headers is not None:
            try:
                self.headers = dict((key.strip(), value.strip()) for (key, value) in (header.split(':', 1)
                                    for header in headers))
            except (Exception) as e:
                raise Exception('Invalid headers')
        else:
            self.headers = {}

    def upload(self):
        files = {self.name: (self.file_name, self.file, self.mime_type, {})}
        session = requests.Session()
        session.headers.update({'User-agent': self.user_agent})
        if self.cookie is not None:
            session.headers.update({'Cookie': self.cookie.strip()})
        for key, value in self.headers.items():
            session.headers.update({key: value})
        proxies = ({'http': self.proxy, 'https': self.proxy} if self.proxy is not None else None)
        response = session.post(self.url, files=files, data=self.data, timeout=self.timeout, proxies=proxies, allow_redirects=self.allow_redirects,verify=False)
        result = {}
        result['status'] = response.status_code
        result['headers'] = '\n'.join(['%s: %s' % (key, value) for (key, value) in response.headers.items()])
        result['body'] = response.content
        return result


def parse_arguments():
    usage = 'Usage: %prog [-u|--url] target [-f|--file] file [-n|--name] name [options]'
    parser = OptionParser(usage)
    mandatory = OptionGroup(parser, 'Mandatory')
    mandatory.add_option('-u', '--url', help='URL target', action='store', type='string', dest='url', default=None)
    mandatory.add_option('-f', '--file', help='File to upload', action='store', type='string', dest='file_path',
                         default=None)
    mandatory.add_option('-n', '--name', help='Parameter name', action='store', type='string', dest='name',
                         default=None)
    settings = OptionGroup(parser, 'Optional Settings')
    settings.add_option('--file-name', '--file-name', help='Upload with this file_name', action='store', type='string',
                        dest='file_name', default=None)
    settings.add_option('-m', '--mime-type', help='Mime-type', action='store', type='string', dest='mime_type',
                        default=None)
    settings.add_option('-c', '--cookie', help='Cookie', action='store', type='string', dest='cookie', default=None)
    settings.add_option('-a', '--user-agent', help='User agent', action='store', dest='user_agent', default=USER_AGENT)
    settings.add_option('-r', '--allow-redirects', help='Allow redirects', action='store_true', dest='allow_redirects',
                        default=False)
    settings.add_option('-d', '--data', help='POST data (example: a=v1&b=v2)', action='store', type='string',
                        dest='data', default=None)
    settings.add_option('--header', '--header',
                        help='Headers to add (example: --header "Referer: example.com" --header "User-Agent: IE"',
                        action='append', type='string', dest='headers', default=None)
    settings.add_option('-p', '--proxy-http', help='HTTP proxy (example: http://localhost:8080', action='store',
                        type='string', dest='proxy', default=None)
    settings.add_option('-t', '--timeout', help='Connection Timeout (default 250)', action='store', type='string',
                        dest='timeout', default=250)
    parser.add_option_group(mandatory)
    parser.add_option_group(settings)
    options, arguments = parser.parse_args()
    if options.url is None or options.file_path is None or options.name is None:
        raise Exception('Mandatory argument(s) missing!')
    return options


def checkRequestsVersion():
    try:
        version = pkg_resources.require('requests')[0].version.split('.')
    except pkg_resources.DistributionNotFound:
        return False
    return not (int(version[0]) < 2 and int(version[1]) < 3)


if __name__ == '__main__':
    try:
        if not checkRequestsVersion():
            print ('This program needs at least requests 2.3.0')
            print ('http://docs.python-requests.org/en/latest/user/install/')
            exit()
        options = parse_arguments()
        upfile = Upfile(options.url, options.file_path, options.name, file_name=options.file_name,
                        mime_type=options.mime_type, cookie=options.cookie, data=options.data, headers=options.headers,
                        proxy=options.proxy, timeout=options.timeout, allow_redirects=options.allow_redirects,
                        user_agent=options.user_agent)
        result = upfile.upload()
        print ('Status ', result['status'])
        print (result['headers'])
        print ()
        print (result['body'].decode())
    except (Exception) as e:
        print (str(e))


