#!/usr/bin/env bash

TMP="analyse_tmp.pmd"

cd data/covid_19
git pull
cd ../..

./modify_data.py
./missing.py

sed "s/\[Timestamp\]/$(date)/g" analyse.pmd > $TMP

pweave -f markdown -i noweb -k python3 -o doc/corona_visualisation.md $TMP


