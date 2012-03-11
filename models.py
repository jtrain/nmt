"""
Models for Not My Team.

Game:
    games have a year,
    a round number,
    home team,
    away team,
    home score,
    away score

User:
    team
"""
import sqlite3
import settings

#--------------------
# Game

Game = """
create table if not exists Game (

 year integer,
 round integer,

 home_name text,
 home_score integer,
 home_logo_url text,

 away_name text,
 away_score integer,
 away_logo_url text,

 primary key (year, round, home_name, away_name)

);

create index if not exists by_year on Game (
 year);
create index if not exists by_round on Game (
 round);
"""

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
    conn = sqlite3.connect(db_name)
    conn.executescript(Game)
    conn.executescript(User)
    conn.commit()
    return conn

def new_user(team_name, conn):

    create_user = "insert into User values (null, ?);"
    conn.execute(create_user, (team_name,))

    get_user_id ="select last_insert_rowid();"
    new_user_id = conn.execute(get_user_id)
    conn.commit()
    return new_user_id.fetchone()

def this_round(conn):
    """
    Return this round's scores from the game table.

    The Game table only holds the latest game round.
    Newer rounds purge the table before entering their own game.
    """
    latest_games = "select * from Game;"
    return conn.execute(latest_games)

def update_games(records, conn):
    delete_games = "delete from Game where 1=1;"
    insert_games = """
                insert into Game values (
                    :year, :round,
                    :home_name, :home_score, :home_logo_url,
                    :away_name, :away_score, :away_logo_url);"""

    conn.execute(delete_games)
    conn.executemany(insert_games, records)
    conn.commit()
