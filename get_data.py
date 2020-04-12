#!/usr/bin/env python3
from subprocess import call
import os

repository = "https://github.com/openZH/covid_19.git"

def get_data( repository ):
    orig_dir = os.getcwd()
    try:
        os.chdir('data/covid_19')
        call( ['git', 'pull'] )
    except( FileNotFoundError ):
        try:
            os.chdir('data')
        except( FileNotFoundError ):
            os.makedirs('data')
        call( ['git','clone',repository] )
    os.chdir( orig_dir )

if __name__ == "__main__":
    get_data( respository )
