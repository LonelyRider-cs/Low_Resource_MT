import requests
import urllib.request
import os
import time
from bs4 import BeautifulSoup
import re
from nltk.tokenize import word_tokenize
#------------IMPORTANT------------#
#2524 total bibles on bible.com


def page_scraper(url, book, book_number, chapter_number, lang_code):

    response = requests.get(url)

    #grap the file name to be created from the url
    file_name = re.search("/[\.a-zA-Z0-9]*$", url)
    print(file_name.group())

    soup = BeautifulSoup(response.text, "html.parser")

    file_name = str(file_name.group())[1:]
    if not os.path.exists("/" + str(lang_code) + "/" + str(book)):
        os.makedirs(str(lang_code)+ "/" + str(book_number) + "_" + str(book), exist_ok = True)
        file = open(str(lang_code) + "/" + str(book_number) + "_" + str(book) + "/" + str(file_name)+".txt", "w")
    else:
        file = open(str(lang_code) + "/" + str(book_number) + "_" + str(book) + "/" + str(file_name)+".txt", "w")


    #get all the tags that contain a verse
    all_tags = soup.findAll('span', class_=re.compile("(verse v[0-9]+)"))
    #print(all_tags)
    psuedo_file = []
    verse_count = 1
    current_working_verse = ""
    tokened_working_verse = ""
    #loop through all the verses
    for tag in all_tags:

        #this check is not neeeded currently, if we add labels/titles this will be useful then
        if tag['class'][0] == 'verse':
            temp_verse = int(tag['class'][1][1:])

            #if our verse changes we know to then append the current verses, then update the verse count and reset the current verse string to blank
            #this also writes to the specified text file
            if verse_count != temp_verse:
                #tokenize all words and symbols before writing to file
                token = word_tokenize(current_working_verse.replace("’", "'"))
                tokened_working_verse = ' '.join(token)
                #print(current_working_verse)
                #print(token)
                #print(tokened_working_verse)
                if len(str(verse_count)) == 1:
                    file.write(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                    #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse)
                    #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse)
                if len(str(verse_count)) == 2:
                    file.write(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                    #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse)
                    #print(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse)
                if len(str(verse_count)) == 3:
                    file.write(str(book_number) + ":" + str(chapter_number) + ":" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                    #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":" + str(verse_count) + ":0\t " + tokened_working_verse)
                    #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse)
                #updating count and clearing string
                verse_count = temp_verse
                current_working_verse = ""
                tokened_working_verse = ""

        #loop through all the tags children to get to the content of the verse
        #for some reason most of the verses are within a class called content,
        #however there appears that when writing is in red the class is called wj
        #and then within that is the class called content. See the online HTML if confusing
        for child in tag.children:
            #print(child)
            if child['class'] == ['content']:
                #print(child.text)
                current_working_verse += child.text
            if child['class'] != ['content']:
                for gchild in child:
                    if gchild['class'] == ['content']:
                        #print(gchild.text)
                        current_working_verse += gchild.text

    #tokenize that last line
    token = word_tokenize(current_working_verse.replace("’", "'"))
    tokened_working_verse = ' '.join(token)
    #print(tokened_working_verse)
    #at the end here we need to add the last verse no matter what due to the way the for loop is set up
    if len(str(verse_count)) == 1:
        file.write(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
        psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse)
        #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0    " + tokened_working_verse)
    if len(str(verse_count)) == 2:
        file.write(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
        psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse)
        #print(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse)
    if len(str(verse_count)) == 3:
        file.write(str(book_number) + ":" + str(chapter_number) + ":" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
        psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":" + str(verse_count) + ":0\t" + tokened_working_verse)
        #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse)
    #print(psuedo_file)
    file.close()
    return 0

def driver():
    book_table_of_contents_dic = {"GEN" : 1, "EXO" : 2, "LEV" : 3, "NUM" : 4, "DEU" : 5, "JOS" : 6, "JDG" : 7, "RUT" : 8, "1SA" : 9, "2SA" : 10, "1KI" : 11, "2KI" : 12, "1CG" : 13, "2CH" : 14, "EZR" : 15, "NEH" : 16, "EST" : 17, "JOB" : 18, "PSA" : 19, "PRO" : 20, "ECC" : 21, "SNG" : 22, "ISA" : 23, "JER" : 24, "LAM" : 25, "EZK" : 26, "DAN" : 27, "HOS" : 28, "JOL" : 29, "AMO" : 30, "OBA" : 31, "JON" : 32, "MIC" : 33, "NAH" : 34, "HAB" : 35, "ZEP" : 36, "HAG" : 37, "ZEC" : 38, "MAL" : 39, "MAT" : 40, "MRK" : 41, "LUK" : 42, "JHN" : 43, "ACT" : 44, "ROM" : 45, "1CO" : 46, "2CO" : 47, "GAL" : 48, "EPH" : 49, "PHP" : 50, "COL" : 51, "1TH" : 52, "2TH" : 53, "1TI" : 54, "2TI" : 55, "TIT" : 56, "PHM" : 57, "HEB" : 58, "JAS" : 59, "1PE" : 60, "2PE" : 61, "1JN" : 62, "2JN" : 63, "3JN" : 64, "JUD" : 65, "REV" : 66}
    #loop through all 2524 bibles
    #change the numbers to scrape specific bibles,
    #lets say you only want bible 1245, then it would be range(1245, 1246)
    #all ->  range(1, 2525)
    #first -> range(1,2)
    for i in range(1,2):
        #get the language code
        lang_code = get_lang_code(i)
        #if lang code comes back false, then we know its a bad url
        if lang_code != False:
            #if the lang code is good then we want to loop through all the books in the bible
            for book in book_table_of_contents_dic:
                chapter_count = 1
                status = True
                #for each book we also need to loop though all the chapters
                #status changes to false when a book or chapter is not in this specific edition of the bible.
                #due to the way bible.com works, if you throw a bad url at it but the 'bible.com/bible/' is there it automaticaly brings you to 'bible.com/bible/1/GEN.1.KJV'
                #comparing the url given back to the one created, if they match then we are good to scrape that page
                #if they do not match then we know to move on to the next book/chapter
                while status == True:
                    url = "https://www.bible.com/bible/" + str(i) + "/" + str(book) + "." + str(chapter_count) + "." + str(lang_code)
                    response =  requests.get(url)
                    print(response.url)
                    if response.url != url:
                        status = False
                    else:
                        print(url)
                        #after satisfying all othre conditions we then scrape the web page and store the data
                        page_scraper(url, book, book_table_of_contents_dic[book], chapter_count, lang_code)
                        chapter_count += 1
        else:
            continue

def get_lang_code(i):
    #this grabs the language code for the current bible being checked.
    url = "https://www.bible.com/bible/" + str(i)
    response = requests.get(url)
    if response.status_code == 200:
        lang_code = re.search(".[a-zA-Z0-9]*$", response.url)
        return lang_code.group()[1:]
    else:
        return False


if __name__ == '__main__':
    driver()
