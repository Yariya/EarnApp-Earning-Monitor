from urllib import parse
from requests import get
from urllib.parse import urljoin

def report_banned_ip(ipaddresses:list):
    try:
        SERVER = "https://ipban.ffehost.com/"
        SLUG = "ban/"
        url = urljoin(urljoin(SERVER, SLUG), ",".join(ipaddresses))
        get(url)
    except:
        parse