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
* for Unix/Mac: go build -o crtsh crtsh.go

### exemple
```
$ go run crtsh.go -u uol.com

CRTSH ----------- by @maurosoria and @jbz0
==========================================
geo-qa.batepapo.uol.com.br
ingress-akamai.service.uol.com.br
tagservice.uol.com.br
ads.uol.com
email.folha.uol.com.br
rss.musica.uol.com.br
app.uol.com
saas-poc.uol.com
auth.aws.production.sa-east-1a.service.uol.com.br
geo.batepapo.uol.com.br
geoip.canais.uol.com.br
jogos.uol.com.br
noticias.uol.com.br
blogmiltonneves.bol.uol.com.br
rss.diversao.uol.com.br
pr.tt.uol.com.br
eleicoes.uol.com.br
cadastro.uol.com.br
economia.uol.com.br
(.......)
```

## TODO
* Async/Multithread
* Recursive
* uniq output
* --debug
