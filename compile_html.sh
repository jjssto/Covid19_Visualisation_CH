#!/usr/bin/env bash

TMP="analyse_tmp.pmd"

cd /var/www/python/data/covid_19
git pull
cd ../..

./modify_data.py
sed "s/\[Timestamp\]/$(date)/g" analyse.pmd > $TMP

pweave -f md2html -F figures -o corona_info.html $TMP

cp corona_info.html ../html/documents/
cp figures/* ../html/documents/figures/
chmod go+r ../html/documents/corona_info.html
chmod go+r ../html/documents/figures/*
