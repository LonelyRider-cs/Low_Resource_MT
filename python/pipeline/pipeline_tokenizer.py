from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer


#this file is called when needing to tokenize anything.
#the language's three letter code is used to distinguish between different types of tokenizers
#to add a new langauge tokenizer follow the syntax below and replace 'tag' with the languages 3 letter lang_code
#elif tokenizer_type.lower() == 'tag' or tokenizer_type.lower()[:3] == 'tag':

def basic_tokenizer(text: str, tokenizer_type = None) -> str:
    """
    segment punctuations from words
    """
    #none
    if tokenizer_type is None:
        segmented = text
    #English
    elif tokenizer_type.lower() == 'eng' or tokenizer_type.lower()[:3] == 'eng':
        tokens = word_tokenize(text.replace("’", "'").replace("—", " — "))
        segmented = ' '.join(tokens)
    #Navajo
    elif tokenizer_type.lower() == 'nav' or tokenizer_type.lower()[:3] == 'nav':
        tokenizer = RegexpTokenizer("[^\s.\";:,.“”\[\(\)?!]+|[^\w\d'\s\-]")
        tokens = tokenizer.tokenize(text.replace("’", "'").replace("ʼ", "'"))
        segmented = ' '.join(tokens)
    #other
    else:
        tokenizer = RegexpTokenizer("[^\s.\";:,.“”\[\(\)?!]+|[^\w\d'\s\-]")
        tokens = tokenizer.tokenize(text)
        segmented = ' '.join(tokens)

    return segmented
