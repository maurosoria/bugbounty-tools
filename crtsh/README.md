# A tool for getting domains from crtsh
I coded this tool tonight so I haven't tested well yet. Please create an issue if you find a bug

## Usage:
* python3 crtsh.py -u domain.com
* python3 crtsh.py -f domain_list.txt
* cat domain_list.txt | python3 crtsh.py

## Usage in Golang:
* go run crtsh.go -u domain.com
* go run crtsh.go -f domain_list.txt
* cat domain_list.txt | go run crtsh.go
* go build -o crtsh.exe crtsh.go

## TODO
* Async/Multithread
* Recursive
* uniq output
* --debug
