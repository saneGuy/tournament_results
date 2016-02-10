#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
        return db, cursor
    except:
        print("Unable to connect to tournament database")


def deleteMatches():
    """Remove all the match records from the database."""
    # connect to the tournament database
    conn, cur = connect()
    cur.execute("delete from matches;")
    # commit the change to the database
    conn.commit()
    # close the connection
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    # connect to the tournament database
    conn, cur = connect()
    cur.execute("delete from players;")
    # commit the change to the database
    conn.commit()
    # close the connection
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # connect to the tournament database
    conn, cur = connect()
    cur.execute("select count(*) from players;")
    # fetch all the tuples from the cursor
    results = cur.fetchone()[0]
    # close the connection
    conn.close()
    return results


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # connect to the tournament database
    conn, cur = connect()
    cur.execute("insert into players(name) values(%s)",
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
    conn, cur = connect()
    # The query will fetch tuples from players table sorted by number of wins
    # in descending order of wins
    cur.execute("select players.id, players.name, (select count(*) as wins\
      from matches where players.id = matches.winner), (select count(*) as\
      matches from matches where players.id = matches.winner or \
      players.id = matches.loser) from players left join  matches on  \
      players.id = matches.winner group by players.id order by wins;")
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
    conn, cur = connect()
    # fetch all the tuples into playersInMatches list
    cur.execute("select winner, loser from matches")
    playersInMatches = cur.fetchall()
    # check whether (winner,loser) or (loser, winner) tuple exists in the
    # playersInMatches list of tuples if any such tuple exists we should
    # not insert a row in matches table as there won't be a second match
    # between any two players
    if (winner, loser) not in playersInMatches and (loser, winner) not in\
            playersInMatches:
        cur.execute("insert into matches (winner, loser)\
                     values(%s,%s)", (winner, loser))
    # commit the changeges to database
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
