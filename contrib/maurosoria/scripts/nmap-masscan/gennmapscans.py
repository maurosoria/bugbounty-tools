#!/usr/bin/env python3
import sys
import os
import time

NMAP_CMD = "nmap -p{0} -iL gscan_{0}.list -Pn -sV -sT -sC -vvv -oN gscan_{0}_report.nmap -oX gscan_{0}_report.xml"

def get_port_dict(ip_ports):
    nmap_lines_by_port = {}
    for ip_port in ip_ports:
        _tmp = ip_port.split(':')
        ip = _tmp[0]
        port = int(_tmp[1])
        if nmap_lines_by_port.get(port) is None:
            nmap_lines_by_port[port] = []
        nmap_lines_by_port[port].append(ip)
    return nmap_lines_by_port

def main():
    if len(sys.argv) < 3:
        print('Usage of {0}: ip_port.txt name'.format(sys.argv[0]))
        exit(1)

    if not os.path.exists(sys.argv[1]):
        print('Input file not found')
        exit(1)
    scan_name = sys.argv[2]

    dest_dir = "GNMAPSCAN_{0}_{1}".format(scan_name,time.strftime('%y-%m-%d_%H-%M-%S'))

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    port_dict = get_port_dict(open(sys.argv[1]).read().splitlines())
    bash_file = open(os.path.join(dest_dir, 'runme.sh'), 'w')
    for port, hosts in port_dict.items():
        list_file = open(os.path.join(dest_dir, 'gscan_{0}.list'.format(port)), 'w')
        for host in hosts:
            list_file.write(host + "\n")
        list_file.close()
        bash_file.write(NMAP_CMD.format(port) + "\n")
    bash_file.close()


if __name__ == '__main__':
    main()
