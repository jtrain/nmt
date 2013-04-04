from collections import namedtuple, defaultdict
import datetime
import os
import sqlite3
import settings
import sys

import pytz

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import generic_namedtuple_factory

AFL_CODE = 'afl'

MELBOURNE_TIME = pytz.timezone('Australia/Melbourne')
ONE_DAY = datetime.timedelta(days=1)

FixtureRecord = namedtuple("FixtureRecord", ["seriesId",
                                                "roundId",
                                                "matchId",
                                                "venueId",
                                                "team_one",
                                                "team_two",
                                                "startdatetimeUTC"])

TeamNameRecord = namedtuple("TeamNameRecord", ["seriesId",
                                                "teamId",
                                                "longname",
                                                "shortname"])

AFLGameRecord = namedtuple("AFLGameRecord", ["seriesId",
                                                "roundId",
                                                "matchId",
                                                "venueId",
                                                "home_name",
                                                "home_score",
                                                "away_name",
                                                "away_score",
                                                "currentstatus"
                                                ])
#--------------------
# Fixture

Fixture = """
create table if not exists Fixture (

 seriesId integer,
 roundId integer,
 matchId integer,
 venueId integer,

 team_one text,
 team_two text,
 startdatetimeUTC timestamp,

 primary key (seriesId, roundId, matchId)

);"""

# Team name to team id

TeamName = """
create table if not exists TeamName (

 seriesId integer,
 teamId integer,
 longname text,
 shortname text

);"""

# AFLGame

AFLGame = """
create table if not exists AFLGame (

 seriesId integer,
 roundId integer,
 matchId integer,
 venueId integer,

 home_name text,
 home_score integer,

 away_name text,
 away_score integer,

 startdatetimeUTC timestamp,
 currentstatus text,

 primary key (seriesId, roundId, matchId)

);"""

# Last update
FetchTime = """
create table if not exists FetchTime (
 methodname text primary key on conflict abort,
 checkdatetime timestamp
);"""

def create_db_and_get_connection(db_name):
    # connect and re-create tables if they don't exist.
    conn = sqlite3.connect(db_name,
                            check_same_thread=False,
                            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
                            )
    conn.executescript(Fixture)
    conn.executescript(TeamName)
    conn.executescript(AFLGame)
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
                                venueId,
                                team_one,
                                team_two,
                                startdatetimeUTC)
                            values
                                (:seriesId,
                                    :roundId,
                                    :matchId,
                                    :venueId,
                                    :team_one,
                                    :team_two,
                                    :startdatetimeUTC)"""
    records_as_dicts = [record._asdict() for record in records]
    conn.execute(del_fixture)
    conn.executemany(insert_fixture_games, records_as_dicts)
    conn.commit()

def compute_round(start_end_round_dates, start_melb_day):
    # only one round to return
    if len(start_end_round_dates) == 1:
        return start_end_round_dates[0]

    # If the current time is within the start of the first day a game is played
    # and midnight of the night the last game of the round is played, return
    # that round.
    for round in start_end_round_dates:
        if ((start_melb_day < pytz.utc.localize(round.end) + ONE_DAY)
                    and (start_melb_day > pytz.utc.localize(round.start))):
            return round

    # If we are not in a round, return the last played round or the next round
    # if we are within 1 day of the first game day (eg. Thursday for a Friday
    # night match)
    for round in start_end_round_dates:
        game_day_start = MELBOURNE_TIME.localize(round.start)
        game_day_start = game_day_start.replace(hour=0, minute=0, second=0)
        game_day_start_utc = game_day_start.astimezone(pytz.utc)
        if (game_day_start_utc - ONE_DAY) <= start_melb_day:
            this_round = round

    return this_round

def get_round(conn, start_melb_day):
    start_end_round_dates = """select seriesId,
                                roundId,
                                min(startdatetimeUTC) as "start [timestamp]",
                                max(startdatetimeUTC) as "end [timestamp]"
                        from Fixture
                        group by seriesId, roundId
                        order by seriesId, roundId"""
    start_end_round_dates = conn.execute(start_end_round_dates).fetchall()

    return compute_round(start_end_round_dates, start_melb_day)

def refresh_AFLGame_table_round(conn, seriesId, roundId):
    param_dict = {'seriesId': seriesId, 'roundId': roundId}
    conn.execute("""delete from AFLGame
                    where seriesId != :seriesId
                        or roundId != :roundId""", param_dict)

    insert_or_ignore_new_games = """insert or ignore into AFLGame
                    (seriesId,
                        roundId,
                        matchId,
                        venueId,
                        home_name,
                        home_score,
                        away_name,
                        away_score,
                        startdatetimeUTC,
                        currentstatus
                        )
                    select seriesId,
                            roundId,
                            matchId,
                            venueId,
                            team_one,
                            null,
                            team_two,
                            null,
                            startdateTimeUTC,
                            ''
                        from Fixture
                        where seriesId=:seriesId
                            and roundId=:roundId"""

    conn.execute(insert_or_ignore_new_games, param_dict)

    conn.commit()


def update_AFLGame(conn, aflgame):
    conn.execute("""update AFLGame
                    set home_name=:home_name,
                        home_score=:home_score,
                        away_name=:away_name,
                        away_score=:away_score,
                        currentstatus=:currentstatus
                    where seriesId=:seriesId
                        and roundId=:roundId
                        and matchId=:matchId""",
                        aflgame._asdict())
    conn.commit()


def get_active_games(conn):
    result = conn.execute("""select seriesId,
                                    roundId,
                                    matchId,
                                    home_name,
                                    away_name,
                                    venueId
                            from AFLGame
                            where startdatetimeUTC < datetime('now')
                                and currentstatus != 'FT'
                                """)

    return result.fetchall()

def get_current_round_scores(conn):
    results = conn.execute("""select home_name,
                                        home_score,
                                        away_name,
                                        away_score
                                from AFLGame""")
    return results.fetchall()

def update_teamnamemap(conn, records):
    if not records:
        raise Exception("No team names to write to database")

    del_names = "delete from TeamName"
    insert_team_names = """insert into TeamName
                            (seriesId,
                                teamId,
                                shortname,
                                longname)
                            values
                                (:seriesId,
                                :teamId,
                                :shortname,
                                :longname)"""

    records_as_dicts = [record._asdict() for record in records]
    conn.execute(del_names)
    conn.executemany(insert_team_names, records_as_dicts)
    conn.commit()

def get_teamid(conn, seriesId, teamname):
    result = conn.execute("""select teamId from TeamName
                    where seriesId=?
                    and longname=?""", (seriesId, teamname))
    return result.fetchone()

def get_fetchtime(conn, method):
    results = conn.execute("""select checkdatetime from FetchTime
                                where methodname=?""", (method,))
    return results.fetchone()

def update_fetchtime(conn, method, time):
    conn.execute("""insert or replace into FetchTime
                    (methodname, checkdatetime)
                    values
                    (?, ?)""", (method, time))
    conn.commit()
