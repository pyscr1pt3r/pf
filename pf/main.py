#!/usr/bin/python3
import os, sys
import argparse
import logging
import time
import colorama
from colorama import Fore, Style
from urllib.parse import urlparse, parse_qs, urlencode
from .core.http import fetch


HARDCODED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".json", ".css", ".js", ".webp", ".woff", ".woff2", ".eot", ".ttf", ".otf", ".mp4", ".txt"]

yellow_color_code = "\033[93m"
reset_color_code = "\033[0m"

colorama.init(autoreset=True)  # Initialize colorama for colored terminal output

logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stderr, datefmt='%Y-%m-%d %H:%M:%S')

p = argparse.ArgumentParser(description="Mining URLs from of Web Archives ")
p.add_argument("-d", "--domain", help="Domain name to fetch related URLs for.")
p.add_argument("-l", "--list", help="File containing a list of domain names.")
p.add_argument('-x', "--proxy", help="Set the proxy address for web requests.")
p.add_argument("-s", "--stream", action="store_true", help="Stream URLs on the terminal.")
p.add_argument("-p", "--placeholder", help="placeholder for parameter values", default="FUZZ")
p.add_argument('-t', '--timeout', default=10, type=int, help='Timeout for avoiding ratelimit of wayback machine')
args = p.parse_args()


def has_extension(url, extensions):
    parsed_url = urlparse(url)
    path = parsed_url.path
    extension = os.path.splitext(path)[1].lower()

    return extension in extensions


def clean_url(url):
    parsed = urlparse(url)

    if (parsed.port == 80 and parsed.scheme == "http") or (parsed.port == 443 and parsed.scheme == "https"):
        parsed = parsed._replace(netloc=parsed.netloc.rsplit(":", 1)[0])

    return parsed.geturl()


def main():
    if not args.domain and not args.list:
        p.error("Please provide either the -d option or the -l option.")

    if args.list:
        with open(args.list, "r") as f:
            domains = [line.strip().lower().replace('https://', '').replace('http://', '') for line in f.readlines()]
            domains = [domain for domain in domains if domain]  # Remove empty lines
            domains = list(set(domains))  # Remove duplicates
    else:
        domains = [args.domain]
    extensions = HARDCODED_EXTENSIONS

    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    for idx, domain in enumerate(domains):
        time.sleep(args.timeout)
        logging.info(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} [{idx}] Fetching URLs for {Fore.CYAN + domain + Style.RESET_ALL}")
        resp = fetch(domain, args.proxy)
        if not resp:
            continue
        urls = resp.text.split()
        logging.info(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} [{idx}] Found {Fore.GREEN}{len(urls)}{Style.RESET_ALL} URLs for {Fore.CYAN + domain + Style.RESET_ALL}")
        if not len(urls):
            continue
        cleaned_urls = set()
        for url in urls:
            cleaned_url = clean_url(url)
            if not has_extension(cleaned_url, extensions):
                parsed_url = urlparse(cleaned_url)
                query_params = parse_qs(parsed_url.query)
                cleaned_params = {key: args.placeholder for key in query_params}
                cleaned_query = urlencode(cleaned_params, doseq=True)
                cleaned_url = parsed_url._replace(query=cleaned_query).geturl()
                cleaned_urls.add(cleaned_url)
        cleaned_urls = list(cleaned_urls)
        logging.info(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} [{idx}] Found {Fore.GREEN}{len(cleaned_urls)}{Style.RESET_ALL} URLs after cleaning")

        if not len(cleaned_urls):
            continue
        result_file = os.path.join(results_dir, f"{domain}.txt")
        with open(result_file, "w") as f:
            for url in cleaned_urls:
                if '?' in url:
                    f.write(f'{url}\n')
                    if args.stream:
                        sys.stdout.write(f'{url}\n')
        logging.info(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} [{idx}] Saved cleaned URLs to {Fore.CYAN + result_file + Style.RESET_ALL}")


if __name__ == '__main__':
    main()
