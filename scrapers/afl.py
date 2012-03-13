"""
Use the afl SOAP web app (see here for details:
http://xml.afl.com.au/mobilewebservices.asmx) to get the latest game scores.
"""
from collections import namedtuple
import datetime
import json
import suds

import settings

Game = namedtuple("Game", "home_name home_score away_name away_score")

url = 'http://xml.afl.com.au/mobilewebservices.asmx?WSDL'


# ========   App codes   =======
#
# ========   SportCodes
# (returned from GetSportCodes() only listing important ones.):
#   (SportCode){
#          Id = 1
#          Name = "Australian Rules Football"
#       },
#   (SportCode){
#            Id = 5
#            Name = "Rugby League"
#         }
#   (SportCode){
#            Id = 7
#            Name = "Rugby Union"
#         }
#
# ========   Competitioncodes
# (returned from GetSportCompetitionsByCode() only listing important ones.):
# ====  AFL
#
#   (SportCompetition){
#            Id = 26
#            Name = "AFL NAB Cup"
#         },
#   (SportCompetition){
#            Id = 1
#            Name = "AFL Premiership"
#         }
#   (SportCompetition){
#            Id = 22
#            Name = "AFL Finals Series"
#         },

def get_client(url):
    """Create a suds client for getting data from a SOAP api.
    """
    return Client(url)

def get_current_season(client, competition_id):
    """Return the unique id for the current season for the competition
    requested.

    The competition id can be obtained from 'GetSportCompetitionsByCode()'.
    A short list of the more important ones are shown above.
    """
    result = client.service.GetCurrentSportSeasonByCompetition(competition_id)
    dateformat = '%Y-%m-%d %H:%M:%S'
    date = datetime.datetime.strptime(result.StartDate, dateformat)
    return season_id, date.year

def get_current_week(client, season_id):
    """Return the unique round id (it is unique across all sports and comps).
    """
    result = client.service.GetCurrentSportRoundBySeason(season_id)
    return result.Id

def get_games(client, round_id):
    """Return all the games for the unique round id key given.

    home_team, home_score, away_team, away_score
    """
    result = client.service.GetFixturesByRound(round_id)

    matches = result.FixtureList[0]

    games = []

    for match in matches:
        home = match.HomeTeam.Name
        away = match.AwayTeam.Name

        if match.Status == '[undefined]':
            # If the game hasn't started, use this so the site will show 'vs'
            home_score = ''
            away_score = ''
        else:
            home_score = match.HomeScore
            away_score = match.AwayScore

        games.append(Game(home, home_score, away, away_score))

    return games

def store_games_in_db(year, weekno, games):
    """
    Store the games into the database. Create the records then post to the app
    server.
    """
    records = []
    for game in games:
        record = {
                'year': year,
                'round': weekno,

                'home_logo_url': '',
                'away_logo_url': ''}
        record.update(game._asdict())
        records.append(record)

    requests.post(
            settings.APP_URL + settings.POST_HOOK,
            data={
                'records': json.dumps(records),
                'key': settings.POST_KEY})

if __name__ == '__main__':
    backoff = random.randint(0, 10)
    time.sleep(backoff * 60)

    # Create the client to the web app.
    client = get_client(url)

    season_id, year = get_current_season(client, competition_id)
    current_week = get_current_week(client, season_id)

    # get games from the fixture table for this week.
    games = get_games_from_fixture(soup)

    # save in the database.
    # TODO: Need to change the database format to allow more than one league.
    # store_games_in_db(year, current_week, games)
