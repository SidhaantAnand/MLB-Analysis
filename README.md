# ECE 356 Project

ECE 356 Database Project, using MLB data from 2015 to 2018.

## Running the client application

To run, use command `python MLB.py`

### Requirements

This program requires Python 3.7.4 to run. Additionally, the following packages need to be installed

* matplotlib 3.1.3
* mysql-connector-python 8.0.23
* numpy 1.18.1
* pandas 1.0.3
* pandocfilters 1.4.2
* PyMySQL 1.0.2
* scikit-learn 0.22.1
* scipy 1.4.1
* seaborn 0.10.0
* sklearn 0.0
* SQLAlchemy 1.4.8

They are also listed in requirements.txt and can be installed by running `pip install -r requirements.txt`

## Directory Contents

### Top level
At the top level, there is a file requirements.txt with a list of dependencies, a file mlb_loading.sql that is used to
create and populate the database, a file create_connection.py that connects to the database, and a file MLB.py that the
client application is run from. 
The CSVs for loading in in mlb_loading can be found at:
https://www.kaggle.com/pschale/mlb-pitch-data-20152018

### addData/ directory
The scripts in this directory run code that queries the user for data and adds it to the database.

### requestData/ directory
Under this directory are scripts that return IDs for a given name, or vice versa, for players, teams, and venues. An
example of when these are used is when a user must enter a player name to query some stats, the request_player function
in request_player.py queries for and returns the relevant player ID.

### searchPython/ directory
The scripts in this directory contain functions that perform a specified query on the database. For example, in
team_queries.py there is a function "most_player_apps" that takes in a specified team and returns the player with the
most appearances for that team.

### searchSQL/ directory
Contains the raw SQL executed by each of the functions in the searchPython/ directory.

### viewStatsClient/ directory
The scripts in this directory run the code that asks the user what stats they want to view.
