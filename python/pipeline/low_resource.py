import os
import sys
import getopt
import lookup
import pipeline_bible_com_web_scraper
import wikipedia_dump_grabber
import wikiDump_convert
import subprocess
import shutil

def main(argv):
    BIBLE_LIST = []
    LANG_TAG = []
    LANG_TO_SEARCH = ''
    WIKI_DUMP = False
    TOKEN_CHOICE = 2
    TOKENIZERS = []
    #graps command line arguments inputed from user
    options, remainder =  getopt.gnu_getopt(argv[1:], 'n:l:t:w', ['no_lookup=', 'lookup=', 'tokens=' 'wiki_dump', 'help'])

    for opt, arg in options:
        if opt in ('-n', '--no_lookup'):
            bible_list = arg.split(',')
            for bible in bible_list:
                start = int(bible)
                stop = int(bible) + 1
                BIBLE_LIST.append((start, stop, lookup.no_lookup(str(start))))
                LANG_TAG.append(lookup.no_lookup(str(start)))
        if opt in ('-l', '--lookup'):
            LANG_TO_SEARCH = str(arg)
            lookup.lookup(LANG_TO_SEARCH)
            bible_to_preprocess = input("Enter the index number of a bible you would like to preprocess(leave blank to finish):")
            try:
                if isinstance(int(bible_to_preprocess), int):
                    print("Begining preprocess")
                    start = int(bible_to_preprocess)
                    stop = int(bible_to_preprocess) + 1
                    BIBLE_LIST.append((start, stop, lookup.no_lookup(str(start))))
                    LANG_TAG.append(lookup.no_lookup(str(BIBLE_LIST[0][0])))
                else:
                    quit()
            except Exception as e:
                #raise e
                print("sorry this did not work")
        if opt in ('-t', '--tokens'):
            TOKEN_CHOICE = int(arg)
        if opt in ('-w', '--wiki_dump'):
            WIKI_DUMP = True
        if opt in ('-h', '--help'):
            print("\n*** Bible.com webpage scraper ***\n")
            print("Usage: low_resource.py [OPTIONS] ")
            print("Stores specified bibles and wikipedia dumps in local storage")
            print("Each bible has a unique numerical code associated to it between 1 and 2524")
            print("The tokenizer default is set to off, one needs to be specified if wanted")
            print("OPTIONS:")
            print(" -n NUM     comma seperated list of specified bibles you want")
            print(" -l WRD     language you want to search for from bible.com language table")
            print(" -w         checks if language has a wikipedia dump, if so the data is grabbed")
            print(" -t NUM     options:0-doesn't tokenize, 1-only tokenizes, 2-produces non-tokenized and tokenized(this is the default)")
            print(" -h          help")
            quit()

    print(BIBLE_LIST)
    print(LANG_TO_SEARCH)
    print(LANG_TAG)
    print(TOKENIZERS)
    print(TOKEN_CHOICE)




    if TOKEN_CHOICE == 0:
        for b in BIBLE_LIST:
            pipeline_bible_com_web_scraper.driver(b[0], b[1], [None])
            if WIKI_DUMP:
                wiki_start(b[0])
    if TOKEN_CHOICE == 1:
        for b in BIBLE_LIST:
            pipeline_bible_com_web_scraper.driver(b[0], b[1], [b[2]])
            if WIKI_DUMP:
                wiki_start(b[0])
    if TOKEN_CHOICE == 2:
        for b in BIBLE_LIST:
            pipeline_bible_com_web_scraper.driver(b[0], b[1], [None, b[2]])
            if WIKI_DUMP:
                wiki_start(b[0])







def wiki_start(lang_search):
    tag = lookup.wiki_lang_lookup(lang_search)
    print('final Wiki lookup: ' + str(tag))
    url = 'https://dumps.wikimedia.org/' + str(tag) + 'wiki/latest/' + str(tag) + 'wiki-latest-pages-meta-current.xml.bz2'
    print('url: ' + str(url))
    bz2_file_save = '../../all_wikipedia_dumps/' + str(tag) + '_latest.xml.bz2'

    try:
        wikipedia_dump_grabber.dump_downloader(url, tag)
    except Exception as e:
        print("No suitable wikipedia dump found")
        #raise e

    try:
        wiki_extract_cmd = 'python wikipedia_dump_extractor.py -o ../../all_wikipedia_dumps/text --json ' + bz2_file_save
        subprocess.call(wiki_extract_cmd, shell=True)
    except Exception as e:
        print("Could not extract wiki dump files")
        #raise e

    try:
        wiki_convert_cmd = 'python wikiDump_convert.py ' + bz2_file_save
        subprocess.call(wiki_convert_cmd, shell=True)
    except Exception as e:
        print("Could not convert extracted wike dump files")
        #raise e

    location = os.getcwd() # get present working directory location here

    shutil.rmtree(location+"/../../all_wikipedia_dumps/text")



if __name__ == '__main__':
    main(sys.argv)
