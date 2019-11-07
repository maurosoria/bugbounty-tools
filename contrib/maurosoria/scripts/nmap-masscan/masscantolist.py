#!/usr/bin/env python3
import os
import sys
import xml.etree.ElementTree as ET

def parse_xml(file_path):
    masscan_file = file_path
    tree = ET.parse(masscan_file)

    for host in tree.getroot().iter('host'):
        for address in host.iter('address'):
            ip = address.get('addr')
            for ports in host.iter('ports'):
                for port in ports.iter('port'):
                    port = port.get('portid')
                    print(ip + ':' + port)

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print('Usage of {0}: report.xml'.format(sys.argv[0]))
        exit(1)
    parse_xml(sys.argv[1])

if __name__ == '__main__':
    main()
