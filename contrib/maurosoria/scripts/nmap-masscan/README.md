# This scripts are helpful for running and parsing nmap/masscan reports

* domainsfromnmapxml.py: get a list of domains from a nmap xml report (from ssl-certs).
* masscantolist.py: get a list (IP:PORT) of open ports from a masscan/nmap xml file 
* gennmapscans.py: create a folder with a list of files (one for each port) and a runme.sh file for running the nmap scans. Masscan is faster for detecting open ports but nmap is better for recon. So: run masscan and generate a xml report, get the ip_port list with masscantolist.py and run this tool to generate the folder.
