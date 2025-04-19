## Resolve domains 
Asynchronous dns resolver written in python (30 threads)

## Python Example:
```python
cat domainlist.txt | python3 resolvedomains.py > ip_addresses
```

## Ruby Example:
```ruby
cat domainlist.txt | ruby resolvedomains.rb > ip_addresses
# useful for bbrf
cat domainlist.txt | ruby resolvedomains.rb -v > ips_hosts 
```

```bash
$ awk '{print $1}' ip_addresses_verbose > resolved_hosts
$ awk '{print $2}' ip_addresses_verbose > ip_addresses
```

## Go Exemple:

### Usage exemple

![Exemple](exemple.gif)

#### Compile the resolvedomains.go file:
```
$ go build -o resolvedomains.exe resolvedomains.go
```

* for Unix/Mac just run `go build -o resolvedomains resolvedomais.go`

```go
$ cat domainlist.txt | go run .\resolvedomains.go
or if you compile:
$ resolvedomains.exe domainlist.txt
```
#### exemple of use

```
$ go run resolvedomains.go domain.txt

DNS RESOLVER - by @maurosoria and @jbz0
=======================================
Loading...
Starting domain resolution...

Results:
[*] Domain: google.com | IPv4: 142.250.79.174
[*] Domain: google.com | IPv4: 2800:3f0:4004:804::200e
```
