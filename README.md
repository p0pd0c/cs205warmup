# NeuralTeam Query Engine

## Description

A simple query engine that allows a user to query information about an IMDb movie dataset

The set, built by the team, contains a selection of the top 250 movies and their directors from IMDb.

[DB SCHEMA AND DATA](https://docs.google.com/spreadsheets/d/10uNZty7Ix6n4S_ww2qhkvcJ7jfikw8rN0CeShY-WSuE/edit?usp=sharing)

This project is for our cs205 (Software Engineering) course at UVM with professor Jason Hibbler.

[PRESENTATION](https://docs.google.com/presentation/d/12EugwYQW6lgqt0djMILuD6K_ihHnTbOqu1pTB_NQdDw/edit?usp=sharing)

## Requirements
Must have python 3.9 or greater

## Running the program
Colocate the csv files with the main, parser, and sqlinterface python scripts

Run the following in your command line to start the query shell:
```
python main.py
```

### Interacting with the shell
While the program is running, try giving some commands to the query engine...
It will show you a list of commands.

Before the user can query the data, they must first issue:
```
load data
```
Otherwise the shell will tell the user that the database hasn't been initialized. 

### Example Queries

For example, the net profit query:
```
net profit director "Christopher Nolan"
```
Would yield the amount of money generated by Christopher Nolan after the budgets for all his movies are subtracted. 

What if you wanted to know who the most successful director is?
```
most successful director
```

And if you wanted to know what movies are by that director?
```
which movies by "Christopher Nolan"
```

There are many more commands supported by the query engine, and if you ever forget, you can activate the help menu at any time by entering any invalid command
```
help me please!
```

And to quit the shell
```
quit
```
