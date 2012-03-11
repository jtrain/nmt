import os

HOST = 'localhost'
PORT = 8080
DEBUG = True

APP_DIR = os.path.dirname(__file__)

def here(filename):
    return os.path.join(APP_DIR, filename)

DB_NAME = here('nmt.db')
