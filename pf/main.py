#!/usr/bin/python3
import os
import re
import sys
import html
import argparse
from urllib.parse import urlparse, parse_qs, urlencode, unquote


extensions = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".json", ".css", ".js", ".webp", ".woff", ".woff2", ".eot", ".ttf", ".otf", ".mp4", ".txt"]
j_params = ['utm_campaign', 'utm_source', 'utm_medium', 'utm_content', 'utm_term']

p = argparse.ArgumentParser(description="Replace URL values with keyword")
p.add_argument("-p", "--placeholder", help="placeholder for parameter values", default="FUZZ")
args = p.parse_args()


def has_extension(url, extensions):
    parsed = urlparse(url)
    path = parsed.path
    extension = os.path.splitext(path)[1].lower()

    return extension in extensions


def has_params(url):
    return '?' in url


def clean_url(url):
    # decode
    html.unescape(unquote(url))

    parsed = urlparse(url)

    # handle port
    if (parsed.port == 80 and parsed.scheme == "http") or (parsed.port == 443 and parsed.scheme == "https"):
        parsed = parsed._replace(netloc=parsed.netloc.rsplit(":", 1)[0])

    return parsed.geturl()


def clean_params(url):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    cleaned_params = {}
    for k in query_params.keys():
        if not re.match(r'^[0-9a-zA-Z_\[\]-]+$', k):
            continue
        if k in j_params:
            continue
        cleaned_params[k] = args.placeholder
    cleaned_query = urlencode(cleaned_params, doseq=True)
    # cleaned_query = '&'.join([f'{k}={v}' for k, v in cleaned_params.items()])
    url = parsed._replace(query=cleaned_query).geturl()

    return url if has_params(url) else None


def main():
    if sys.stdin.isatty():
        sys.exit(0)

    urls = set()
    for line in sys.stdin.readlines():
        url = line.strip('\r').strip('\n')
        if not has_params(url):
            continue
        if has_extension(url, extensions):
            continue
        url = clean_url(url)
        url = clean_params(url)
        if not url:
            continue
        urls.add(url)

    for url in urls:
        sys.stdout.write(f'{url}\n')


if __name__ == '__main__':
    main()
