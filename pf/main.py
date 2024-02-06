#!/usr/bin/python3
import os
import sys
import argparse
from urllib.parse import urlparse, parse_qs, urlencode


extensions = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".json", ".css", ".js", ".webp", ".woff", ".woff2", ".eot", ".ttf", ".otf", ".mp4", ".txt"]
j_params = ['utm_campaign']

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
    parsed = urlparse(url)

    if (parsed.port == 80 and parsed.scheme == "http") or (parsed.port == 443 and parsed.scheme == "https"):
        parsed = parsed._replace(netloc=parsed.netloc.rsplit(":", 1)[0])

    return parsed.geturl()


def remove_junk_params(url):

    ...


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
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        cleaned_params = {key: args.placeholder for key in query_params}
        cleaned_query = urlencode(cleaned_params, doseq=True)
        url = parsed._replace(query=cleaned_query).geturl()
        urls.add(url)

    for url in urls:
        sys.stdout.write(f'{url}\n')


if __name__ == '__main__':
    main()
