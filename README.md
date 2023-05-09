# Debian contents index parser

## Summary
CLI tool for parse debian content index file

## How-to-use guide
1. Install python 3 latest stable version. Tested version 3.10.4
2. Install required packages from requirements.txt file. 
```bash
pip install -r requirements.txt
```
3. Run the cli tool with the following format.

## Usage
```bash
python package-statistics.py -a mips64el
```
```bash
./package-statistics.py -a mips64el
```

```
python package-statistics.py -a mips64el -m <debian mirror link> -t <top n value>
```
>**Note**
- -a amd64: Architecture - amd64, arm64, mips etc.
- -m debian_mirror_link: Debian mirror link - http://ftp.uk.debian.org/debian/dists/stable/main/ etc.
- -t top_n_value: Value to find top n packages.






