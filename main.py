#!/usr/bin/python
import argparse
import sys
import re
#formatting + colors
from rich.console import Console
from rich.table import Column, Table

# Argument Handling
parser = argparse.ArgumentParser(description="View top # of IPs in a log file")
parser.add_argument("--filename", type=str, help="Source log filename to scan for ips.")
parser.add_argument("--top", default=1, type=int, help="Top # of IPs to display")
args = parser.parse_args()

# Argument Error Checking
if args.filename is None:
    print("Please specify a filename. usage: main.py [-h] [--filename FILENAME] [--top TOP]")
    sys.exit(1)
elif args.top <= 1:
    print("Please specify a positive top #.")
    sys.exit(1)

# Setup Dictionary to track IPS
ipDict = {}

# IP Valication and Tracking

def ipValidation(ip: str) -> bool:
    # IP Pattern Validation (v4 or v6 or None)
    if load_ipv4.match(ip) or load_ipv6.match(ip):
        return True
    else:
        # comment out to identify bad ip strings
        # print(f'{ip} is not a valid IP') 
        return False

def upsertIPDict(ip: str) -> None:
    """ Checks IP against previous history. """
    # Upsert into IP Dict
    if ipValidation(ip):
        if ipDict.get(ip):
            ipDict[ip] += 1
        else:
            ipDict[ip] = 1
        return None
    else:
        return None

def calculate() -> None:
    """ Prints Top Results """
    line_num = 1
    console = Console()
    print("\n")
    table = Table(
        show_header=True,
        header_style="bold magenta",
        show_edge=True,
        title=f"TOP IPs")
    table.add_column("RANK", width=4, justify="center")
    table.add_column("IP", justify="center")
    table.add_column("COUNT", justify="center", style="green")

    # iterate through a sorted dictionary of IPs and build results table
    for _ip in sorted(ipDict, key=ipDict.get, reverse=True)[0:args.top]:
        table.add_row(
            str(line_num),
            str(_ip),
            str(ipDict.get(_ip))
        )
        line_num = line_num + 1

    console.print(table)


""" RegEx Match Patterns."""
ipv4 = "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
ipv6 = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
""" Precompile for more efficient reuse."""
load_ipv4 = re.compile(ipv4)
load_ipv6 = re.compile(ipv6)


# Main Function
if __name__ == "__main__":

    # File Handling
    rows = ( row.split(" ") for row in open(args.filename, "r", encoding="UTF-8") )
    
    for row in rows:
        sourceIP = row[0]
        upsertIPDict(sourceIP)

    calculate()
