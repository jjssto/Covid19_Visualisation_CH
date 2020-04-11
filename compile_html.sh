#!/usr/bin/env bash

TMP="analyse_tmp.pmd"

cd data/covid_19
git pull
cd ../..

./modify_data.py
sed "s/\[Timestamp\]/$(date)/g" analyse.pmd > $TMP

pweave -f md2html -F figures -o corona_info.html $TMP
