from bottle import redirect, request, response, route, template,\
                    SimpleTemplate, url, static_file
from models import this_round, new_user

from utils import strip_tags

DEBUG = True

SimpleTemplate.defaults.update({"get_url": url, 'sitename':'Not My Team'})

class team(object):
    def __init__(self, name):
        self.name = name

teams = []
for i in ['hi','bye','pissoff','1','2','3','4','5','6','7']:
    teams.append(team(i))


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
    Home page, if the user doesn't have a cookie we will show them a list of
    teams that they can select from.

    Picking a team will issue a POST command with the name of the team selected.
    We need to respond to the POST with a cookie that has the team name inside.

    The home page will always serve the same content regardless of whether the
    user has a cookie or not. We use javascript on the client side to check the
    cookie and selectively show the scores.
    """
    return template("index", title='Games!', teams=teams,
            games=this_round().fetchall())

@route('/', method="POST")
def index():
    user_team = request.params.get("team")
    if not user_team:
        # a malformed POST - didn't select a team.
        return redirect('/')

    user_team = strip_tags(user_team)
    new_user(user_team)

    response.set_cookie('not_my_team_name', user_team,
                        max_age=3600*24*365)
    redirect('/')

@route('/static/:path#.+#', name='static')
def static(path):
    if DEBUG:
        response.set_header('Cache-Control', 'no-cache')
    return static_file(path, root='static')
