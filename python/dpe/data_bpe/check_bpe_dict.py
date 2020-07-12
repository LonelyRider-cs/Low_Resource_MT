def get_dict_info(fname):
    seg2count = {}
    with open(fname) as f:
        for line in f:
            word, count = line.strip().split()
            seg2count[word] = int(count)
    return seg2count

seg2count_eng = get_dict_info("English-Basque/dict.English.txt")
seg2count_bas = get_dict_info("English-Basque/dict.Basque.txt")

def get_bpe_info(fname, foutname):
    seg2count = {}
    with open(fname) as f:
        for line in f:
            for word in line.strip().split():
                if word not in seg2count:
                    seg2count[word] = 1
                else:
                    seg2count[word] += 1
    with open(foutname, 'w') as fw:
        for word, count in seg2count.items():
            fw.write(word + ' ' + str(count) + '\n')
    return seg2count

BPEseg2count_eng = get_bpe_info("English-Basque/train.English-Basque.English", "English-Basque/dict.English.in.txt")
BPEseg2count_bas = get_bpe_info("English-Basque/train.English-Basque.Basque", "English-Basque/dict.Basque.in.txt")

def compare_keys(dict1, dict2):
    count = 0
    print('dict1 only:')
    for k in dict1.keys():
        if k not in dict2:
            count += 1
            print(count, k)
    print('---------------')
    print('dict2 only:')
    for k in dict2.keys():
        if k not in dict1:
            count += 1
            print(count, k)

print('---checking English---')
compare_keys(seg2count_eng, BPEseg2count_eng)
print('---checking Basque---')
compare_keys(seg2count_bas, BPEseg2count_bas)
