from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

def tokenize(text_string, tokenizer_type):
    '''
    Given a string of text and a type of tokenizer to use;
    Return the tokenized string of text.
    '''
    if tokenizer_type is None:
        tokened = text_string
    elif tokenizer_type.lower() == 'eng' or tokenizer_type.lower()[:3] == 'eng':
        tokens = word_tokenize(text_string.replace("’", "'").replace("—", " — "))
        tokened = ' '.join(tokens)
    elif tokenizer_type.lower() == 'other':
        tokenizer = RegexpTokenizer("[^\s.\";:,.“”\[\(\)?!]+|[^\w\d'\s\-]")
        tokens = tokenizer.tokenize(text_string)
        tokened = ' '.join(tokens)
    else:
        tokened = text_string
    return tokened