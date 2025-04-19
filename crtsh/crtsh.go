package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

type Crtsh struct {
	BaseURL   string
	UserAgent string
	Client    *http.Client
}

func NewCrtsh() *Crtsh {
	return &Crtsh{
		BaseURL:   "https://crt.sh/?q=%%.%s&output=json",
		UserAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
		Client:    &http.Client{},
	}
}

func PrintBanner(show bool) {
	if !show {
		return
	}
	fmt.Fprintf(os.Stderr, "\nCRTSH ----------- by @maurosoria and @jbz0\n")
	fmt.Fprintf(os.Stderr, "==========================================\n")
}

func (c *Crtsh) GetDomains(domain string) ([]string, error) {
	url := fmt.Sprintf(c.BaseURL, domain)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("error creating request: %w", err)
	}
	req.Header.Set("User-Agent", c.UserAgent)
	req.Header.Set("Accept", "application/json")

	resp, err := c.Client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("error making request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := ioutil.ReadAll(resp.Body)
		return nil, fmt.Errorf("unexpected status code: %d, response: %s", resp.StatusCode, string(body))
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("error reading response body: %w", err)
	}

	var entries []struct {
		NameValue string `json:"name_value"`
	}

	if err := json.Unmarshal(body, &entries); err != nil {
		return nil, fmt.Errorf("error parsing JSON: %w", err)
	}

	domains := make(map[string]struct{})
	for _, entry := range entries {
		for _, d := range strings.Split(entry.NameValue, "\n") {
			cleaned := strings.TrimSpace(d)
			if cleaned != "" {
				domains[cleaned] = struct{}{}
			}
		}
	}

	uniqueDomains := make([]string, 0, len(domains))
	for domain := range domains {
		uniqueDomains = append(uniqueDomains, domain)
	}

	return uniqueDomains, nil
}

func isStdinEmpty() bool {
	stat, _ := os.Stdin.Stat()
	return (stat.Mode() & os.ModeCharDevice) != 0
}

func cleanDomain(domain string) string {
	return strings.TrimSpace(strings.ToLower(domain))
}

func parseURI(arg string) string {
	if strings.HasPrefix(arg, "http://") || strings.HasPrefix(arg, "https://") {
		arg = strings.Split(arg, "//")[1]
	}
	if strings.Contains(arg, "/") {
		arg = strings.Split(arg, "/")[0]
	}
	return strings.TrimSpace(arg)
}

func readDomainsFromFile(filename string) ([]string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var domains []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		domain := cleanDomain(scanner.Text())
		if domain != "" {
			domains = append(domains, domain)
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return domains, nil
}

func readDomainsFromStdin() ([]string, error) {
	scanner := bufio.NewScanner(os.Stdin)
	var domains []string
	for scanner.Scan() {
		domain := cleanDomain(scanner.Text())
		if domain != "" {
			domains = append(domains, domain)
		}
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}
	return domains, nil
}

func writeDomainsToFile(filename string, domains []string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	for _, domain := range domains {
		_, err := file.WriteString(domain + "\n")
		if err != nil {
			return err
		}
	}

	return nil
}

func printDomains(domains []string) {
	for _, domain := range domains {
		fmt.Println(domain)
	}
}

func main() {
	var (
		url        string
		inputFile  string
		outputFile string
		silent     bool
		noHeader   bool
		help       bool
	)

	flag.StringVar(&url, "u", "", "Target URL (e.g., 'example.com')")
	flag.StringVar(&inputFile, "f", "", "Input file with domains (one per line)")
	flag.StringVar(&outputFile, "o", "", "Output file to save results")
	flag.BoolVar(&silent, "s", false, "Silent mode (no output to stdout)")
	flag.BoolVar(&noHeader, "no-header", false, "Disable banner")
	flag.BoolVar(&help, "h", false, "Show help")
	flag.Parse()

	if help {
		flag.Usage()
		os.Exit(0)
	}

	log.SetFlags(0)
	log.SetOutput(os.Stderr)
	PrintBanner(!noHeader)

	inputMethods := 0
	if url != "" {
		inputMethods++
	}
	if inputFile != "" {
		inputMethods++
	}
	if !isStdinEmpty() {
		inputMethods++
	}

	if inputMethods == 0 || inputMethods > 1 {
		log.Println("Error: Provide exactly one input method (-u, -f, or stdin)")
		flag.Usage()
		os.Exit(1)
	}

	var domains []string
	var err error

	if url != "" {
		domains = append(domains, cleanDomain(url))
	} else if inputFile != "" {
		domains, err = readDomainsFromFile(inputFile)
		if err != nil {
			log.Fatalf("Error reading input file: %v", err)
		}
	} else if !isStdinEmpty() {
		domains, err = readDomainsFromStdin()
		if err != nil {
			log.Fatalf("Error reading from stdin: %v", err)
		}
	}

	crtsh := NewCrtsh()
	allResults := make([]string, 0)

	for _, domain := range domains {
		domain = parseURI(domain)
		results, err := crtsh.GetDomains(domain)
		if err != nil {
			log.Printf("Error fetching domains for %s: %v", domain, err)
			continue
		}
		allResults = append(allResults, results...)
	}

	if !silent {
		printDomains(allResults)
	}

	if outputFile != "" {
		err = writeDomainsToFile(outputFile, allResults)
		if err != nil {
			log.Fatalf("Error writing to output file: %v", err)
		}
	}
}