from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer



def basic_tokenizer(text: str, tokenizer_type = None) -> str:
    """
    segment punctuations from words
    """
    if tokenizer_type is None:
        segmented = text
    elif tokenizer_type.lower() == 'eng' or tokenizer_type.lower()[:3] == 'eng':
        tokens = word_tokenize(text.replace("’", "'").replace("—", " — "))
        segmented = ' '.join(tokens)
    else:
        tokenizer = RegexpTokenizer("[^\s.\";:,.“”\[\(\)?!]+|[^\w\d'\s\-]")
        tokens = tokenizer.tokenize(text)
        segmented = ' '.join(tokens)
    return segmented
