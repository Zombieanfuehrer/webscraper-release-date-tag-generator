import re
from http.client import responses

from bs4 import BeautifulSoup
import requests

class WebScrapper:
    def __init__(self, url):
        self.url = url

    def scrap_string(self, regex):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            match = re.search(regex, text)
            if match:
                return match.group()
            else:
                raise Exception(f"Failed to find the pattern: {regex}")
        else:
            raise Exception(
                f"Failed to retrieve the website. Status code: {response.status_code}"
            )