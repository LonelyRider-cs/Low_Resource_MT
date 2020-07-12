"""
Please make sure your have foma.py in the same directory as this file.
"""

from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import foma
import sentencepiece as spm
import subword_nmt.learn_bpe
import subword_nmt.apply_bpe


def normalize_navajo(text: str) -> str:
    """
    Some Navajo sources which use RIGHT SINGLE QUOTATION MARK (2019) ’ or MODIFIER LETTER APOSTROPHE (02BC) ʼ for apostrophe.
    This is to convert these symbols to apostrohes.
    """
    return text.replace("’", "'").replace("ʼ", "'")

def basic_tokenizer(text: str, tokenizer_type = None) -> str:
    """
    segment punctuations from words
    """
    if tokenizer_type is None:
        segmented = text
    elif tokenizer_type.lower() == 'eng' or tokenizer_type.lower()[:3] == 'eng':
        tokens = word_tokenize(text.replace("’", "'").replace("—", " — "))
        segmented = ' '.join(tokens)
    elif tokenizer_type.lower() == 'other':
        tokenizer = RegexpTokenizer("[^\s.\";:,.“”\[\(\)?!]+|[^\w\d'\s\-]")
        tokens = tokenizer.tokenize(text)
        segmented = ' '.join(tokens)
    else:
        print("!!! Unrecognized specifier name! Please make sure you specified a valid tokenizer.")
    return segmented

def syllabifier(text: str, syllabifier_type = None) -> str:
    """
    segment words by using foma transducer syllabifiers
    """
    if 'eus' in syllabifier_type:
        fomafile = "foma_tokenizer/eus_wordtokenizer.fomabin"
    elif 'nav' in syllabifier_type:
        fomafile = "foma_tokenizer/nav_wordtokenizer.fomabin"
    else:
        print("!!! Unrecognized syllabifier name! Please make sure you have a .fomabin file for the language you specify")
    syllabifier = foma.FST.load(fomafile)
    wordlist_syllabified = []
    for token in text.split():
        syllabified = syllabifier[token][0].decode("utf-8")
        # syllabified = syllabified.replace('@', '')
        syllabified = syllabified.replace('@ @', '@@ ')
        wordlist_syllabified.append(syllabified)
    outputstring = ' '.join(wordlist_syllabified)
    return outputstring


def preprocess(text, language=None, tokenizer_type=None, syllabifier_type = None):
    '''
    Given a string of text, a type of tokenizer to use, and a type of syllabifier to apply;
    Return the text in the format of the tokenized string each breaks into a sequence of syllables.
    '''
    # normalized navajo data
    if language.lower() in ['navajo', 'nvjob']:
        normalize_navajo(text)

    # segment punctuations from words
    segmented = basic_tokenizer(text, tokenizer_type)

    # break words into syllables
    if syllabifier_type:
        segmented = syllabifier(segmented, syllabifier_type)

    return segmented


def sentencepiece_train(training_file_name: str, model_prefix: str, model_type: str='bpe', vocab_size: int=16000, user_defined_symbols=[]):
    """
    train a BPE model
    """
    spm.SentencePieceTrainer.train(input=training_file_name,
                                   model_prefix=model_prefix,
                                   vocab_size=vocab_size,
                                   user_defined_symbols=user_defined_symbols,
                                   model_type=model_type)

def sentencepiece_segment(text: str, model_file_name: str) -> str:
    # segmentation
    sp = spm.SentencePieceProcessor(model_file=model_file_name)
    text_bpe = sp.encode(text, out_type=str)
    text_bpe = " ".join(text_bpe)
    return text_bpe


def bpe_train(training_file_name: str, model_file_name: str, num_symbols: int):
    with open(training_file_name) as data, open(model_file_name, 'w') as model:
        subword_nmt.learn_bpe.learn_bpe(data, model, num_symbols)

def bpe_segment(text: str, model_file_name: str) -> str:
    with open(model_file_name) as model:
        bpe = subword_nmt.apply_bpe.BPE(model)
        text = bpe.process_line(text)
    return text



# def tokenize(text, language = None, tokenizer_type = None, syllabifier_type = None, bpe = None):
#     '''
#     Given a string of text, a type of tokenizer to use, and a type of syllabifier to apply;
#     Return the text in the format of the tokenized string each breaks into a sequence of syllables.
#     '''
#     # normalized navajo data
#     if language.lower() in ['navajo', 'nvjob']:
#         normalize_navajo(text)
#
#     # segment punctuations from words
#     segmented = basic_tokenizer(text, tokenizer_type)
#
#     # break words into syllables
#     if syllabifier_type:
#         segmented = syllabifier(segmented, syllabifier_type)
#
#
#
#     return segmented