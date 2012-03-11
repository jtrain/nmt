from bottle import request, route, template
from models import this_round

def register_urls():
    """
    Not actually required. But calling this do nothing function is a stronger
    hint to check out this file once you have read the runserver.py file.

    The real magic happens on the:

    import urls

    line. Because each of these routes are defined and registered at that step.
    """
    pass

@route('/')
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
    if request.method == "GET":
        return template("index", games=this_round().fetchall())

    elif request.method == "POST":
        user_team = request.params.get("team")
        if not user_team:
            return template("index", games=this_round().fetchall())




