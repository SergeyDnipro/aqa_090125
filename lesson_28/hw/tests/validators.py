import requests
from urllib.parse import urlparse


def validate_url(url, timeout: int = 5):
    url_parse = urlparse(url)
    url_valid = any([url_parse.scheme in ("http", "https"), url_parse.netloc])

    url_response = requests.head(url, timeout=timeout)
    url_reachable = url_response.status_code < 400

    if not url_valid:
        raise ValueError(f"Invalid URL format: {url}")

    if not url_reachable:
        raise ConnectionError(f"URL is not reachable: {url}")

    return url
