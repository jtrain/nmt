# paste this in 

import os,sys, bottle

app_path = os.path.dirname(os.path.abspath(__file__))
sys.path = [app_path] + sys.path
os.chdir(app_path)

import runserver

application = bottle.default_app()
