//  DNS Resolver - a script to resolve domain names to IP addresses, but in golang
//
//  Usage: .\resolvedomains.exe domainlist.txt
//  If you don't compile you can also use:
//	Usage: cat domainlist.txt | go run .\resolvedomains.go > <exemple.txt>
//
//  just ipv6  ./resolvedomains -ipv6-only=true domainlist.txt
//  just ipv4  ./resolvedomains -ipv6-only=false domainlist.txt
//
//  I made the code but automated it with chat gpt

package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"strings"
	"sync"
	"time"
)

var (
	ipv6Only bool
)

func init() {
	// Adds the parameter to choose between IPv6 or IPv4
	flag.BoolVar(&ipv6Only, "ipv6-only", false, "Resolve only IPv6 addresses")
}

func resolveDomain(domain string) ([]string, error) {
	var ips []string
	var err error

	if ipv6Only {
		ips, err = resolveIPv6(domain)
	} else {
		ips, err = resolveIPs(domain)
	}

	return ips, err
}

func resolveIPs(domain string) ([]string, error) {
	var ips []string
	addrs, err := net.LookupHost(domain)
	if err != nil {
		return nil, err
	}

	for _, addr := range addrs {
		ips = append(ips, fmt.Sprintf("IPv4: %s", addr))
	}

	return ips, nil
}

func resolveIPv6(domain string) ([]string, error) {
	var ips []string
	addrs, err := net.LookupIP(domain)
	if err != nil {
		return nil, err
	}

	for _, addr := range addrs {
		if strings.Contains(addr.String(), ":") { // IPv6 check
			ips = append(ips, fmt.Sprintf("IPv6: %s", addr.String()))
		}
	}

	return ips, nil
}

func displayLoading() {
	for i := 0; i < 3; i++ {
		fmt.Print(".")
		time.Sleep(1 * time.Second)
	}
}

func main() {
	// Print logo
	fmt.Println("\nDNS RESOLVER - by @maurosoria and @yhk0")
	fmt.Println("=========================================")

	// Load parameters and start the flag
	flag.Parse()

	// Verify that the file has been passed
	if len(flag.Args()) < 1 {
		log.Fatal("Please provide the filename containing the domains to resolve.")
	}

	fileName := flag.Args()[0]
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		log.Fatal(err)
	}

	// Prepare the list of domains
	domains := strings.Split(string(data), "\n")
	domains = removeEmptyLines(domains)

	// Loading Screen
	fmt.Print("Loading")
	displayLoading()
	fmt.Print("\nStarting domain resolution")
	displayLoading()

	// Divide the domains that found IPs and those that didn't
	var foundIPs, notFound []string
	var mu sync.Mutex
	var wg sync.WaitGroup

	// Resolve domains
	for _, domain := range domains {
		wg.Add(1)
		go func(domain string) {
			defer wg.Done()
			ips, err := resolveDomain(domain)
			mu.Lock()
			defer mu.Unlock()

			if err == nil && len(ips) > 0 {
				for _, ip := range ips {
					foundIPs = append(foundIPs, fmt.Sprintf("[*] Domain: %s | %s", domain, ip))
				}
			} else {
				notFound = append(notFound, fmt.Sprintf("[!] Domain: %s\n L> No IP addresses found.", domain))
			}
		}(domain)
	}

	// Wait for all goroutines to finish
	wg.Wait()

	// View results found first
	fmt.Print("\n\nResults:\n")
	for _, result := range foundIPs {
		fmt.Println(result)
	}
	for _, result := range notFound {
		fmt.Println(result)
	}
}

// Remove empty rows
func removeEmptyLines(input []string) []string {
	var output []string
	for _, line := range input {
		if line != "" {
			output = append(output, line)
		}
	}
	return output
}
