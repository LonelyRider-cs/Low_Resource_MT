#!/bin/bash

srclang=$1
tgtlang=$2
seed=$3

data_dir='data_bpe'
direction=$srclang-$tgtlang
bpe_data_dir=$data_dir/$direction
mkdir -p $bpe_data_dir
train_data_dir="example_data"
#train_data_dir="../../data_in_MT_format/${direction}"

# 1. use sentencepiece (https://github.com/google/sentencepiece) to segment your corpus via BPE algorithm.
train_data_now=$train_data_dir/$srclang.tmp
python3 sentencepiece_preprocess.py $srclang $train_data_now

cp $train_data_dir/train.$direction.input $bpe_data_dir/train.$direction.$srclang
cp $train_data_dir/dev.$direction.input $bpe_data_dir/valid.$direction.$srclang
cp $train_data_dir/test.$direction.input $bpe_data_dir/test.$direction.$srclang

train_data_now=$train_data_dir/$tgtlang.tmp
python3 sentencepiece_preprocess.py $tgtlang $train_data_now

cp $train_data_dir/train.$direction.output $bpe_data_dir/train.$direction.$tgtlang
cp $train_data_dir/dev.$direction.output $bpe_data_dir/valid.$direction.$tgtlang
cp $train_data_dir/test.$direction.output $bpe_data_dir/test.$direction.$tgtlang

# 2. use fairseq (https://github.com/pytorch/fairseq) to construct **a shared BPE dictionary**. Then you will get two files: dict.src.txt and dict.tgt.txt

fairseq-preprocess \
     --source-lang="${direction}.${srclang}" \
     --target-lang="${direction}.${tgtlang}" \
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

cp data-bin/${direction}/dict.${direction}.${srclang}.txt ${bpe_data_dir}/dict.${srclang}.txt
cp data-bin/${direction}/dict.${direction}.${tgtlang}.txt ${bpe_data_dir}/dict.${tgtlang}.txt


fin="${data_dir}/${srclang}/${srclang}.txt"
fout="${bpe_data_dir}/dict.${srclang}.in.txt"
python3 make_bpe_character_dict.py $fin $fout

fin="${data_dir}/${tgtlang}/${tgtlang}.txt"
fout="${bpe_data_dir}/dict.${tgtlang}.in.txt"
python3 make_bpe_character_dict.py $fin $fout

# 4. put the train/dev/test and dict files together. and change DATA var in submit_drop script to the dir where your data is located.
# all the data are stored in $bpe_data_dir
# these data include:
# - train file
# - dev file
# - test file
# - dict.src.txt
# - dict.tgt.txt
# - dict.src.in.txt
# - dict.tgt.in.txt

# 5. train your DPE model via this command: sh submit_drop.sh SRC TGT seed epochs, where SRC is your source lang, tgt is your target lang, seed is a seed number and epochs is the maximum epochs.

./submit_drop.sh $srclang $tgtlang $seed 5

# 6. segment your target data via this command: sh find_seg.sh SRC TGT seed split, where split can be train, valid and test.

./find_seg.sh $srclang $tgtlang $seed train
./find_seg.sh $srclang $tgtlang $seed valid
./find_seg.sh $srclang $tgtlang $seed test





