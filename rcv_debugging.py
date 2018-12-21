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
        dataset_name (string): name of the dataset to be imported

    Returns: Pandas DataFrame
    '''

    return rcv.read_and_process_ballots(rcv.DATA_FILE_LOCS[dataset_name])

    