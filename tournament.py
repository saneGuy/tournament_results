#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # connect to the tournament database
    conn = connect()
    # get the cursor and execute the query
    # delete from matches; deletes all the records from matches
    cur = conn.cursor()
    cur.execute("delete from matches;")
    # commit the change to the database
    conn.commit()
    # close the connection
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    # connect to the tournament database
    conn = connect()
    # get the cursor and execute the query
    # delete from players; deletes all the records from players
    cur = conn.cursor()
    cur.execute("delete from players;")
    # commit the change to the database
    conn.commit()
    # close the connection
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # connect to the tournament database
    conn = connect()
    # get the cursor and execute the query
    # select count(*) from players; will count the number of tuples
    # in players table
    cur = conn.cursor()
    cur.execute("select count(*) from players;")
    # fetch all the tuples from the cursor
    results = cur.fetchall()
    # close the connection
    conn.close()
    return results[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # connect to the tournament database
    conn = connect()
    # get the cursor and execute the query
    # The query will insert a row with id, name, wins, matches for
    # a single player
    cur = conn.cursor()
    cur.execute("insert into players(name, wins, matches) values(%s,0,0)",
                (name,))
    # commit the change to the database
    conn.commit()
    # close the connection
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # connect to the tournament database
    conn = connect()
    # get the cursor and execute the query
    # The query will fetch tuples from players table sorted by number of wins
    # in descending order of wins
    cur = conn.cursor()
    cur.execute("select * from players order by wins desc;")
    # Fetch all the tuples from the cursor
    results = cur.fetchall()
    # close the connection
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # connect to the tournament database
    conn = connect()
    # get the cursor and execute the query
    # fetch all the tuples into playersInMatches list
    cur = conn.cursor()
    cur.execute("select player1, player2 from matches")
    playersInMatches = cur.fetchall()
    # check whether (winner,loser) or (loser, winner) tuple exists in the
    # playersInMatches list of tuples if any such tuple exists we should
    # not insert a row in matches table as there won't be a second match
    # between any two players
    if (winner, loser) not in playersInMatches and (loser, winner) not in playersInMatches:
            cur.execute("insert into matches (player1, player2, winner, loser)\
                         values(%s,%s,%s,%s)", (winner, loser, winner, loser))
            cur.execute("update players set wins = wins + 1 where id = %s ;",
                        (winner, ))
            cur.execute("update players set matches = matches + 1 where \
                        id = %s ;", (winner, ))
            cur.execute("update players set matches = matches + 1 where \
                        id = %s ;", (loser, ))
    # commit the changes to database
    conn.commit()
    # close the database connection
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # get the current playerStandings and pairup and make a list
    # as the tuples are already sorted by the number of wins a
    # sequential pairing will pair players with equal wins or nearly
    # equal wins
    results = playerStandings()
    pairings = []
    i = 0
    while i < len(results):
        pairings.append((results[i][0], results[i][1], results[i+1][0],
                        results[i+1][1]))
        i = i + 2
    return pairings
