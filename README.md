# Maine CD2 2018 Election Re-creation

This project takes data from the 2018 election in Maine's Second Congressional District and recreates the ranked choice voting algorithm used to declare Jared Golden the Congressman-Elect. This election was the first in Maine to use ranked choice voting and is a particularly interesting test case for this algorithm as the winner of the election after realignment differed from the winner of the election based on the first round alone.

All data used in the project was acquired from the Maine Secretary of State's website at https://www.maine.gov/sos/cec/elec/results/results18.html#Nov6.

## Requirements

This project was developed using Python 3.7.3 and has the following dependencies:

| Package         | Version |
| --------------- | ------- |
| numpy           | 1.18.1  |
| pandas          | 1.0.1   |
| python-dateutil | 2.8.1   |
| pytz            | 2019.3  | 
| setuptools      | 40.8.0  |
| six             | 1.14.0  |
| xlrd            | 1.2.0   |

All dependcies are saved in `requirements.txt` and can be installed with the following command.

```
pip3 install -r requirements.txt
```

## Running the program

### First things first

Before running the program, you first need to download the data files. For MacOS users, this can be accomplished by running get_files.sh at the terminal.

```
sh get_files.sh
```

For Windows or Linux users, the files can be downloaded from https://www.maine.gov/sos/cec/elec/results/results18.html#Nov6. Download all eight spreadsheets under the `Representative to Congress -  District 2 (FINAL)` header.

Each spreadsheet contains a set of ballots cast in the 2018 Maine CD2 election. Each row is one ballot and contains that ballot's full ranking of candidates.

### Running the main program

The main program includes a command line interface that can be run as:

```
python3 rcv.py filpath <optional int>
```

- The first argument is the path to the directory containing all of the cast ballot records from the Maine SOS website; relative or absolute paths are acceptable. 
- The optional integer argument presents the opportunity for users to specify a random seed. This can be helpful for making results reproducable because in the case of ties the algorithm uses randomization to eliminate candidates. This is not strictly necessary for this election as the algorithm does not encouter a tie, but it may be useful for other, future elections.

## Status and possible future work

Current status: Complete and producing correct results for the Maine 2018 election

Ideas for future implementation: showing transfer of votes between candidates; tracking exhausted and/or invalid votes; batch elimination; further testing with different cast ballots records
