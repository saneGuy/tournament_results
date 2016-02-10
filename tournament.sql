-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- drop tournament database if it already exists
drop database if exists tournament;
-- create tournament database 
create database tournament;

-- connect to the tournament database
\c tournament;

-- create players table that contains player id, name
create table players(id serial PRIMARY KEY, name varchar(50));

-- create matches table that contains match id, winner id, loser id
create table matches(id serial PRIMARY KEY, winner int references players(id), loser int references players(id));

