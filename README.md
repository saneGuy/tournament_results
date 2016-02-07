# Tournament Results
Here we use a relational database PostgreSQL to store information about the 
players, matches played, and use this stored information to schedule 
matches among the players with same number of wins to get a champion.


## Getting Started
* Download the following files into your local machine.
	It contains 3 files:
	* tournament.py
	* tournament.sql
	* tournament_test.py
* bring your virtual machine up by running the following commands:
	* vagrant up 
	* vagrant ssh
* Run psql -f tournament.sql to create the database and tables
* Now to test the functions in module tournament run
	* python tournament_test.py from the directory where 
	the python files are located


**Note:** Make sure all the files are in the same directory

tournamet.py is the main module with all the required functions.
tournament_test.py contains unit tests to test all the functions in the
tournament module.
import the module tournament into your code and use the functions.


## Prerequisites for running 
* Python should be installed
* Vagrant with PostgreSQL with psql client should be installed 

##Code details
*  **tournamet.py**  contains all the functions to connect to the database,
delete matches, delete players, count players, register player, current player
standings, report match between two players, swisPairings to return a list of 
pairs of players for scheduling matches.
*  **tournament_test.py** contains functions to test each function defined in 
the tournament module.
*  **tournament.sql** is the database setup file that creates the required tournament
database, players and matches tables . You need to run this file before running any 
of the above python modules. As this sets up the required database and table for the
tournament.

##Testing : Done 
