#!/usr/bin/env python3
import requests
import urllib.parse
import sys
from orderedset import OrderedSet

class Crtsh:
    def __init__(self):
        self.base_url = 'https://crt.sh/?output=json&q={}'
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
        self.headers = {'User-Agent' : self.user_agent}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_domains(self, domain):
        result = OrderedSet()

        req = self.session.get(self.base_url.format(domain), headers=self.headers)

        for entry in req.json():
            name_value = entry['name_value'].strip().lower()

            result.add(name_value)

        return list(result)

def parse_uri(arg):
    if arg.startswith('http://') or arg.startswith('https://'):
        arg = urlparse.urlparse(arg).netloc
    elif arg.endswith('/'):
        arg = urlparse.urlparse('http://' + arg).netloc.split(':')[0]

    return arg.strip()

def print_domains(domain_list):
    for domain in domain_list:
        print(domain)

def check_stdin():
    return not sys.stdin.isatty()

def parse_arguments():
    from optparse import OptionParser, OptionGroup

    usage = 'Usage: %prog [-u|--url] target [-i|--input-file] input_file [-o|--output-file] dest_file [-s|--silent]'

    parser = OptionParser(usage)

    arguments = OptionGroup(parser, 'Arguments')
    arguments.add_option('-u', '--url', help='URL target', action='store', type='string', dest='url', default=None)
    arguments.add_option('-f', '--input_file', help='Input File (accept multiple values)', action='append', type='string', dest='input_file_list', default=None)
    arguments.add_option('-o', '--output-file', help='Output File', action='store', type='string', dest='output_file', default=None)
    arguments.add_option('-s', '--silent', help='No printing', action='store_true')
    parser.add_option_group(arguments)
    options, arguments = parser.parse_args()

    input_methods = [not options.url is None, not options.input_file_list is None, check_stdin()]

    if not any(input_methods):
        print("No input provided. Use -u or -f or stdin.")
        sys.exit(1)
    elif sum(input_methods) > 1:
        print("Use only one input.")
        sys.exit(1)

    return options

def clean_domain(arg):
    return arg.strip().lower()

def main():
    import os
    import logging

    #logging.basicConfig(level=logging.DEBUG)
    requests.packages.urllib3.disable_warnings()

    domain_list = OrderedSet()

    options = parse_arguments()

    output_fd = None

    if not options.output_file is None:
        try:
            output_fd = open(options.output_file, 'w')
        except Exception as e:
            print('Cannot open output file \"{0}\"'.format(options.output_file))
            print(str(e))
            exit(1)


    if not options.url is None:
        domain_list.add(clean_domain(options.url))

    elif not options.input_file_list is None:
        for input_file in options.input_file_list:
            if not os.path.exists(input_file):
                print("Input file \"{0}\" does not exist".format(input_file))
                exit(1)
            if not os.path.isfile(input_file):
                print("Input file \"{0}\" is not a valid file".format(input_file))
                exit(1)
            if not os.access(input_file, os.R_OK):
                print("Input file \"{0}\" is not readable".format(input_file))
                exit(1)

        for input_file in options.input_file_list:
            with open(input_file, 'r', errors="replace") as infile:
                for line in infile:
                    line = clean_domain(line)
                    domain_list.add(line)
        domain_list = list(domain_list)
    elif check_stdin():
        lines = sys.stdin.readlines()
        for line in [clean_domain(l) for l in lines]:
            domain_list.add(line)
        domain_list = list(domain_list)



    crtsh = Crtsh()



    for domain in domain_list:
        domain = parse_uri(domain)

        if domain.startswith('www.'):
            domain = domain[4:]

        if domain.startswith('*.'):
            domain = domain[2:]

        result = crtsh.get_domains(domain)

        # If it is a *.www.domain, process both cases
        if domain.startswith('www.'):
            result = crtsh.get_domains(domain[4:])

        if not options.silent:
            print_domains(result)
        result += result

        if not output_fd is None:
            output_fd.writelines(result)
    output_fd.close()

if __name__ == '__main__':

    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        sys.stdout.flush()
        exit(1)
    except Exception as e:
        print(str(e))
        exit(1)
