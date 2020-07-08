#!/usr/bin/env bash

echo "Please enter the wikipedia xml file you would like to convert:"

read file_name

echo $file_name

python ../python/wikipedia_dump_extractor.py --json ../all_wikipedia_dumps/$file_name

wait

python ../python/wikiDump_convert.py ../all_wikipedia_dumps/$file_name

wait

rm -r text/*
rmdir text
