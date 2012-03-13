import os
import socket

HOST = 'localhost'
PORT = 8080
DEBUG = True

APP_DIR = os.path.dirname(__file__)

def here(filename):
    return os.path.join(APP_DIR, filename)

DB_NAME = here('nmt.db')
APP_URL = "http://127.0.0.1:8080/"

LEAGUES = {'epl':'English Premier League',
        'afl':'Australian Rules'}

# scraper settings.

SCRAPE_URL = ('http://theworldgame.sbs.com.au/'
              'english-premier-league/stats/results/')
SCRAPE_URL_WEEK = SCRAPE_URL + 'filterby/gameweek/week/%d'

# time between scrapes in seconds.
SCRAPE_FREQ = 3600

SCRAPE_USER_AGENT = ('Mozilla/5.0 (Windows NT x.y; rv:10.0.1) '
                     'Gecko/20100101 Firefox/10.0.1')

POST_KEY = 'secret.squirrel.shit'
POST_HOOK = 'update/games/'

if socket.gethostname().lower().startswith('ip'):
    from prod_settings import *
