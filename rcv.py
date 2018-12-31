'''
Maine 2018 2nd Congressional District Re-creation

Ben Fogarty

All references to Maine election law from:
https://www.maine.gov/sos/cec/elec/upcoming/pdf/250c535-2018-230-complete.pdf
'''

import pandas as pd
import random

#data files downloaded from the maine sos website
NAN = float('nan')
EXHAUSTED = 'exhausted'
OVERVOTE = 'overvote'
UNDERVOTE = 'undervote'
SKIP = 'skip'
DATA_FILE_LOCS = {'digital1': 'data/NOV18CVRExportFINAL1.csv',
                  'digital2': 'data/NOV18CVRExportFINAL2.csv',
                  'digital3': 'data/NOV18CVRExportFINAL3.csv',
                  'uocava4': 'data/UOCAVA-FINALRepCD2.csv',
                  'uocava5': 'data/UOCAVA-AUX-CVRRepCD2.csv',
                  'uocava6': 'data/UOCAVA2CVRRepCD2.csv',
                  'noscan7': 'data/AUXCVRProofedCVR95RepCD2.csv',
                  'digital8': 'data/RepCD2-8final.csv'
                 }
CHOICE_FIELDS = ['first_choice', 'second_choice', 'third_choice',
                 'fourth_choice', 'fifth_choice']
NEXT_CHOICE = {'first_choice': 'second_choice',
               'second_choice': 'third_choice',
               'third_choice': 'fourth_choice',
               'fourth_choice': 'fifth_choice',
               'fifth_choice': EXHAUSTED,
               EXHAUSTED: EXHAUSTED}


def compute_election_results(seed=11012017):
    '''
    Computes the results of the election
    '''
    
    random.seed(seed)
    ballots = pd.DataFrame()
    n_files = len(DATA_FILE_LOCS)
    current_file = 1
    for path in DATA_FILE_LOCS.values():
        print('Loading ballots file {}/{}!'.format(current_file, n_files))
        ballots = ballots.append(read_and_process_ballots(path))
        current_file += 1
    print('All ballots loaded!')
    print()
    
    #ballots = read_and_process_ballots('data/mini.csv')

    active_candidates = set(ballots.first_choice.values)

    found_winner = False
    n_rounds = 0
    while not found_winner:
        n_rounds += 1
        print("Round #{}:".format(n_rounds))
        results = tabulate_one_round(ballots)
        if results.iloc[0]['% Votes'] > 50:
            print("{} was elected in round {}.".format(results.index[0],
                                                       n_rounds))
            print(results)
            found_winner = True
        else:
            to_eliminate = find_candidate_to_eliminate(results)
            print('{} was eliminated in round {}.'.format(to_eliminate,
                n_rounds))
            print(results)
            print()
            active_candidates.remove(to_eliminate)
            advance_round(ballots, active_candidates)
            

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
                 'Rep. to Congress 5th Choice District 2': 'category'
                 }
    col_names = {'cast_vote_record': 'vote_id',
                 'Precinct': 'precinct',
                 'Ballot Style': 'ballot_style',
                 'Rep. to Congress 1st Choice District 2': 'first_choice',
                 'Rep. to Congress 2nd Choice District 2': 'second_choice',
                 'Rep. to Congress 3rd Choice District 2': 'third_choice',
                 'Rep. to Congress 4th Choice District 2': 'fourth_choice',
                 'Rep. to Congress 5th Choice District 2': 'fifth_choice',
                 'Rep. to Congress District 2 1st Choice': 'first_choice',
                 'Rep. to Congress District 2 2nd Choice': 'second_choice',
                 'Rep. to Congress District 2 3rd Choice': 'third_choice',
                 'Rep. to Congress District 2 4th Choice': 'fourth_choice',
                 'Rep. to Congress District 2 5th Choice': 'fifth_choice',
                }
    fix_entries = {'REP Poliquin, Bruce (5931)': 'REP Poliquin, Bruce',
                   'DEM Golden, Jared F. (5471)': 'DEM Golden, Jared F.',
                   'DEM Golden, Jared F. ': 'DEM Golden, Jared F.'}

    try:
        dataframe = pd.read_csv(filepath, index_col="Cast Vote Record",
                                  dtype=col_types)
        dataframe.rename(col_names, axis=1, inplace=True)
        for choice in CHOICE_FIELDS:
            dataframe[choice] = dataframe[choice].replace(fix_entries)
        dataframe = dataframe.apply(process_ballot, axis=1)
        dataframe['active_choice'] = 'first_choice'
        dataframe[dataframe.first_choice == NAN] = EXHAUSTED
    except FileNotFoundError:
        print("No file found at", filepath + "!")

    return dataframe


def get_active_choice(ballot):
    '''
    Returns which candidate each ballot is active for.

    Inputs:
        ballot (Pandas series): one ballot from the election

    Returns: Panda series
    '''
    if ballot.active_choice == EXHAUSTED:
        return NAN
    else:
        return ballot[ballot.active_choice]


def tabulate_one_round(ballots):
    '''
    Calculate the vote totals for all candidates in one round finds eliminate
    and candidates below the threshold.

    Inputs:
        ballots (Pandas dataframe): all the ballots in the election

    Returns: tuple of Pandas series, Panda series string where the series is the
        results of the round and the string is the candidate to be eliminated
    '''
    active_choices = ballots.apply(get_active_choice, axis=1)
    vote_cts = active_choices.value_counts()
    vote_pcts = active_choices[active_choices != NAN]\
                .value_counts()\
                .transform(lambda x: x / sum(x) * 100)
    results = pd.concat([vote_cts, vote_pcts], axis=1)\
                .rename(mapper={0: '# Votes', 1: "% Votes"}, axis=1)\
                .sort_values(by="# Votes", ascending=False, axis=0)
    
    return results


def find_candidate_to_eliminate(results):
    '''
    Finds the candidate(s) with the lowest vote total after a round. If two or
    more candidate are tied for the lowest vote total, then a candidate to
    eliminate is chosen randomly.

    Inputs:
        resuts(Pandas dataframe): the results of one round in the election

    Returns: string, the name of the candidate to be eliminated
    '''
    min_votes = results.iloc[-1]['# Votes']
    min_candidates = results[results['# Votes'] == min_votes].index.tolist()

    eliminated_candidate = random.sample(min_candidates, 1)[0]
    if len(min_candidates) > 1:
        print(min_candidates, "all tied for lowest vote total in this round.")

    return eliminated_candidate


def find_high_valid_choice(ballot, active_candidates):
    '''
    Finds the highest on a ballot containing a still active candidate. To be
    used recursively.

    Inputs:
        ballot (Pandas series): one ballot from the election
        active_candidates (set): uneliminated candidates
    
    Returns: Pandas series
    '''
    ballot['active_choice'] = NEXT_CHOICE[ballot.active_choice]
    if ballot.active_choice == EXHAUSTED or \
    ballot[ballot.active_choice] in active_candidates:
        return ballot    

    return find_high_valid_choice(ballot, active_candidates)


def advance_round(ballots, active_candidates):
    '''
    Updates active choice on ballots after a candidate is eliminated

    Inputs:
        ballots (Pandas dataframe): all the ballots in the election
        active_candidates (set): uneliminated candidates
    '''
    to_update = ~ ballots.apply(get_active_choice, axis=1) \
                         .isin(active_candidates)
    ballots.loc[to_update] = ballots[to_update].apply(find_high_valid_choice,
        axis=1, args=(active_candidates,))

    return ballots

