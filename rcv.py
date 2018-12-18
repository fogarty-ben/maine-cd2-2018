'''
Maine 2018 2nd Congressional District Re-creation

Ben Fogarty

All references to Maine election law from:
https://www.maine.gov/sos/cec/elec/upcoming/pdf/250c535-2018-230-complete.pdf
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
CHOICE_FIELDS = ['first_choice', 'second_choice', 'third_choice',
				 'fourth_choice', 'fifth_choice']

def compute_election_results():
	'''
	Computes the results of the election
	'''


def move_forward_one_choice(ballot, ind):
	'''
	Moves all the choices at or after index ind forward by one ranking.

	Inputs:
		ballot (Pandas series): one ballot from the election
		ind (int): the index to start the process at

	Returns: Pandas series
	'''
	ballot[CHOICE_FIELDS[ind] : CHOICE_FIELDS[-2]] = \
		ballot[CHOICE_FIELDS[ind + 1] : CHOICE_FIELDS[-1]]
	ballot[CHOICE_FIELDS[-1]] = float('nan')

	return ballot


def exhaust_beyond(ballot, ind):
	'''
	Replaces all choices at or after index ind with NaN, representing that the
	ballot is exhausted at these choices

	Inputs:
		ballot (Pandas series): one ballot from the election
		ind (int): the index to start the process at

	Returns: Pandas series
	'''
	ballot[CHOICE_FIELDS[ind] : CHOICE_FIELDS[-1]] = float('nan')

	return ballot



def process_ballot(ballot):
	'''
	Handles overvotes, undervotes, and duplicate rankings for a single candidate
	in accordance with Maine election law in Section 4.2.B.

	Inputs:
		ballot (Pandas series): one ballot from the election

	Returns: Pandas series
	'''
	candidates_voted_for = set()
	for i, col in enumerate(CHOICE_FIELDS):
		#process overvotes
		if ballot[col] == 'overvote':
			ballot = exhaust_beyond(ballot, i)
			break
		#process undervotes
		elif ballot[col] == 'undervote':
			if i == len(CHOICE_FIELDS) - 1 or \
			ballot[CHOICE_FIELDS[i + 1]] == 'undervote':
				ballot = exhaust_beyond(ballot, i)
				break
			else:
				ballot = move_forward_one_choice(ballot, i)
		#process duplicate rankings
		if ballot[col] in candidates_voted_for:
			if i == len(CHOICE_FIELDS) - 1:
				ballot[CHOICE_FIELDS[i]] == float('nan')
			else:
				ballot = move_forward_one_choice(ballot, i)	
		else:
			candidates_voted_for.add(ballot[col])

	return ballot


def read_and_process_dataset(filepath):
	'''
	Read in a dataset from file and process it.

	Inputs:
		filepath (string): the relative location of the file

	Returns: pandas dataframe
	'''
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
				  'Rep. to Congress 4th Choice District 2': 'fourth_choice',
				  'Rep. to Congress 5th Choice District 2': 'fifth_choice',
				 }

	try:
		df = pd.read_excel(filepath, index_col="Cast Vote Record",
						   dtypes=col_types)
		df.rename(col_names, axis=1, inplace=True)
		df = df.apply(process_ballot, axis=1)
	except FileNotFoundError:
		print("No file found at", filepath + "!")

	return df
