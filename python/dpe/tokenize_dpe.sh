#!/bin/bash

srclang=Basque
tgtlang=English
seed=1

./preprocess.sh $srclang $tgtlang $seed
./preprocess.sh $tgtlang $srclang $seed
python3 convert_to_MT_format.py $srclang $tgtlang $seed

