#!/usr/bin/env bash

echo "Please enter the language code or the name of the language you want to search for."
echo "Please note this is case sensitve."

read lang_search

echo "The fourth column(numerical value) contains the unique ID associated to bible.com"
echo -e "1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11"

result=$(grep $lang_search ../supplemental_bible.com_info/bible_versions.tsv)

echo "$result"
