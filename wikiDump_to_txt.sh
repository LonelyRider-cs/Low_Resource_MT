#!/usr/bin/env bash

echo "Please enter the wikipedia xml file you would like to convert:"

read file_name

echo $file_name

python wikipedia_dump_extractor.py --json $file_name

wait

python wikiDump_convert.py $file_name

wait

rm -r text/*
rmdir text
