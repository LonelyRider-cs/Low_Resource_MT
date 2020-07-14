import requests
import urllib.request
import os
import time
from bs4 import BeautifulSoup
import re
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import getopt
import sys
import pipeline_tokenizer
#------------IMPORTANT------------#
#2524 total bibles on bible.com


def page_scraper(url, book, book_number, chapter_number, lang_code, TOKENIZER):

    response = requests.get(url)

    #grab the file name to be created from the url
    file_name = re.search("/[\.a-zA-Z0-9]*$", url)
    print(file_name.group())

    soup = BeautifulSoup(response.text, "html.parser")

    file_name = str(file_name.group())[1:]
    for token in TOKENIZER:
        if token == None:
            if not os.path.exists("../bible.com_scrapes/" + str(lang_code) + "/non_tokenized/" + str(book)):
                os.makedirs("../../bible.com_scrapes/"+str(lang_code)+ "/non_tokenized/" + str(book_number) + "_" + str(book), exist_ok = True)
                non_tokenized_file = open("../../bible.com_scrapes/"+str(lang_code) + "/non_tokenized/" + str(book_number) + "_" + str(book) + "/" + str(file_name)+".txt", "w")
            else:
                non_tokenized_file = open("../../bible.com_scrapes/"+str(lang_code) + "/non_tokenized/" + str(book_number) + "_" + str(book) + "/" + str(file_name)+".txt", "w")
        elif token != None:
            if not os.path.exists("../bible.com_scrapes/" + str(lang_code) + "/tokenized/" + str(book)):
                os.makedirs("../../bible.com_scrapes/"+str(lang_code)+ "/tokenized/" + str(book_number) + "_" + str(book), exist_ok = True)
                tokenized_file = open("../../bible.com_scrapes/"+str(lang_code) + "/tokenized/" + str(book_number) + "_" + str(book) + "/" + str(file_name)+".txt", "w")
            else:
                tokenized_file = open("../../bible.com_scrapes/"+str(lang_code) + "/tokenized/" + str(book_number) + "_" + str(book) + "/" + str(file_name)+".txt", "w")


    #get all the tags that contain a verse
    all_tags = soup.findAll(['span', 'div'], class_=re.compile("verse v[0-9]+|s1"))
    #print(all_tags)
    psuedo_file = []
    verse_count = 1
    heading_count = 1
    current_working_verse = ""
    tokened_working_verse = ""
    tokened_heading = ""
    #loop through all the verses
    for tag in all_tags:

        if tag['class'][0] == 's1':
            for child in tag.children:
                if child['class'][0] == 'heading':
                    for token in TOKENIZER:
                        if token == None:
                            tokened_heading = pipeline_tokenizer.basic_tokenizer(tag.text, token)
                            if len(str(heading_count)) == 1:
                                non_tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading + "\n")
                                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                                #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                            if len(str(heading_count)) == 2:
                                non_tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading + "\n")
                                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                                #print(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                            if len(str(heading_count)) == 3:
                                non_tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t" + tokened_heading + "\n")
                                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t " + tokened_heading)
                                #print(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t" + tokened_heading)
                        elif token != None:
                            tokened_heading = pipeline_tokenizer.basic_tokenizer(tag.text, str(token))
                            if len(str(heading_count)) == 1:
                                tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading + "\n")
                                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                                #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                            if len(str(heading_count)) == 2:
                                tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading + "\n")
                                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                                #print(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                            if len(str(heading_count)) == 3:
                                tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t" + tokened_heading + "\n")
                                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t " + tokened_heading)
                                #print(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t" + tokened_heading)
                    heading_count += 1
                    tokened_heading = ""

        #this check is not neeeded currently, if we add labels/titles this will be useful then
        if tag['class'][0] == 'verse':
            temp_verse = int(tag['class'][1][1:])



            #if our verse changes we know to then append the current verses, then update the verse count and reset the current verse string to blank
            #this also writes to the specified text file
            if verse_count != temp_verse:
                for token in TOKENIZER:
                    if token == None:
                        tokened_working_verse = pipeline_tokenizer.basic_tokenizer(current_working_verse, token)
                        if len(str(verse_count)) == 1:
                            non_tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                            #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                            #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                        if len(str(verse_count)) == 2:
                            non_tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                            #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                            #print(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                        if len(str(verse_count)) == 3:
                            non_tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                            #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t " + tokened_heading)
                            #print(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t" + tokened_heading)
                    elif token != None:
                        tokened_working_verse = pipeline_tokenizer.basic_tokenizer(current_working_verse, str(token))
                        if len(str(verse_count)) == 1:
                            tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                            #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                            #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                        if len(str(verse_count)) == 2:
                            tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                            #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                            #print(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                        if len(str(verse_count)) == 3:
                            tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                            #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t " + tokened_heading)
                            #print(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t" + tokened_heading)
                #updating count and clearing string
                verse_count = temp_verse
                current_working_verse = ""
                tokened_working_verse = ""

            #loop through all the tags children to get to the content of the verse
            #for some reason most of the verses are within a class called content,
            #however there appears that when writing is in red the class is called wj
            #and then within that is the class called content. See the online HTML if confusing
            for child in tag.children:

                if child['class'] == ['content']:
                    #print(child['class'])
                    #print('APPENDED: ' + child.text)
                    current_working_verse += child.text
                if child['class'] != ['content'] and child['class'] != ['label'] and child['class'] != ['heading']:
                    #print(child)
                    for gchild in child:
                        #print(gchild)
                        if gchild['class'] == ['content']:
                            #print('APPENDED: ' + gchild.text)
                            current_working_verse += gchild.text

    #tokenize that last line
    for token in TOKENIZER:
        if token == None:
            tokened_working_verse = pipeline_tokenizer.basic_tokenizer(current_working_verse, token)
            if len(str(verse_count)) == 1:
                non_tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
            if len(str(verse_count)) == 2:
                non_tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                #print(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
            if len(str(verse_count)) == 3:
                non_tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t " + tokened_heading)
                #print(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t" + tokened_heading)
        elif token != None:
            tokened_working_verse = pipeline_tokenizer.basic_tokenizer(current_working_verse, str(token))
            if len(str(verse_count)) == 1:
                tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":00" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
                #print(str(book_number) + ":" + str(chapter_number) + ":00" + str(heading_count) + ":1\t" + tokened_heading)
            if len(str(verse_count)) == 2:
                tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":0" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
                #print(str(book_number) + ":" + str(chapter_number) + ":0" + str(heading_count) + ":1\t" + tokened_heading)
            if len(str(verse_count)) == 3:
                tokenized_file.write(str(book_number) + ":" + str(chapter_number) + ":" + str(verse_count) + ":0\t" + tokened_working_verse + "\n")
                #psuedo_file.append(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t " + tokened_heading)
                #print(str(book_number) + ":" + str(chapter_number) + ":" + str(heading_count) + ":1\t" + tokened_heading)

    for token in TOKENIZER:
        if token == None:
            non_tokenized_file.close()
        elif token != None:
            tokenized_file.close()
    return 0

def driver(start, stop, TOKENIZER):
    book_table_of_contents_dic = {"GEN" : 1, "EXO" : 2, "LEV" : 3, "NUM" : 4, "DEU" : 5, "JOS" : 6, "JDG" : 7, "RUT" : 8, "1SA" : 9, "2SA" : 10, "1KI" : 11, "2KI" : 12, "1CG" : 13, "2CH" : 14, "EZR" : 15, "NEH" : 16, "EST" : 17, "JOB" : 18, "PSA" : 19, "PRO" : 20, "ECC" : 21, "SNG" : 22, "ISA" : 23, "JER" : 24, "LAM" : 25, "EZK" : 26, "DAN" : 27, "HOS" : 28, "JOL" : 29, "AMO" : 30, "OBA" : 31, "JON" : 32, "MIC" : 33, "NAH" : 34, "HAB" : 35, "ZEP" : 36, "HAG" : 37, "ZEC" : 38, "MAL" : 39, "MAT" : 40, "MRK" : 41, "LUK" : 42, "JHN" : 43, "ACT" : 44, "ROM" : 45, "1CO" : 46, "2CO" : 47, "GAL" : 48, "EPH" : 49, "PHP" : 50, "COL" : 51, "1TH" : 52, "2TH" : 53, "1TI" : 54, "2TI" : 55, "TIT" : 56, "PHM" : 57, "HEB" : 58, "JAS" : 59, "1PE" : 60, "2PE" : 61, "1JN" : 62, "2JN" : 63, "3JN" : 64, "JUD" : 65, "REV" : 66}
    #loop through all 2524 bibles
    #change the numbers to scrape specific bibles,
    #lets say you only want bible 1245, then it would be range(1245, 1246)
    #all ->  range(1, 2525)
    #first -> range(1,2)
    for i in range(start,stop):
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
                        page_scraper(url, book, book_table_of_contents_dic[book], chapter_count, lang_code, TOKENIZER)
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


#sets up the driver function
def menu(argv):
    BIBLE_LIST = []
    TOKENIZER = None

    #graps command line arguments inputed from user
    options, remainder =  getopt.gnu_getopt(argv[1:], 'al:r:s:eoh', ['all_bibles', 'list=', 'range=', 'single=', 'english_token', 'other_token', '--help'])

    for opt, arg in options:
        if opt in ('-a', '--all_bibles'):
            BIBLE_LIST.append((1,2525))
        if opt in ('-l', '--list'):
            #print(arg.split(','))
            bible_list = arg.split(',')
            for bible in bible_list:
                start = int(bible)
                stop = int(bible) + 1
                BIBLE_LIST.append((start, stop))
        if opt in ('-r', '--range'):
            #print(arg)
            bible_range = arg.split(',')
            start = int(bible_range[0])
            stop = int(bible_range[1]) + 1
            BIBLE_LIST.append((start,stop))
        if opt in ('-s', '--single'):
            start = int(arg)
            stop = int(arg) + 1
            BIBLE_LIST.append((start,stop))
        if opt in ('-e', '--english_token'):
            TOKENIZER = 'ENGLISH'
        if opt in ('-o', '--other_token'):
            TOKENIZER = 'OTHER'
        if opt in ('-h', '--help'):
            print("\n*** Bible.com webpage scraper ***\n")
            print("Usage: bible.com_web_scraper.py [OPTIONS] ")
            print("Stores specified bibles in local storage")
            print("Each bible has a unique numerical code associated to it between 1 and 2524")
            print("The tokenizer default is set to off, one needs to be specified if wanted")
            print("OPTIONS:")
            print(" -a         scrapes and stores all 2524 bibles")
            print(" -l NUM     comma seperated list of specified bibles you want")
            print(" -r NUM     two comma seperated values for a range of bibles to grab")
            print(" -s NUM     only grabs a single bible specified")
            print(" -e         tokenizes words based off of english grammar")
            print(" -o         standardized rule set for tokenizing any language")
            print(" -h         help")
            quit()

    print(BIBLE_LIST)
    print(TOKENIZER)
    for b in BIBLE_LIST:
        driver(b[0], b[1], TOKENIZER)


if __name__ == '__main__':
    menu(sys.argv)
