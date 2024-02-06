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

p = argparse.ArgumentParser(description="Replace URL values with keyword")
p.add_argument("-p", "--placeholder", help="placeholder for parameter values", default="FUZZ")
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
    if sys.stdin.isatty():
        sys.exit(0)

    extensions = HARDCODED_EXTENSIONS
    urls = set()
    for line in sys.stdin.readlines():
        url = line.strip('\r').strip('\n')
        if not has_extension(url, extensions):
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            cleaned_params = {key: args.placeholder for key in query_params}
            cleaned_query = urlencode(cleaned_params, doseq=True)
            url = parsed_url._replace(query=cleaned_query).geturl()
            urls.add(url)
    for url in urls:
        sys.stdout.write(f'{url}\n')


if __name__ == '__main__':
    main()
