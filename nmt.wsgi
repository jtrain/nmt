# paste this in 

import os,sys, bottle

sys.path = ['/home/ubuntu/nmt/'] + sys.path
os.chdir(os.path.dirname(__file__))

import nmt

application = bottle.default_app()