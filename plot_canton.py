import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from index import Index

class Plot_canton:


	def __init__(self, abbreviation, canton):
		self.abbreviation = abbreviation
		self.canton = canton

		self.cycler = (
			cycler( color=['blue','green','orange','red','fuchsia'] )*
			cycler( linestyle=['-'])
			)

	def plot0(self, dat):
		plt.rc('axes', prop_cycle=self.cycler)
		with Index(dat,['canton']) as df_:
			df = df_.loc[self.abbreviation]
			df = df.reset_index()
			dates = df['date'].drop_duplicates()
			#dates_complete = complete_index(dates)
			dates_complete = dates
			df = df.set_index('date')
			plt.rc('axes', prop_cycle=self.cycler)
			fig = plt.figure()
			ax = fig.subplots()
			ax.plot(df['ncumul_conf'],label='Positive Testergebnisse')
			ax.plot(df['current_hosp'],label='Hospitalisierungen')
			ax.plot(df['ncumul_deceased'],label='Verstorben')
			ax.plot(df['current_icu'],label='Intensivstation')
			ax.plot(df['current_vent'],label='Beatmet')
			plt.yscale('log')
			plt.grid(which='both')
			plt.legend()
			ax.set_title(self.canton)
			ax.set_ylabel('Anzahl Fälle')
			fig.autofmt_xdate()
		return( fig )

	def plot1(self, dat):
		with Index(dat,['canton']) as df_:
			df = df_.loc[self.abbreviation]
			df = df.reset_index()
			dates = df['date'].drop_duplicates()
			#dates_complete = complete_index(dates)
			dates_complete = dates
			df = df.set_index('date')
			released = df.loc[:,'ncumul_released'].values
			released[np.isnan(released)] = 0
			deceased = df.loc[:,'ncumul_deceased'].values
			deceased[np.isnan(deceased)] = 0
			df.loc[:,'current_hosp'] = df.loc[:,'current_hosp'].values + released  + deceased
			df.loc[:,'current_vent'] = df.loc[:,'current_vent'].values + released + deceased
			df.loc[:,'current_icu'] = df.loc[:,'current_icu'].values + deceased
			df = (df.rolling('7D').mean()).diff()
			#df = df.mean().diff()
			fig = plt.figure()
			ax = fig.subplots()
			ax.plot(df['ncumul_conf'],label='Neue Positive Testergebnisse')
			ax.plot(df['current_hosp'],label='Neue Hospitalisierungen')
			#ax.plot(df['current_icu'],label='Intensivstation')
			#ax.plot(df['ncumul_deceased'],label='Beatmet')
			ax.plot(df['ncumul_deceased'],label='Verstorben')
			plt.yscale('log')
			plt.grid(which='both')
			plt.legend()
			ax.set_title(self.canton + ' (Durchschnittswerte der letzten 7 Tage)')
			ax.set_ylabel('Durchschnittswert pro Tag')
			fig.autofmt_xdate()
		return ( fig )
