#!/usr/bin/env python3

import pandas as pd
import numpy as np
from index import Index

def missing():
	dat = pd.read_csv('data/ch_full.csv',
		parse_dates = ['date'])
	cantons = dat['canton'].drop_duplicates()
	dates = dat['date'].drop_duplicates()
	cols = dat.columns[2:]
	cols.set_names('column', inplace = True)
	dat['date']
	last_update = pd.DataFrame(index=cantons, columns=cols, dtype='datetime64')


	total_last_update = pd.DataFrame(index=cols, columns =['date'], dtype='datetime64')

	for col in list(cols):
		total_last_update.loc[col] = np.datetime64('2100-01-01')

	with Index(dat, 'canton') as df:
		for canton in cantons:
			for col in cols:
				series = df.loc[canton,col].values
				i = len(dates) - 1
				while np.isnan(series[i]):
					if i >= 0:
						i = i - 1
					else:
						break
				if i >= 0:
					last_update.loc[canton,col] = dates.iloc[i]
					if dates.iloc[i] < total_last_update.loc[col].values:
						total_last_update.loc[col] = dates.iloc[i]
				else:
					last_update.loc[canton,col] = pd.NaT

	for col in list(cols):
		if total_last_update.loc[col].values == '2100-01-01':
			total_last_update.loc[col] = pd.NaT

	last_update.to_csv('data/ch_last_updated.csv')
	total_last_update.to_csv('data/ch_last_update_total.csv')

if __name__ == "__main__":
	missing()
