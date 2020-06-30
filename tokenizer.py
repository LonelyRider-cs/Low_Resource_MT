"""
Please make sure your have foma.py in the same directory as this file.
"""

from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import foma


def tokenize(text_string, tokenizer_type = None, syllabifier_type = None):
    '''
    Given a string of text, a type of tokenizer to use, and a type of syllabifier to apply;
    Return the text in the format of the tokenized string each breaks into a sequence of syllables.
    '''
    if tokenizer_type is None:
        # tokened = text_string
        tokens = text_string.split()
    elif tokenizer_type.lower() == 'eng' or tokenizer_type.lower()[:3] == 'eng':
        tokens = word_tokenize(text_string.replace("’", "'").replace("—", " — "))
        # tokened = ' '.join(tokens)
    elif tokenizer_type.lower() == 'other':
        tokenizer = RegexpTokenizer("[^\s.\";:,.“”\[\(\)?!]+|[^\w\d'\s\-]")
        tokens = tokenizer.tokenize(text_string)
        # tokened = ' '.join(tokens)
    else:
        # tokened = text_string
        tokens = text_string.split()

    if syllabifier_type:
        if 'eus' in syllabifier_type:
            fomafile = "eus_wordtokenizer.fomabin"
        else:
            print("!!!please make sure you have a .fomabin file for the language you specify")
        syllabifier = foma.FST.load(fomafile)
        wordlist_syllabified = []
        for token in tokens:
            syllabified = syllabifier[token][0].decode("utf-8")
            syllabified = syllabified.replace('@', '')
            wordlist_syllabified.append(syllabified)
        outputstring = ' '.join(wordlist_syllabified)
    else:
        outputstring = ' '.join(tokens)

    return outputstring