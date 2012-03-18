"""
Scrape the the world game website for the latest game scores.
"""
from collections import namedtuple
import json
import re
import urllib2
import os
import posixpath
import sqlite3
import sys

from BeautifulSoup import BeautifulSoup
import requests

# put the parent dir on the system path.
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import settings

SBS_URL = 'http://theworldgame.sbs.com.au/'
RESTULTS_PATH = 'stats/results/'
SCRAPE_URL_WEEK = 'filterby/gameweek/week/%d'

def complete_league_url(league_path):
    return posixpath.join(SBS_URL, league_path, RESTULTS_PATH)

LEAGUE_URLS = {'epl':complete_league_url('english-premier-league'),
        'bundesliga':complete_league_url('germany-bundesliga')}


# blend in with the crowd..
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', settings.SCRAPE_USER_AGENT)]

# to find the week number.
re_weekno = re.compile('[\d]+')
# to find the fixtures table.
re_fixture = re.compile('fixtures')
re_home = re.compile('c3')
re_score = re.compile('c4')
re_away = re.compile('c5')

Game = namedtuple("Game", "home_name home_score away_name away_score")

def get_current_week(soup):
    """
    From the given soup, return the latest week number.
    """
    weeks = soup.findAll('option', value=re_weekno)
    return int(weeks[-1].get('value'))

def get_url_as_soup(url):
    content = opener.open(url)
    return BeautifulSoup(content)

def get_games_from_fixture(soup):
    """
    Given a soup with the fixture. Return all the games.

    home_team, home_score, away_team, away_score
    """
    rows = soup.find('div', {'class': re_fixture}).findAll('tr')

    games = []

    for row in rows[1:]:
        try:
            home, scores, away = (
                row.find('td', {'class': re_home}).text,
                row.find('td', {'class': re_score}).text,
                row.find('td', {'class': re_away}).text)
        except AttributeError:
            # skip the header rows.
            continue

        try:
            home_score, away_score = scores.replace(' ', '').split('-')
            home_score, away_score = int(home_score), int(away_score)
        except ValueError:
            home_score = away_score = None

        games.append(Game(home, home_score, away, away_score))

    # game date is first row (c1) with format: "Sat, 10 Mar 12"
    year = int(rows[1].find('td', {'class': "c1"}).text.split()[-1])
    return year, games

def store_games_in_db(league, year, weekno, games):
    """
    Store the games into the database. Blow away all the old stuff and then add
    the new things.
    """
    records = []
    for game in games:
        record = {
                'league': league,
                'year': year,
                'round': weekno,

                'home_logo_url': '',
                'away_logo_url': ''}
        record.update(game._asdict())
        records.append(record)

    requests.post(
            settings.APP_URL + settings.POST_HOOK,
            data={
                'league':league,
                'records': json.dumps(records),
                'key': settings.POST_KEY})

def scrape_league(league):
    """Does the scrape of the league and sends it to the db.

    Pass in the unque string for the league you want to scrape.
    """
    # find the week number.
    base_scrape_url = LEAGUE_URLS[league]
    soup = get_url_as_soup(base_scrape_url)
    current_week = get_current_week(soup)

    # get games from the fixture table for this week.
    soup = get_url_as_soup(posixpath.join(base_scrape_url,SCRAPE_URL_WEEK)
                            % current_week)
    year, games = get_games_from_fixture(soup)

    # save in the database.
    store_games_in_db(league, year, current_week, games)

if __name__ == '__main__':

    # English Premier league
    scrape_league('epl')

    # bundesliga
    scrape_league('bundesliga')
