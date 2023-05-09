# Debian contents index parser

## Summary
CLI tool for parse debian content index file

## How-to-use guide
1. Install python 3 latest stable version. Tested version 3.10.4
2. Install required packages from requirements.txt file. 
```sh
pip install -r requirements.txt
3. Run the cli tool with the following format.

## Usage
```sh
python package-statistics.py -a mips64el
./package-statistics.py -a mips64el

```sh
python package-statistics.py -a mips64el -m <debian mirror link> -t <top n value>

**Note**  
Architecture - amd64, arm64, mips etc: -a amd64
Debian mirror link - http://ftp.uk.debian.org/debian/dists/stable/main/
`






