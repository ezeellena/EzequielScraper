import requests
from bs4 import BeautifulSoup
import json
import pickle
import urllib
import re
url = "http://www.eltreboldigital.com.ar/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
response = requests.get(url, headers=headers).text


parser = BeautifulSoup(response, "html.parser").find_all("div", {"class": 'td-block-span4'})

itemps = parser.a["href"]

eze = 1+1