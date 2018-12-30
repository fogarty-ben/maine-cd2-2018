'''
Maine 2018 2nd Congressional District Re-creation

Ben Fogarty

All references to Maine election law from:
https://www.maine.gov/sos/cec/elec/upcoming/pdf/250c535-2018-230-complete.pdf
'''

import pandas as pd

#data files downloaded from the maine sos website
NAN = float('nan')
EXHAUSTED = 'exhausted'
OVERVOTE = 'overvote'
UNDERVOTE = 'undervote'
SKIP = 'skip'
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
NEXT_CHOICE = {'first_choice': 'second_choice',
               'second_choice': 'third_choice',
               'third_choice': 'fourth_choice',
               'fourth_choice': 'fifth_choice',
               'fifth_choice': EXHAUSTED}

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
    ballot[CHOICE_FIELDS[-1]] = NAN

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
    ballot[CHOICE_FIELDS[ind] : CHOICE_FIELDS[-1]] = NAN

    return ballot



def process_ballot(ballot):
    '''
    Handles overvotes, undervotes, and duplicate rankings for a single candidate
    in accordance with Maine election law in Section 4.2.B.

    Inputs:
        ballot (Pandas series): one ballot from the election

    Returns: Pandas series
    '''
    #process overvotes
    candidates_voted_for = set()
    for i, col in enumerate(CHOICE_FIELDS):
        #process overvotes
        if ballot[col] == OVERVOTE:
            ballot = exhaust_beyond(ballot, i)
            break
        #process duplicate rankings
        elif ballot[col] in candidates_voted_for:
                ballot[col] = SKIP
        #process undervotes
        elif ballot[col] == UNDERVOTE:
            if i == len(CHOICE_FIELDS) - 1 or \
            ballot[CHOICE_FIELDS[i + 1]] == UNDERVOTE:
                ballot = exhaust_beyond(ballot, i)
            else:
                ballot[col] = SKIP
        candidates_voted_for.add(ballot[col])
    #remove skips
    for i in range(len(CHOICE_FIELDS) - 1, -1, -1):
        col = CHOICE_FIELDS[i]
        if ballot[col] == SKIP:
            if i == len(CHOICE_FIELDS) - 1:
                ballot[col] = NAN
            else:
                ballot = move_forward_one_choice(ballot, i)

    return ballot


def read_and_process_ballots(filepath):
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
    col_names = {'cast_vote_record': 'vote_id',
                 'Precinct': 'precinct',
                 'Ballot Style': 'ballot_style',
                 'Rep. to Congress 1st Choice District 2': 'first_choice',
                 'Rep. to Congress 2nd Choice District 2': 'second_choice',
                 'Rep. to Congress 3rd Choice District 2': 'third_choice',
                 'Rep. to Congress 4th Choice District 2': 'fourth_choice',
                 'Rep. to Congress 5th Choice District 2': 'fifth_choice',
                }
    fix_entries = {'REP Poliquin, Bruce (5931)': 'REP Poliquin, Bruce',
                   'DEM Golden, Jared F. (5471)': 'DEM Golden, Jared F.'}

    try:
        dataframe = pd.read_excel(filepath, index_col="Cast Vote Record",
                                  dtype=col_types)
        dataframe.rename(col_names, axis=1, inplace=True)
        dataframe['first_choice'] = dataframe.first_choice.replace(fix_entries)
        dataframe = dataframe.apply(process_ballot, axis=1)
        dataframe['active_choice'] = 'first_choice'
        dataframe[dataframe.first_choice == NAN] = EXHAUSTED
    except FileNotFoundError:
        print("No file found at", filepath + "!")

    return dataframe


def get_active_choice(ballots):
    '''
    Returns which candidate each ballot is active for.

    Inputs:
        ballots (Pandas dataframe): all the ballots in the election

    Returns: Panda series
    '''
    active_ballots = ballots[ballots.active_choice != EXHAUSTED]
    return active_ballots.apply(lambda x: x[x.active_choice], axis=1)


def tabulate_one_round(ballots):
    '''
    Calculate the vote totals for all candidates in one round finds eliminate
    and candidates below the threshold.

    Inputs:
        ballots (Pandas dataframe): all the ballots in the election

    Returns: tuple of Pandas series, string where the series is the results of
        the round and the string is the candidate to be eliminated
    '''
    vote_tally = get_active_choice(ballots) \
                 .value_counts() \
                 .transform(lambda x: x / sum(x) * 100)
    eliminated_candidate = vote_tally.index[-1]
    
    return (vote_tally, eliminated_candidate)

def advance_round(ballots, active_candidates):
    '''
    Updates active choice on ballots after a candidate is eliminated

    Inputs:
        ballots (Pandas dataframe): all the ballots in the election
        active_candidates (set): uneliminated candidates
    '''
    continue_updating = True
    while continue_updating:
        to_update = ~ get_active_choice(ballots).isin(active_candidates)
        ballots.loc[to_update, 'active_choice'] = ballots[to_update].\
            active_choice.map(NEXT_CHOICE)
        tally = get_active_choice(ballots)
        candidates_with_votes = set(tally)
        if len(candidates_with_votes - active_candidates)  == 0:
            continue_updating = False

    return ballots

