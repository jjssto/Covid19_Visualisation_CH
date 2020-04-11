#!/usr/bin/env python3

import pandas as pd
import numpy as np
from index import Index


dat = pd.read_csv('data/covid_19/COVID19_Fallzahlen_CH_total_v2.csv',
    	parse_dates = ['date']
    	#date_parser = dateparse,
    	)
dat.rename(
    columns={'abbreviation_canton_and_fl': 'canton'},
    inplace = True
)

# Fürstentum Lichtenstein endat_ch = pd.concat(
dat = dat[dat['canton'] != 'FL' ]
dat

# remove columns that don't contain data
cols = dat.columns[[0,2,3,4,5,6,7,8,9,10]]
dat = dat.loc[:,cols]
dat

dat.to_csv('data/ch.cvs')


first_day = dat['date'].min()
last_day = dat['date'].max()
cantons = dat['canton'].drop_duplicates()
cols = dat.columns[2:]
date_range = pd.date_range(
	start = first_day,
	end = last_day
)
date_canton = pd.MultiIndex.from_product(
	[date_range, cantons],
	names = ['date','canton']
)
dat_inter_raw = pd.DataFrame(
	index = date_canton,
	columns = cols
)
with Index(dat, ['date','canton']) as df:
	for ind in dat_inter_raw.index:
		if ind in df.index:
			dat_inter_raw.loc[ind] = df.loc[ind].values
dat_inter_raw.loc[:,cols] = dat_inter_raw.loc[:,cols].astype('float')
dat_inter_raw.reset_index(inplace = True)

# interpolated

dat_inter_raw.set_index('canton', inplace = True)
dat_inter = dat_inter_raw.copy()
cols_date = ['date']
cols_date.extend(cols)
for canton in cantons:
#	canton = 'LU'
	df_sub = dat_inter_raw.loc[canton]
	df_sub.reset_index( inplace = True )
	df_sub = df_sub.loc[:,cols_date]
	df_sub.set_index( 'date', inplace = True)
	#df_sub.interpolate( method='spline',order=1, inplace = True)
	df_sub = df_sub.interpolate( method='time')
	df_sub.reset_index( inplace = True )
	dat_inter.loc[canton,cols] = df_sub.loc[:,cols].values

dat_inter.reset_index( inplace = True )
dat_inter_raw.reset_index( inplace = True )


# forward fill

dat_inter_raw.set_index('canton', inplace = True)
dat_ffill = dat_inter_raw.copy()
cols_date = ['date']
cols_date.extend(cols)
for canton in cantons:
#	canton = 'LU'
	df_sub = dat_inter_raw.loc[canton]
	df_sub.reset_index( inplace = True )
	df_sub = df_sub.loc[:,cols_date]
	df_sub.set_index( 'date', inplace = True)
	df_sub = df_sub.fillna( method = 'ffill')
	df_sub
	df_sub.reset_index( inplace = True )
	dat_ffill.loc[canton,cols] = df_sub.loc[:,cols].values

dat_ffill.reset_index( inplace = True )
dat_inter_raw.reset_index( inplace = True )


dat.to_csv('data/ch.csv', index = False )
dat_inter_raw.to_csv('data/ch_full.csv', index = False)
dat_inter.to_csv('data/ch_interpolated.csv', index = False)
dat_ffill.to_csv('data/ch_ffill.csv', index = False )
