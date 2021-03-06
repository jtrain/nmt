import os
import socket

HOST = 'localhost'
PORT = 8080
DEBUG = True

APP_DIR = os.path.dirname(__file__)

def here(filename):
    return os.path.join(APP_DIR, filename)

DB_NAME = here('nmt.db')
AFL_DB_NAME = here('afl.db')
APP_URL = "http://127.0.0.1:8080/"

LEAGUES = {'epl':'English Premier League',
           'bundesliga':'Bundesliga',
           'afl':'Australian Rules'}

# time between scrapes in seconds.
SCRAPE_FREQ = 3600

SCRAPE_USER_AGENT = ('Mozilla/5.0 (Windows NT x.y; rv:10.0.1) '
                     'Gecko/20100101 Firefox/10.0.1')

POST_KEY = 'secret.squirrel.shit'
POST_HOOK = 'update/games/'

LOG_FILE = os.path.join(APP_DIR, 'scrape_errors.log')
if socket.gethostname().lower().startswith('ip'):
    if 'preprod' in os.path.abspath(__file__):
        from preprod_settings import *
    else:
        from prod_settings import *
