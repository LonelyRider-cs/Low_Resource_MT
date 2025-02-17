import os, random, argparse
from tokenizer import preprocess, \
                      sentencepiece_train, sentencepiece_segment, \
                      bpe_train, bpe_segment

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
                            id2text[lines[0].strip()] = lines[1].strip()
                        else:
                            print("--------Please make sure Line {} in {} is in right format--------".format(count, fname))
                            format_problem = True
                            break
            if format_problem:
                break
        if format_problem:
            break
    return id2text

def read_tokenized_data(fname):
    id2text = {}
    with open(fname) as f:
        count = 0
        for line in f:
            count += 1
            lines = line.rstrip('\n').split('\t')
            if len(lines) == 2:
                id2text[lines[0].strip()] = lines[1].strip()
            else:
                print("--------Please make sure Line {} in {} is in right format--------".format(count, fname))
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
    common_lines = []
    for item in srclang_id2text.keys():
        if item in tgt_ids:
            common_lines.append(item)
    return common_lines
    # return list(src_ids.intersection(tgt_ids))


def _tokenize_preprocess(id2text, idlist, language, tokenizer, syllabifier, ftmp, fall, fmap):
    tokenized_id2text = {id: preprocess(text, language, tokenizer, syllabifier)
                         for id, text in id2text.items()}
    for id, text in tokenized_id2text.items():
        ftmp.write(text + '\n')
        fall.write(str(id) + '\t' + text + '\n')
    for id in idlist:
        text = tokenized_id2text[id]
        fmap.write(text + '\n')

def _tokenize_sentencepiece(language, id2text, training_file, model_dir, model_type='bpe', vocab_size=16000, user_defined_symbols=[]):
    # train sentencepiece model
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model_prefix = os.path.join(model_dir, language)
    sentencepiece_train(training_file, model_prefix, model_type, vocab_size, user_defined_symbols)

    # segment text with sentencepiece model
    id2sentencepiece_text = {}
    model = model_prefix + '.model'
    count = 0
    for id, text in id2text.items():
        if not count%1000:
            print('> line {}'.format(id))
            print('> before sentencepiece segmentation:', text)
        text = sentencepiece_segment(text, model)
        id2sentencepiece_text[id] = text
        if not count % 1000:
            print('> after sentencepiece segmentation:', text)
            print()
        count += 1
    return id2sentencepiece_text

def _tokenize_bpe(id2text, training_file, model_dir, language, vocab_size):

    # train BPE model
    print("... training BPE model ...")
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    model_file = os.path.join(model_dir, language+'.bpe.model')
    bpe_train(training_file, model_file, vocab_size)

    # segment text with BPE model
    print("... segmenting text with BPE model ...")
    id2bpe_text = {}
    count = 0
    for id, text in id2text.items():
        if not count%1000:
            print('> line {}'.format(id))
            print('> before BPE segmentation:', text)
        text = bpe_segment(text, model_file)
        id2bpe_text[id] = text
        if not count % 1000:
            print('> after BPE segmentation:', text)
            print()
        count += 1
    return id2bpe_text

def _write_to_file(id2text, idlist, fall, fmapped):
    for id, text in id2text.items():
        fall.write(str(id) + '\t' + text + '\n')
    for id in idlist:
        text = id2text[id]
        fmapped.write(text + '\n')

def map_data(srclang_id2text, tgtlang_id2text, idlist,
             srclang, tgtlang,
             source_tokenizer = None, target_tokenizer = None,
             source_syllabifier = None, target_syllabifier = None,
             source_sentencepiece = None, target_sentencepiece = None,
             source_bpe=None, target_bpe=None,
             datatype = 'shared'):
    srclang_name = srclang.split('/')[-1]
    tgtlang_name = tgtlang.split('/')[-1]
    direction = srclang_name + '-' + tgtlang_name
    inputfile = datatype + '.' + direction + '.input'
    outputfile = datatype + '.' + direction + '.output'
    all_src = srclang_name + '.txt'
    all_tgt = tgtlang_name + '.txt'
    tmp_src = srclang_name + '.tmp'
    tmp_tgt = tgtlang_name + '.tmp'

    output_dir = "../data_in_MT_format/"+direction
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    inputfile = os.path.join(output_dir, inputfile)
    outputfile = os.path.join(output_dir, outputfile)
    all_src = os.path.join(output_dir, all_src)
    all_tgt = os.path.join(output_dir, all_tgt)
    tmp_src = os.path.join(output_dir, tmp_src)
    tmp_tgt = os.path.join(output_dir, tmp_tgt)

    with open(tmp_src, 'w') as ftmp_src, open(tmp_tgt, 'w') as ftmp_tgt, \
        open(all_src, 'w') as fall_src, open(all_tgt, 'w') as fall_tgt, \
        open(inputfile, 'w') as fin, open(outputfile, 'w') as fout:
        _tokenize_preprocess(srclang_id2text, idlist, srclang,
                    source_tokenizer,
                    source_syllabifier,
                    ftmp_src, fall_src, fin)
        _tokenize_preprocess(tgtlang_id2text, idlist, tgtlang,
                    target_tokenizer,
                    target_syllabifier,
                    ftmp_tgt, fall_tgt, fout)

    if source_sentencepiece:
        print('>>> source sentencepiece vocabulary size:', source_sentencepiece)
        model_type, vocab_size = source_sentencepiece
        model_dir = '../' + model_type + '_models/'
        srclang_id2text = _tokenize_sentencepiece(language=srclang_name,
                                        id2text=read_tokenized_data(all_src),
                                        training_file=tmp_src,
                                        model_dir=model_dir,
                                        model_type=model_type,
                                        vocab_size=vocab_size,
                                        user_defined_symbols=[])
    if target_sentencepiece:
        print('>>> target sentencepiece vocabulary size:', target_sentencepiece)
        model_type, vocab_size = target_sentencepiece
        model_dir = '../' + model_type + '_models/'
        tgtlang_id2text = _tokenize_sentencepiece(language=tgtlang_name,
                                        id2text=read_tokenized_data(all_tgt),
                                        training_file=tmp_tgt,
                                        model_dir=model_dir,
                                        model_type=model_type,
                                        vocab_size=vocab_size,
                                        user_defined_symbols=[])

    model_dir = '../bpe_models/'
    if source_bpe:
        print('>>> source bpe number of symbols:', source_bpe)
        srclang_id2text = _tokenize_bpe(id2text=read_tokenized_data(all_src),
                                                  training_file=tmp_src,
                                                  model_dir=model_dir,
                                                  language=srclang_name,
                                                  vocab_size=source_bpe)
    if target_bpe:
        print('>>> target bpe number of symbols:', target_bpe)
        tgtlang_id2text = _tokenize_bpe(id2text=read_tokenized_data(all_tgt),
                                                  training_file=tmp_tgt,
                                                  model_dir=model_dir,
                                                  language=tgtlang_name,
                                                  vocab_size=target_bpe)

    with open(all_src, 'w') as fall_src, open(all_tgt, 'w') as fall_tgt, \
        open(inputfile, 'w') as fin, open(outputfile, 'w') as fout:
        _write_to_file(srclang_id2text, idlist, fall_src, fin)
        _write_to_file(tgtlang_id2text, idlist, fall_tgt, fout)
    # os.system('rm '+output_dir+'/*.tmp')

def _write_split_idlist(foutname, idlist):
    with open(foutname, 'w') as fw:
        for id in idlist:
            fw.write(id + '\n')

def splitBYlines(idlist, srclang, tgtlang, verbose=False):
    """
    split the lines into train-validation-test by the ratio: 7:1:2
    """
    random.shuffle(idlist)
    train_boundary = round(len(idlist)*0.7)
    dev_boundary = round(len(idlist)*0.8)
    train_idlist = idlist[:train_boundary]
    dev_idlist = idlist[train_boundary:dev_boundary]
    test_idlist = idlist[dev_boundary:]

    srclang_name = srclang.split('/')[-1]
    tgtlang_name = tgtlang.split('/')[-1]
    direction = srclang_name + '-' + tgtlang_name
    datadir = "../data_in_MT_format/" + direction
    srcdata = os.path.join(datadir, srclang_name + '.txt')
    tgtdata = os.path.join(datadir, tgtlang_name + '.txt')
    srclang_id2text = read_tokenized_data(srcdata)
    tgtlang_id2text = read_tokenized_data(tgtdata)

    for datatype, idlist in zip(['train', 'dev', 'test'], [train_idlist, dev_idlist, test_idlist]):
        inputfile = os.path.join(datadir, datatype + '.' + direction + '.input')
        outputfile = os.path.join(datadir, datatype + '.' + direction + '.output')
        with open(inputfile, 'w') as fin, open(outputfile, 'w') as fout:
            for id in idlist:
                fin.write(srclang_id2text[id] + '\n')
                fout.write(tgtlang_id2text[id] + '\n')
    if verbose:
        ftrainID = os.path.join(datadir, 'train.idlist.txt')
        fdevID = os.path.join(datadir, 'dev.idlist.txt')
        ftestID = os.path.join(datadir, 'test.idlist.txt')
        _write_split_idlist(ftrainID, train_idlist)
        _write_split_idlist(fdevID, dev_idlist)
        _write_split_idlist(ftestID, test_idlist)



def main():

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-s", "--source",
                        type = str, required=True,
                        help = "dir name for source language")
    parser.add_argument("-t", "--target",
                        type=str, required=True,
                        help="dir name for target language")
    parser.add_argument("-split", "--split",
                        action='store_true', required=False,
                        help="If specified, split the data lines into train-dev-test with the ratio of 7:1:2")
    parser.add_argument("-stk", "--source_tokenizer",
                        type = str, required=False,
                        help="For the source language, you can specify '-stk eng' to tokenize the text with the English tokenizer, or '-stk other' to tokenize the text with the tokenizer for other languages. When not specified or if you specify tokenizer names other than 'eng' and 'other', no tokenization is conducted")
    parser.add_argument("-ttk", "--target_tokenizer",
                        type=str, required=False,
                        help="For the target language, you can specify '-stk eng' to tokenize the text with the English tokenizer, or '-stk other' to tokenize the text with the tokenizer for other languages. When not specified or if you specify tokenizer names other than 'eng' and 'other', no tokenization is conducted")
    parser.add_argument("-ssl", "--source_syllabifier",
                        type=str, required=False,
                        help="For the source language, you can specify '-ssl eus' to break words in to syllables by the Basque syllabifier. Currently, Basque (eus) and Navajo (nav) syllabifiers are provided. More syllabifier choices will be added.")
    parser.add_argument("-tsl", "--target_syllabifier",
                        type=str, required=False,
                        help="For the target language, you can specify '-tsl eus' to break words in to syllables by the Basque syllabifier. Currently, Basque (eus) and Navajo (nav) syllabifiers are provided. More syllabifier choices will be added.")
    parser.add_argument("-ssp", "--source_sentencepiece",
                        type=str, required=False,
                        help="You can specified a tokenizer model type implemented in sentencepiece, e.g. bpe, unigram, char, or word. You can specify a model type with a customized vocabulary size in the format of {MODEL TYPE}:{VOCABULARY SIZE}, e.g. bpe:8000. Suggested values for vocabulary size are 8000, 16000, 32000, and the number should be smaller than the vocabulary size before this process of tokenization. Default vocabulary size is 16000. A sentencepiece model (the model will be saved in '{MODEL_TYPE}_models/{source}') will be trained and applied to segmented the source language text.")
    parser.add_argument("-tsp", "--target_sentencepiece",
                        type=str, required=False,
                        help="You can specified a tokenizer model type implemented in sentencepiece, e.g. bpe, unigram, char, or word. You can specify a model type with a customized vocabulary size in the format of {MODEL TYPE}:{VOCABULARY SIZE}, e.g. bpe:8000. Suggested values for vocabulary size are 8000, 16000, 32000, and the number should be smaller than the vocabulary size before this process of tokenization. Default vocabulary size is 16000. A sentencepiece model (the model will be saved in '{MODEL_TYPE}_models/{target}') will be trained and applied to segmented the target language text.")
    parser.add_argument("-sbpe", "--source_bpe",
                        type=int, required=False,
                        help="When specified, the subword_nmt implementation of BPE is used. A BPE model (the model will be saved in 'bpe_models/{source}') will be trained and applied to segmented the source language text. You can specify the vocabulary size by specifying an integer.")
    parser.add_argument("-tbpe", "--target_bpe",
                        type=int, required=False,
                        help="When specified, the subword_nmt implementation of BPE is used. A BPE model (the model will be saved in 'bpe_models/{target}') will be trained and applied to segmented the target language text. You can specify the vocabulary size by specifying an integer.")
    parser.add_argument("-v", "--verbose",
                        action='store_true', required=False,
                        help="If specified, print out the lines only the source language or only the target language. If both {verbose} and {split} are turned on, the train/dev/test id will be stored in the same directory as the split data under the name of *.idlist.txt")
    parser.add_argument("-h", "--help",
                        action="help", default=argparse.SUPPRESS,
                        help="convert the source-target languages into the format needed for MT with Fairseq. The converted data will be stored in '../data_in_MT_format/SOURCE-TARGET/'")


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

    if args.source_sentencepiece:
        source_sentencepiece = args.source_sentencepiece
        if ":" in source_sentencepiece:
            model_type, vocab_size = source_sentencepiece.split(':')
            source_sentencepiece = (model_type, int(vocab_size))
        else:
            if source_sentencepiece.isalpha():
                model_type = source_sentencepiece
                vocab_size = 16000
            else:
                model_type = 'bpe'
                vocab_size = int(source_sentencepiece)
    else:
        source_sentencepiece = None
    if args.target_sentencepiece:
        target_sentencepiece = args.target_sentencepiece
        if ":" in target_sentencepiece:
            model_type, vocab_size = target_sentencepiece.split(':')
            target_sentencepiece = (model_type, int(vocab_size))
        else:
            if target_sentencepiece.isalpha():
                model_type = target_sentencepiece
                vocab_size = 16000
            else:
                model_type = 'bpe'
                vocab_size = int(target_sentencepiece)
    else:
        target_sentencepiece = None

    if args.source_bpe:
        source_bpe = args.source_bpe
    else:
        source_bpe = None
    if args.target_bpe:
        target_bpe = args.target_bpe
    else:
        target_bpe = None

    map_data(srclang_id2text, tgtlang_id2text, common_lines,
             srclang=srclang, tgtlang=tgtlang,
             source_tokenizer=source_tokenizer, target_tokenizer=target_tokenizer,
             source_syllabifier=source_syllabifier, target_syllabifier=target_syllabifier,
             source_sentencepiece=source_sentencepiece, target_sentencepiece=target_sentencepiece,
             source_bpe=source_bpe, target_bpe=target_bpe)

    if args.split:
        splitBYlines(common_lines, srclang, tgtlang, verbose=args.verbose)




if __name__ == "__main__":
    main()

