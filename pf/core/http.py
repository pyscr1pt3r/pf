import sys
import requests


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]


def fetch(domain, proxy=None):
    wayback_uri = f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=txt&collapse=urlkey&fl=original&page=/"
    proxies = {'http': proxy, 'https': proxy}
    headers = {'User-Agent': user_agents[0]}
    try:
        r = requests.get(wayback_uri, proxies=proxies, headers=headers)
        return r
    except (requests.exceptions.RequestException, ValueError) as e:
        sys.stderr.write(f'[ERR] {domain}: {e}\n')
    except KeyboardInterrupt:
        sys.stderr.write(f'KeyboardInterrupt\n')
        sys.exit(0)