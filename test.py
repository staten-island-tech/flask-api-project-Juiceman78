from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

query = "Mario"  # Replace with your search term
request = Request(f'http://smashdb.me/api/search?query={query}')

try:
    response_body = urlopen(request).read().decode('utf-8')
    print(response_body)
except HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
except URLError as e:
    print(f"URL Error: {e.reason}")