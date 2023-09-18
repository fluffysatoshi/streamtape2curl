#!/usr/bin/env python
import re
import requests
import sys

PREFIX='https:/'

def get_curl_command(url: str) -> str:
    html = requests.get(url).content.decode()
    token = re.match(r".*document.getElementById.*\('norobotlink'\).innerHTML =.*?token=(.*?)'.*?;", html, re.M|re.S).group(1)
    infix=re.match(r'.*<div id="ideoooolink" style="display:none;">(.*?token=).*?<[/]div>', html, re.M|re.S).group(1)
    final_URL=f'{PREFIX}{infix}{token}'
    orig_title=re.match(r'.*<meta name="og:title" content="(.*?)">', html, re.M|re.S).group(1)
    return f"curl -L -o '{orig_title}' '{final_URL}'"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} STREAMTAPE_URL...", file=sys.stderr)
        sys.exit(1)
    for url in sys.argv[1:]:
        try:
            command = get_curl_command(url)
            print(command)
        except Exception as e:
            print(e, file=sys.stderr)
