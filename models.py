"""
Models for Not My Team.

Game:
    games have a league,
    a year,
    a round number,
    home team,
    away team,
    home score,
    away score

User:
    team
"""
from collections import namedtuple
import sqlite3
import settings

from utils import make_namedtuple_factory
#--------------------
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

);

create index if not exists by_league on Game(
 league);
create index if not exists by_year on Game (
 year);
create index if not exists by_round on Game (
 round);
"""
GameRecord = namedtuple("Game",
                   "league year round "
                   "home_name home_score home_logo_url "
                   "away_name away_score away_logo_url")

User = """
create table if not exists User (

  id integer primary key autoincrement,
  team_name text
);
create index if not exists by_user_id on User (
 id);
"""

def create_db_and_get_connection(db_name):
    # connect and re-create tables if they don't exist.
    conn = sqlite3.connect(db_name, check_same_thread=False)
    conn.executescript(Game)
    conn.executescript(User)
    conn.commit()
    conn.row_factory = make_namedtuple_factory(GameRecord)
    return conn

def new_user(team_name, conn):

    create_user = "insert into User values (null, ?);"
    conn.execute(create_user, (team_name,))

    get_user_id ="select last_insert_rowid();"
    new_user_id = conn.execute(get_user_id)
    conn.commit()
    return new_user_id.fetchone()

def this_round(league, conn):
    """
    Return this round's scores from the game table.

    The Game table only holds the latest game round.
    Newer rounds purge the table before entering their own game.
    """
    latest_games = "select * from Game where league=?;"
    return conn.execute(latest_games, (league,))

def update_games(league, records, conn):
    delete_games = "delete from Game where league=?;"
    insert_games = """
                insert into Game values (
                    :league, :year, :round,
                    :home_name, :home_score, :home_logo_url,
                    :away_name, :away_score, :away_logo_url);"""

    conn.execute(delete_games, (league,))
    conn.executemany(insert_games, records)
    conn.commit()
