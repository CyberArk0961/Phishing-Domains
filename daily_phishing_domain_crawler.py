#!/usr/bin/env python3
"""
Daily Phishing Domain Crawler
Source: Phishing.Database (ACTIVE domains)

Runs safely every 24 hours via GitHub Actions / cron
"""

import requests
import csv
import os
from datetime import datetime

FEED_URL = (
    "https://raw.githubusercontent.com/"
    "Phishing-Database/Phishing.Database/"
    "refs/heads/master/phishing-domains-ACTIVE.txt"
)

OUTPUT_DIR = "output"
OUTPUT_FILE = "daily_phishing_domains.csv"

REQUEST_TIMEOUT = 30

os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_domains():
    print("[*] Fetching active phishing domains feed")
    r = requests.get(FEED_URL, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()

    domains = []
    for line in r.text.splitlines():
        domain = line.strip().lower()
        if domain and not domain.startswith("#"):
            domains.append(domain)

    return sorted(set(domains))

def write_csv(domains):
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    today = datetime.utcnow().strftime("%Y-%m-%d")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "domain", "source"])
        for domain in domains:
            writer.writerow([today, domain, "Phishing.Database"])

    print(f"[+] Written {len(domains)} phishing domains to {output_path}")

def main():
    domains = fetch_domains()
    write_csv(domains)

if __name__ == "__main__":
    main()
