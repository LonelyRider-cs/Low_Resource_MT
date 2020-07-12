#!/bin/bash

SRC=$1
TGT=$2
seed=$3
subset=$4

DATA=data_bpe/$SRC-$TGT
MPATH=checkpoints/$SRC-$TGT/seed$seed
#MPATH=checkpoints/bpe_dropout_post/$SRC-$TGT/seed$seed
#MPATH=checkpoints/pretrain/$SRC-$TGT/big/seed$seed
CKPT=$MPATH/checkpoint_best.pt
TASK=translation
BATCH=35
BEAM=5
TGTOUTPUT=$MPATH/$subset.$SRC-$TGT.$TGT

echo "... segmenting ${TGT} ${subset} data ..."

python3 ./find_seg.py $DATA \
        --task $TASK \
        --segment \
        --raw-text \
        -s $SRC \
        -t $TGT \
        --path $CKPT \
        --batch-size $BATCH \
        --beam $BEAM \
        --max-len-b 100 \
        --gen-subset $subset > $TGTOUTPUT

