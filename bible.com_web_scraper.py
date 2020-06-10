import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = input("Please enter the url you want to scrape from bible.com: \n")
#print(url)
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")


line_count = 1
for tag in soup.findAll('span'):
    temp = tag['class']
    print(temp)
    time.sleep(1)
