#!/usr/bin/env python3
import missing, modify_data, get_data
from tempfile import NamedTemporaryFile
import pweave
import re, os, shutil
from datetime import datetime
from subprocess import call

input_file = 'analyse.pmd'
output_file = 'index.html'
tracking_file = 'matomo.html'
repository = 'data/covid_19/COVID19_Fallzahlen_CH_total_v2.csv'

class Create_html:
    # patters for repalcement using regular expressions
    pattern_update = re.compile(r'<p>Update:.*<br/>')
    pattern_geaendert = re.compile(r'Geändert:.*</p>')

    def __init__(self, input_file, output_file, tracking_file, repository):
        self.input_file = input_file
        self.output_file = output_file
        self.tracking_file = tracking_file
        self.repository = repository

        timestamp = datetime.today()
        timestring = timestamp.strftime('%Y-%m-%d -- %H:%M')
        timestring
        self.subst_update = '<p>Update: ' + timestring + '<br/>'
        self.subst_geaendert = 'Geändert: ' + timestring + '</p>'

    def create_html( self ):
        # timestamp from source file
        timestamp_source = os.stat( self.repository ).st_mtime
        # timesampt from html file
        try:
            timestamp_html = os.stat( self.output_file ).st_mtime
        except( FileNotFoundError ):
            timestamp_html = datetime(2000,1,1)

        if timestamp_source > timestamp_html:
            self.replace_timestamps_source()
            # bring the data in the right form
            modify_data.modify_data()
            missing.missing()
            pweave.weave(
                file = self.input_file,
                doctype = 'md2html',
                output = self.output_file
                )
            self.place_tracking_code()
        else:
            self.replace_timestamps_output()

    def replace_timestamps_source( self ):
        tmp_file = NamedTemporaryFile( 'w', delete = False )
        f = open( self.input_file, 'r')
        for line in f:
            tmp_file.write(
                self.pattern_update.sub( self.subst_update,
                    self.pattern_geaendert.sub( self.subst_geaendert,
                        line )
                    )
                )
        f.close()
        tmp_file.close()
        shutil.copystat( self.input_file, tmp_file.name)
        shutil.move( tmp_file.name, self.input_file )


    def replace_timestamps_output( self ):
        tmp_file = NamedTemporaryFile( 'w', delete = False )
        f = open( self.output_file, 'r')
        for line in f:
            tmp_file.write( self.pattern_update.sub( self.subst_update,
                line) )
        f.close()
        tmp_file.close()
        shutil.copystat( self.output_file, tmp_file.name)
        shutil.move( tmp_file.name, self.output_file )

    def place_tracking_code( self ):
        tmp_file = NamedTemporaryFile( 'w', delete = False )
        f = open( self.output_file, 'r')
        t = open( self.tracking_file, 'r')
        for line in f:
            if re.match(r'.*HEAD.*',line) is not None:
                tmp_file.write( line )
                for line_ in t:
                    tmp_file.write(line_)
            else:
                tmp_file.write( line )
        f.close()
        t.close()
        tmp_file.close()
        shutil.copystat( self.output_file, tmp_file.name)
        shutil.move( tmp_file.name, self.output_file )



if __name__ == "__main__":
    get_data.get_data( repository)
    call(['git','pull'])
    html_creator = Create_html( input_file, output_file, tracking_file, repository )
    html_creator.create_html()
    try:
        call(['git','add','figure/*.png'])
    except:
        pass
    call(['git','commit','-a','-m "Automatic Update"'])
    call(['git','push'])
