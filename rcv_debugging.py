'''
Debugging helper functions for rcv module

Ben Fogarty
'''

import pandas as pd
import rcv


def import_one_ballotset(dataset_name='digital1'):
    '''
    Imports one set of ballots.

    Inputs:
        dataset_name (string): name or path of the dataset to be imported

    Returns: Pandas DataFrame
    '''
    if dataset_name in rcv.DATA_FILE_LOCS:
        file_loc = rcv.DATA_FILE_LOCS[dataset_name]
    else:
        file_loc = 'data/' + dataset_name

    return rcv.read_and_process_ballots(file_loc)

    