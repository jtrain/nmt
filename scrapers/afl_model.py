from collections import namedtuple, defaultdict
import os
import sqlite3
import settings
import sys

sys.path.append(os.path.join(os.path.dirname(__FILE__), '..'))

from utils import generic_namedtuple_factory

AFL_DB_FILE = 'afl.db'

FixtureRecord = namedtuple("FixtureRecord", ["seriesId",
                                                "roundId",
                                                "matchId",
                                                "team_one",
                                                "team_two",
                                                "startdatetimeUTC"])

TeamNameRecord = namedtuple("TeamNameRecord", ["teamId",
                                                "longname",
                                                "shortname"])

#--------------------
# Fixture

Fixture = """
create table if not exists Fixture (

 seriesId integer,
 roundId integer,
 matchId integer,

 team_one text,
 team_two text,
 startdatetimeUTC datetime,

 primary key (seriesId, roundId, matchId)

);"""

# Team name to team id

TeamName = """
create table if not exists TeamName (

 teamId integer,
 longname text,
 shortname text

);"""

# Game

Game = """
create table if not exists Game (

 league text,
 year integer,
 round integer,

 home_name text,
 home_score integer,
 home_logo_url text,

 away_name text,
 away_score integer,
 away_logo_url text,

 primary key (league, year, round, home_name, away_name)

);"""

# Last update
FetchTime = """
create table if not exists FetchTime (
 methodname text,
 checkdatetime datetime
);"""

def create_db_and_get_connection(db_name):
    # connect and re-create tables if they don't exist.
    conn = sqlite3.connect(db_name, check_same_thread=False)
    conn.executescript(Fixture)
    conn.executescript(TeamName)
    conn.executescript(Game)
    conn.executescript(FetchTime)
    conn.commit()
    conn.row_factory = generic_namedtuple_factory
    return conn

def update_fixture(conn, records):
    del_fixture = "delete from Fixture"
    insert_fixture_games = """insert into Fixture
                            (seriesId,
                                roundId,
                                matchId,
                                team_one,
                                team_two,
                                startdatetimeUTC)
                            values
                                (:seriesId,
                                    :roundId,
                                    :matchId,
                                    :team_one,
                                    :team_two,
                                    startdatetimeUTC)"""
    records_as_dicts = [record._asdict() for record in records]
    conn.execute(del_fixture)
    conn.executemany(insert_fixture_games, records_as_dicts)
    conn.commit()

def get_round(conn):
    earliest_dates = """select seriesId, roundId, min(startdatetimeUTC)
                        from Fixture
                        group by seriesId, roundId"""

    latest_dates = """select seriesId, roundId, max(startdatetimeUTC)
                        from Fixture
                        group by seriesId, roundId"""

    

def update_teamnamemap(conn, records):
    if not records:
        raise Exception("No team names to write to database")

    del_names = "delete from TeamName"
    insert_team_names = """insert into TeamName
                            (teamId,
                                shortname,
                                longname)
                            values
                                (:teamId,
                                :shortname,
                                :longname)"""

    records_as_dicts = [record._asdict() for record in records]
    conn.execute(del_fixture)
    conn.executemany(insert_fixture_games, records_as_dicts)
    conn.commit()

def get_teamid(conn, teamname):
    result = conn.execute("""select teamId from TeamName
                    where longname=?""", teamname)
    return result.fetchone().teamId
