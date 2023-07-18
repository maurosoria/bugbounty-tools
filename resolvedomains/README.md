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