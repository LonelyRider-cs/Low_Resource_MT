import os, random, argparse

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

def checkOverlap(srclang_id2text, tgtlang_id2text2):
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
        print('OOPS! {} source language lines BUT missing in target language.'.format(len(srconly)))
        print('OOPS! {} arget language lines BUT missing in source language.'.format(len(tgtonly)))
    # print('Source language lines missing in target language: \n{}\n'.format(srconly))
    # print('Target language lines missing in source language: \n{}'.format(tgtonly))
    return list(src_ids.intersection(tgt_ids))


def map_data(srclang_id2text, tgtlang_id2text, idlist, srclang, tgtlang, datatype = None):
    direction = srclang + '-' + tgtlang
    if datatype:
        inputfile = datatype + '.' + direction + '.input'
        outputfile = datatype + '.' + direction + '.output'
    else:
        inputfile = direction + '.input'
        outputfile = direction + '.output'

    with open(inputfile, 'w') as fin, open(outputfile, 'w') as fout:
        for id in idlist:
            fin.write(srclang_id2text[id])
            fin.write('\n')
            fout.write(tgtlang_id2text[id])
            fout.write('\n')

def splitBYlines(srclang_id2text, tgtlang_id2text, idlist, srclang, tgtlang):
    """
    split the lines into train-validation-test by the ratio: 7:1:2
    """
    random.shuffle(idlist)
    train_boundary = round(len(idlist)*0.7)
    dev_boundary = round(len(idlist)*0.8)
    train_idlist = idlist[:train_boundary]
    dev_idlist = idlist[train_boundary:dev_boundary]
    test_idlist = idlist[dev_boundary:]
    map_data(srclang_id2text, tgtlang_id2text, train_idlist, datatype='train', srclang=srclang, tgtlang=tgtlang)
    map_data(srclang_id2text, tgtlang_id2text, dev_idlist, datatype='dev', srclang=srclang, tgtlang=tgtlang)
    map_data(srclang_id2text, tgtlang_id2text, test_idlist, datatype='test', srclang=srclang, tgtlang=tgtlang)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type = str, required=True, help = "dir name for source language")
    parser.add_argument("-t", "--target", type=str, required=True, help="dir name for target language")
    parser.add_argument("-split", "--split", action='store_true', required=False, help="If specified, split the data lines into train-dev-test with the ratio of 7:1:2")
    args = parser.parse_args()

    srclang = args.source
    tgtlang = args.target
    srclang_id2text = read_data(srclang)
    tgtlang_id2text = read_data(tgtlang)
    common_lines = checkOverlap(srclang_id2text, tgtlang_id2text)
    if args.split:
        splitBYlines(srclang_id2text, tgtlang_id2text, common_lines, srclang = srclang, tgtlang = tgtlang)
    else:
        map_data(srclang_id2text, tgtlang_id2text, common_lines, srclang=srclang, tgtlang=tgtlang)



if __name__ == "__main__":
    main()

