import pandas as pd
import numpy as np
class Complete_indices:

	def __init__(self, dates, last_updates):
		self.dates = dates.copy()
		self.last_updates = last_updates.copy()

	def complete(self, col):
		#return( self.dates <= self.last_updates.loc[col].values[0])
		bool = self.dates <= self.last_updates.loc[col].values[0]
		arr = np.array(list(range(len(self.dates))))
		ret = arr[bool.tolist()]
		return( ret )

	def incomplete(self, col):
		#return( self.dates <= self.last_updates.loc[col].values[0])
		bool = self.dates >= self.last_updates.loc[col].values[0]
		arr = np.array(list(range(len(self.dates))))
		ret = arr[bool.tolist()]
		return( ret )
