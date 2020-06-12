import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
from nltk.tokenize import word_tokenize
#------------IMPORTANT------------#
#2524 total bibles on bible.com
#need a dictionary for the bible.com book abreviations and the book number, i.e. {MRK : 41}

def page_scraper(url, book_number, chapter_number):
    #this is a long string that is printed when asked by the user

    book_table_of_contents_str = "Book 01        Genesis\n Book 02        Exodus\n Book 03        Leviticus\n Book 04        Numbers\n Book 05        Deuteronomy\n Book 07        Judges\n Book 06        Joshua\n Book 08        Ruth\n Book 09        1 Samuel\n Book 10        2 Samuel\n Book 11        1 Kings\n Book 12        2 Kings\n Book 13        1 Chronicles\n Book 14        2 Chronicles\n Book 15        Ezra\n Book 16        Nehemiah\n Book 17        Esther\n Book 18        Job\n Book 19        Psalms\n Book 20        Proverbs\n Book 21        Ecclesiastes\n Book 22        Song of Solomon\n Book 23        Isaiah\n Book 24        Jeremiah\n Book 25        Lamentations\n Book 26        Ezekiel\n Book 27        Daniel\n Book 28        Hosea\n Book 29        Joel\n Book 30        Amos\n Book 31        Obadiah\n Book 32        Jonah\n Book 33        Micah\n Book 34        Nahum\n Book 35        Habakkuk\n Book 36        Zephaniah\n Book 37        Haggai\n Book 38        Zechariah\n Book 39        Malachi\n Book 40        Matthew\n Book 41        Mark\n Book 42        Luke\n Book 43        John\n Book 44        Acts\n Book 45        Romans\n Book 46        1 Corinthians\n Book 47        2 Corinthians\n Book 48        Galatians\n Book 49        Ephesians\n Book 50        Philippians\n Book 51        Colossians\n Book 52        1 Thessalonians\n Book 53        2 Thessalonians\n Book 54        1 Timothy\n Book 55        2 Timothy\n Book 56        Titus\n Book 57        Philemon\n Book 58        Hebrews\n Book 59        James\n Book 60        1 Peter\n Book 61        2 Peter\n Book 62        1 John\n Book 63        2 John\n Book 64        3 John\n Book 65        Jude\n Book 66        Revelation\n"

    #url = 'https://www.bible.com/bible/116/MRK.1.NLT'
    #url = input("Please enter the url you want to scrape from bible.com: \n")
    #print(url)
    response = requests.get(url)

    #grap the file name to be created from the url
    file_name = re.search("/[\.a-zA-Z0-9]*$", url)
    print(file_name.group())

    soup = BeautifulSoup(response.text, "html.parser")


    #get the book and chapter number from the user to print inside the final document
    book_number = -100
    chapter_number = -100

    while book_number < 0:
        book_number = input("Please enter the books number or type '-999' for a list of books and corresponding number: ")
        book_number = int(book_number)
        if book_number == -999:
            print(book_table_of_contents_str)

    while chapter_number < 0:
        chapter_number = input("Please enter the chapter number(001, 002, 003, ..., 010, 011, 012, ...), if this section of the Bible does not have chapters press 1: ")
        chapter_number = int(chapter_number)


    file_name = str(file_name.group())[1:]
    file = open(str(file_name)+".txt", "w")

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
                print(current_working_verse)
                print(token)
                print(tokened_working_verse)
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
            if child['class'] == ['wj']:
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
