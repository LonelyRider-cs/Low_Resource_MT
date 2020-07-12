#!/bin/bash

srclang=$1
tgtlang=$2

data_dir='data_bpe'
direction=$srclang-$tgtlang
bpe_data_dir=$data_dir/$direction
mkdir -p $bpe_data_dir

# 1. use sentencepiece (https://github.com/google/sentencepiece) to segment your corpus via BPE algorithm.

python3 sentencepiece_preprocess.py $srclang

cp $data_dir/$srclang/$srclang.txt $bpe_data_dir/train.$direction.input
cp $data_dir/$srclang/$srclang.txt $bpe_data_dir/dev.$direction.input
cp $data_dir/$srclang/$srclang.txt $bpe_data_dir/test.$direction.input

python3 sentencepiece_preprocess.py $tgtlang

cp $data_dir/$tgtlang/$tgtlang.txt $bpe_data_dir/train.$direction.output
cp $data_dir/$tgtlang/$tgtlang.txt $bpe_data_dir/dev.$direction.output
cp $data_dir/$tgtlang/$tgtlang.txt $bpe_data_dir/test.$direction.output

# 2. use fairseq (https://github.com/pytorch/fairseq) to construct **a shared BPE dictionary**. Then you will get two files: dict.src.txt and dict.tgt.txt

fairseq-preprocess \
     --source-lang="${direction}.input" \
     --target-lang="${direction}.output" \
     --trainpref="${bpe_data_dir}/train" \
     --tokenizer=space \
     --thresholdsrc=1 \
     --thresholdtgt=1 \
     --workers=20 \
     --joined-dictionary \
     --destdir="data-bin/${direction}/"

#     --validpref="${bpe_data_dir}/dev" \
#     --testpref="${bpe_data_dir}/test" \

# 3. create **a character-level dictionary based on the BPE-ed [[training]] corpus**. Please follow the format of the BPE dictionary and name your char dicts as: dict.src.in.txt and dict.tgt.in.txt
# ??? ???

# 4. put the train/dev/test and dict files together. and change DATA var in submit_drop script to the dir where your data is located.


# 5. train your DPE model via this command: sh submit_drop.sh SRC TGT seed epochs, where SRC is your source lang, tgt is your target lang, seed is a seed number and epochs is the maximum epochs.


# 6. segment your target data via this command: sh find_seg.sh SRC TGT seed split, where split can be train, valid and test.

