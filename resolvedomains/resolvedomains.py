#!/usr/bin/env python3
import sys
import re
import concurrent.futures
import dns.resolver

class Resolver(object):
    def __init__(self, string):
        self.ip_addresses = []
        if Resolver._is_ip_addr(string):
            self.ip_addresses.append(string)
        else:
            resolved = Resolver._resolve(string)
            if not resolved is None:
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
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.name.EmptyLabel) as e:
            return None

def solve_ip_addresses(s):
    r = Resolver(s)
    return r.ip_addresses

def main():
    lines = list(set(sys.stdin.read().splitlines()))
    resolved = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_addresses = {executor.submit(solve_ip_addresses, line): line for line in lines}
        for f in concurrent.futures.as_completed(future_addresses):
            addresses = f.result()
            for ip_addr in addresses:
                if not ip_addr in resolved:
                    resolved.append(ip_addr)
                    print(ip_addr)
                
if __name__ == '__main__':
    main()
