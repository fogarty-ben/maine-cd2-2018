'''
Maine 2018 2nd Congressional District Re-creation

Ben Fogarty
'''

import pandas as pd

#data files downloaded from the maine sos website
DATA_FILE_LOCS = {'digital1': 'data/NOV18CVRExportFINAL1.xlsx',
				  'digital2': 'data/NOV18CVRExportFINAL2.xlsx',
				  'digital3': 'data/NOV18CVRExportFINAL3.xlsx',
				  'uocava4': 'data/UOCAVA-FINALRepCD2.xlsx',
				  'uocava5': 'data/UOCAVA-AUX-CVRRepCD2.xlsx',
				  'uocava6': 'data/UOCAVA2CVRRepCD2.xlsx',
				  'noscan7': 'data/AUXCVRProofedCVR95RepCD2.xlsx',
				  'digital8': 'data/RepCD2-8final.xlsx'
				 }

def compute_election_results():
	'''
	Computes the results of the election
	'''

def read_and_process_dataset(filepath):
	'''
	Read in a dataset from file and process it.

	Inputs:
		filepath (string): the relative location of the file

	Returns: pandas dataframe
	'''
	try:
		col_types = {'Cast Vote Record': int,
					 'Precinct': 'category',
					 'Ballot Style': 'category',
					 'Rep. to Congress 1st Choice District 2': 'category',
					 'Rep. to Congress 2nd Choice District 2': 'category',
					 'Rep. to Congress 3rd Choice District 2': 'category',
					 'Rep. to Congress 4th Choice District 2': 'category',
					 'Rep. to Congress 5th Choice District 2': 'category',
					 }
		col_names =  {'cast_vote_record': 'vote_id',
					  'Precinct': 'precinct',
					  'Ballot Style': 'ballot_style',
					  'Rep. to Congress 1st Choice District 2': 'first_choice',
					  'Rep. to Congress 2nd Choice District 2': 'second_choice',
					  'Rep. to Congress 3rd Choice District 2': 'third_choice',
					  'Rep. to Congress 1st Choice District 2': 'fourth_choice',
					  'Rep. to Congress 4th Choice District 2': 'fifth_choice',
					 }
		df = pd.read_excel(filepath, index_col="Cast Vote Record",
						   dtypes=col_types, names=col_names)
		df.rename(col_names)
		df['active_choice'] = df.first_choice
		df['active_rank'] = 1
		df['active_rank'] = df.active_rank.astype('category')
	except File Not Found:
		print("No file found at", filepath + "!")

	return df
