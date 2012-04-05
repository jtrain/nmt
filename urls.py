import json
from base64 import b64encode

from bottle import abort, redirect, request, response, route, template,\
                    SimpleTemplate, url, static_file
from models import this_round, these_rounds, new_user
from models import update_games, create_db_and_get_connection

from utils import strip_tags
import settings

#-------------------
# Setup the database here.

conn = create_db_and_get_connection(settings.DB_NAME)

#-------------------

SimpleTemplate.defaults.update({
    "get_url": url,
    'sitename':"Don't Show My Team"})

def register_urls():
    """
    Not actually required. But calling this do nothing function is a stronger
    hint to check out this file once you have read the runserver.py file.

    The real magic happens on the:

    import urls

    line. Because each of these routes are defined and registered at that step.
    """
    pass

@route('/',name='index')
def index():
    """
    Show the list of competitions.
    """
    return template("index", title="Don't Show My Team",
            leagues=settings.LEAGUES,
            games=these_rounds(conn))

@route('/:league/switch', name='switch')
def switch(league):
    """
    Remove the cookie and redirect to home.
    """
    response.delete_cookie(league)
    return redirect('/%s' % league)

@route('/:league',name='league')
def league(league):
    """
    Home page, if the user doesn't have a cookie we will show them a list of
    teams that they can select from.

    The home page will always serve the same content regardless of whether the
    user has a cookie or not. We use javascript on the client side to check the
    cookie, select the league and selectively show the scores.
    """
    if league not in settings.LEAGUES.keys():
        return abort(404)

    return template("index", title="Don't Show My Team",
            leagues=settings.LEAGUES,
            games=these_rounds(conn))

def cookie_safe(text):
    return b64encode(text.decode('utf-8').encode('latin-1'))

@route('/:league', method="POST")
def league(league):
    user_team = request.params.get("team")
    if not user_team:
        # a malformed POST - didn't select a team.
        return redirect('/%s' % league)

    user_team = strip_tags(user_team)
    new_user(user_team.decode('utf-8'), conn)
    response.set_cookie(league, cookie_safe(user_team),
                        max_age=3600*24*365, path='/%s' % league)
    redirect('/%s' % league)

@route('/static/:path#.+#', name='static')
def static(path):
    if settings.DEBUG:
        response.set_header('Cache-Control', 'no-cache')
    return static_file(path, root='static')

@route('/update/games/', method="POST")
def set_games():
    try:
        key = request.params['key']
        league = request.params['league']
        records = request.params['records']
    except KeyError:
        return abort(400, 'Bad Request')

    if not key == settings.POST_KEY:
        return abort(403, "user key invalid")

    games = json.loads(records)
    update_games(league, games, conn)

    redirect('/')
