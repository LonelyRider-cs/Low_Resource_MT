import os, random, argparse
from tokenizer import tokenize

def read_data(dirname):
    id2text = {}
    format_problem = False
    for dirpath, dirs, files in os.walk(dirname):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            if fname.endswith('.txt'):
                with open(fname) as f:
                    count = 0
                    for line in f:
                        count += 1
                        lines = line.rstrip('\n').split('\t')
                        if len(lines) == 2:
                            id2text[lines[0]] = lines[1]
                        else:
                            print("--------Please make sure Line {} in {} is in right format--------".format(count, fname))
                            format_problem = True
                            break
            if format_problem:
                break
        if format_problem:
            break
    return id2text

def checkOverlap(srclang_id2text, tgtlang_id2text2, verbose=False):
    """
    Check whether the line number in the two languages are the same.
    If not, print out lines in source-language-only lines and target-language-only lines.
    Return the list of ids in both src and tgt language.
    """
    src_ids = set(srclang_id2text.keys())
    tgt_ids = set(tgtlang_id2text2.keys())
    srconly = src_ids.difference(tgt_ids)
    tgtonly = tgt_ids.difference(src_ids)

    if len(srconly) == 0 and len(tgtonly) == 0:
        print('GREAT! Source language and Target language have identical line numbers!')
    else:
        print('OOPS! {} source language lines missing in target language.'.format(len(srconly)))
        print('OOPS! {} target language lines missing in source language.'.format(len(tgtonly)))
    if verbose:
        print('Source language lines missing in target language: \n{}\n'.format(srconly))
        print('Target language lines missing in source language: \n{}'.format(tgtonly))
    return list(src_ids.intersection(tgt_ids))


def map_data(srclang_id2text, tgtlang_id2text, idlist,
             srclang, tgtlang,
             source_tokenizer = None, target_tokenizer = None,
             source_syllabifier = None, target_syllabifier = None,
             datatype = None):
    srclang_name = srclang.split('/')[-1]
    tgtlang_name = tgtlang.split('/')[-1]
    direction = srclang_name + '-' + tgtlang_name
    if datatype:
        inputfile = datatype + '.' + direction + '.input'
        outputfile = datatype + '.' + direction + '.output'
    else:
        inputfile = direction + '.input'
        outputfile = direction + '.output'

    with open(inputfile, 'w') as fin, open(outputfile, 'w') as fout:
        for id in idlist:
            fin.write(tokenize(srclang_id2text[id], source_tokenizer, source_syllabifier))
            fin.write('\n')
            fout.write(tokenize(tgtlang_id2text[id], target_tokenizer, target_syllabifier))
            fout.write('\n')

def splitBYlines(srclang_id2text, tgtlang_id2text, idlist,
                 srclang, tgtlang,
                 source_tokenizer = None, target_tokenizer = None,
                 source_syllabifier = None, target_syllabifier = None):
    """
    split the lines into train-validation-test by the ratio: 7:1:2
    """
    random.shuffle(idlist)
    train_boundary = round(len(idlist)*0.7)
    dev_boundary = round(len(idlist)*0.8)
    train_idlist = idlist[:train_boundary]
    dev_idlist = idlist[train_boundary:dev_boundary]
    test_idlist = idlist[dev_boundary:]
    map_data(srclang_id2text, tgtlang_id2text, train_idlist,
             srclang=srclang, tgtlang=tgtlang,
             source_tokenizer =  source_tokenizer, target_tokenizer = target_tokenizer,
             source_syllabifier = source_syllabifier, target_syllabifier=target_syllabifier,
             datatype='train')
    map_data(srclang_id2text, tgtlang_id2text, dev_idlist,
             srclang=srclang, tgtlang=tgtlang,
             source_tokenizer = source_tokenizer, target_tokenizer = target_tokenizer,
             source_syllabifier = source_syllabifier, target_syllabifier=target_syllabifier,
             datatype='dev')
    map_data(srclang_id2text, tgtlang_id2text, test_idlist,
             srclang=srclang, tgtlang=tgtlang,
             source_tokenizer = source_tokenizer, target_tokenizer = target_tokenizer,
             source_syllabifier = source_syllabifier, target_syllabifier=target_syllabifier,
             datatype='test')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type = str, required=True, help = "dir name for source language")
    parser.add_argument("-t", "--target", type=str, required=True, help="dir name for target language")
    parser.add_argument("-split", "--split", action='store_true', required=False, help="If specified, split the data lines into train-dev-test with the ratio of 7:1:2")
    parser.add_argument("-stk", "--source_tokenizer", type = str, required=False,
                        help="For the source language, you can specify '-stk eng' to tokenize the text with the English tokenizer, or '-stk other' to tokenize the text with the tokenizer for other languages. When not specified or if you specify tokenizer names other than 'eng' and 'other', no tokenization is conducted")
    parser.add_argument("-ttk", "--target_tokenizer", type=str, required=False,
                        help="For the target language, you can specify '-stk eng' to tokenize the text with the English tokenizer, or '-stk other' to tokenize the text with the tokenizer for other languages. When not specified or if you specify tokenizer names other than 'eng' and 'other', no tokenization is conducted")
    parser.add_argument("-ssl", "--source_syllabifier", type=str, required=False,
                        help="For the source language, you can specify '-ssl eus' to break words in to syllables by the Basque syllabifier. Currently, only Basque syllabifier is provided. More syllabifier choices will be added. Please install foma first if you want to use the syllabifier.")
    parser.add_argument("-tsl", "--target_syllabifier", type=str, required=False,
                        help="For the target language, you can specify '-tsl eus' to break words in to syllables by the Basque syllabifier. Currently, only Basque syllabifier is provided. More syllabifier choices will be added. Please install foma first if you want to use the syllabifier.")
    parser.add_argument("-v", "--verbose", action='store_true', required=False,
                        help="If specified, print out the lines only the source language or only the target language")

    args = parser.parse_args()

    srclang = args.source
    tgtlang = args.target
    srclang_id2text = read_data(srclang)
    tgtlang_id2text = read_data(tgtlang)
    common_lines = checkOverlap(srclang_id2text, tgtlang_id2text, args.verbose)

    if args.source_tokenizer:
        source_tokenizer = args.source_tokenizer
    else:
        source_tokenizer = None
    if args.target_tokenizer:
        target_tokenizer = args.target_tokenizer
    else:
        target_tokenizer = None

    if args.source_syllabifier:
        source_syllabifier = args.source_syllabifier
    else:
        source_syllabifier = None
    if args.target_syllabifier:
        target_syllabifier = args.target_syllabifier
    else:
        target_syllabifier = None

    if args.split:
        splitBYlines(srclang_id2text, tgtlang_id2text, common_lines,
                     srclang = srclang, tgtlang = tgtlang,
                     source_tokenizer = source_tokenizer, target_tokenizer = target_tokenizer,
                     source_syllabifier = source_syllabifier, target_syllabifier=target_syllabifier)
    else:
        map_data(srclang_id2text, tgtlang_id2text, common_lines,
                 srclang=srclang, tgtlang=tgtlang,
                 source_tokenizer = source_tokenizer, target_tokenizer = target_tokenizer,
                 source_syllabifier = source_syllabifier, target_syllabifier=target_syllabifier)



if __name__ == "__main__":
    main()

