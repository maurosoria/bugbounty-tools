#!/usr/bin/env python3
import sys
import os
import xml.etree.ElementTree as ET

def parse_xml(file_path):
    nmapscan_file = file_path
    tree = ET.parse(nmapscan_file)

    result = set()

    for host in tree.getroot().iter('host'):
        obj = {'hostnames' : [], 'ssl-certs':[]}
        for address in host.iter('address'):
            ip = address.get('addr')
        for hostname in host.iter('hostnames'):
            obj['hostnames'].append(hostname)
        for port in host.find('ports'):
            for ssl_cert in port.findall('.//script[@id="ssl-cert"]'):
                for table in ssl_cert.findall('.//table[@key="subject"]'):
                    for elem in table.findall('.//elem[@key="commonName"]'):
                        result.add(elem.text)
            for table in port.findall('.//table[@key="extensions"]'):
                for child_table in table.findall('.//table'):
                    if "Subject Alternative Name" in child_table.find('.//elem[@key="name"]').text:
                        alternative_domains = (child_table.find('.//elem[@key="value"]').text)
                        for tmp in [tmp.strip() for tmp in alternative_domains.split(',')]:
                            if tmp.startswith('DNS:'):
                                result.add(tmp[4:])
    return result



def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print('Usage of {0}: report.xml'.format(sys.argv[0]))
        exit(1)
    result = parse_xml(sys.argv[1])
    for dom in sorted(list(result)):
        print(dom)

if __name__ == '__main__':
    main()
