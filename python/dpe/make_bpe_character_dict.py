import os, sys
from collections import defaultdict

fin_name = sys.argv[1]
fout_name = sys.argv[2]

char2count = defaultdict(int)
with open(fin_name) as f:
    for line in f:
        items = line.strip().split()
        for item in items:
            char2count[item] += 1

with open(fout_name, "w") as fw:
    for word, count in char2count.items():
        fw.write(word + ' ' + str(count) + '\n')