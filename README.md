# Maine CD2 2018 Election Re-creation

This project takes data from the 2018 election in Maine's Second Congressional District and recreates the ranked choice voting algorithm used to declare Jared Golden the Congressman-Elect.

Data acquired from: https://www.maine.gov/sos/cec/elec/results/results18.html#Nov6, current as of 12/16/2018

## Requirements

This project requires the pandas library and was developed using version 0.23.4.

## Running the program

### First things first

Before running the program, you first need to download and extract the data files. For Mac users, this can be accomplished by running get_files.sh at the terminal.

```
sh get_files.sh
```

For Windows or Linux users, the file can be downloaded from https://www.ben-fogarty.com/projects/maine-cd2-2018/maine-cd2-2018-ballots.tar.gz. After downloading the file, users must extract the archive into the same directory as the project.

This will download and unpack an archive with eight CSV files of ballots from the 2018 Maine CD2 election. This files were originally downloaded from https://www.maine.gov/sos/cec/elec/results/results18.html#Nov6 on 16 December 2018 and then convereted to CSVs for ease of use in pandas.

### Running the main program

The main program includes a command line interface that can be run as:

```
python3 rcv.py <optional int>
```

The optional integer argument present the opportunity for users to specify a random seed. This can be helpful for making results reproducable because in the case of ties the algorithm uses randomization to eliminate candidates. This is not strictly necessary for this election but may be useful for future uses.

Hence, run the program without a seed the proper command would be:

```
python3 rcv.py
```

And to run the program with my favorite seed, 11012017 (the date on which the Houston Astros won their first World Series title), the proper command would be:

```
python3 rcv.py 11012017
```

## Status and future work

Current status: Produces correct results

To-do: check documentation; code review

Ideas for future implementation: showing transfer of votes between candidates; tracking exhausted and/or invalid votes; batch elimination
