import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import os

for i in range(1,2525):
    url = "https://www.bible.com/bible/" + str(i)

    response = requests.get(url)

    lang_code = re.search(".[a-zA-Z0-9]*$", response.url)

    print(response.status_code)
    print(response.url)
    print(lang_code.group()[1:])
    print(response)
    #print(response.text)
    #book_table_of_contents_dic = {"GEN" : 1, "EXO" : 2, "LEV" : 3, "NUM" : 4, "DEU" : 5, "JOS" : 6, "JDG" : 7, "RUT" : 8, "1SA" : 9, "2SA" : 10, "1KI" : 11, "2KI" : 12, "1CG" : 13, "2CH" : 14, "EZR" : 15, "NEH" : 16, "EST" : 17, "JOB" : 18, "PSA" : 19, "PRO" : 20, "ECC" : 21, "SNG" : 22, "ISA" : 23, "JER" : 24, "LAM" : 25, "EZK" : 26, "DAN" : 27, "HOS" : 28, "JOL" : 29, "AMO" : 30, "OBA" : 31, "JON" : 32, "MIC" : 33, "NAH" : 34, "HAB" : 35, "ZEP" : 36, "HAG" : 37, "ZEC" : 38, "MAL" : 39, "MAT" : 40, "MRK" : 41, "LUK" : 42, "JHN" : 43, "ACT" : 44, "ROM" : 45, "1CO" : 46, "2CO" : 47, "GAL" : 48, "EPH" : 49, "PHP" : 50, "COL" : 51, "1TH" : 52, "2TH" : 53, "1TI" : 54, "2TI" : 55, "TIT" : 56, "PHM" : 57, "HEB" : 58, "JAS" : 59, "1PE" : 60, "2PE" : 61, "1JN" : 62, "2JN" : 63, "3JN" : 64, "JUD" : 65, "REV" : 66}

    #for item in book_table_of_contents_dic:
    #    print(book_table_of_contents_dic[item])


    #if not os.path.exists("/hello"):
    #    os.mkdir("/hello")
    #    if not os.path.exists("/hello/world"):
    #        os.mkdir()

    soup = BeautifulSoup(response.text, "html.parser")

    #all_tags = soup.findAll('span', class_=re.compile("verse v[0-9]+|heading"))
    all_tags = soup.findAll('span', class_=re.compile("f6 black-80"))

    print(all_tags)
