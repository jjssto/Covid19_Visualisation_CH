#!/usr/bin/env python3

import pandas as pd
import numpy as np
from index import Index


dat = pd.read_csv('data/covid_19/COVID19_Fallzahlen_CH_total_v2.csv',
        parse_dates = ['date','time']
        #date_parser = dateparse,
        )
dat.rename(
    columns={'abbreviation_canton_and_fl': 'canton'},
    inplace = True
)

# Fürstentum Lichtenstein endat_ch = pd.concat(
dat = dat[dat['canton'] != 'FL' ]
# remove columns that don't contain data
cols = dat.columns[[0,1,2,3,4,5,6,7,8,9,10]]
dat = dat.loc[:,cols]

dat.set_index(['date','canton','time'], inplace = True)
dat.sort_index(inplace = True)
dat.to_csv('data/ch.csv')

dat.reset_index(inplace=True)
first_day = dat['date'].min()
last_day = dat['date'].max()
cantons = list(dat['canton'].drop_duplicates())
#cantons.sort()
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

df = dat.set_index(['date','canton','time'])
index_ = df.index
index = []
for timestamp in index_:
    index.append( (timestamp[0],timestamp[1]) )
for ind in df.index:
    dat_inter_raw.loc[(ind[0],ind[1])] = df.loc[ind]


dat_inter_raw.loc[:,cols] = dat_inter_raw.loc[:,cols].astype('float')
dat_inter_raw.reset_index(inplace = True)
# interpolated

dat_inter_raw.set_index('canton', inplace = True)
dat_inter = dat_inter_raw.copy()
cols_date = ['date']
cols_date.extend(cols)
for canton in cantons:
#    canton = 'LU'
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
#    canton = 'LU'
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

cantons = dat_ffill['canton'].drop_duplicates()
cases_cantons = pd.DataFrame( index = cantons, columns = ['cases'])
deaths_cantons = pd.DataFrame( index = cantons, columns = ['deaths'])
dat_ffill
with Index(dat_ffill, 'canton') as df:
    for canton in cantons:
        series_cases = df['ncumul_conf'].loc[canton].values
        series_deaths = df['ncumul_deceased'].loc[canton].values

        i = len(series_cases) - 1
        while np.isnan(series_cases[i]):
            if i >= 0:
                i = i - 1
            else:
                break
        cases_cantons.loc[canton] = series_cases[i]

        i = len(series_deaths) - 1
        while np.isnan(series_deaths[i]):
            if i >= 0:
                i = i - 1
            else:
                break  
        deaths_cantons.loc[canton] = series_deaths[i]

deaths_cantons
dat.to_csv('data/ch.csv', index = False )
dat_inter_raw.to_csv('data/ch_full.csv', index = False)
dat_inter.to_csv('data/ch_interpolated.csv', index = False)
dat_ffill.to_csv('data/ch_ffill.csv', index = False )
cases_cantons.to_csv('data/ch_cases_cantons.csv')
deaths_cantons.to_csv('data/ch_deaths_cantons.csv')
