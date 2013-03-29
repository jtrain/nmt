"""
Use the afl SOAP web app (see here for details:
http://xml.afl.com.au/mobilewebservices.asmx) to get the latest game scores.
"""
from collections import namedtuple
import json
import os
import requests
from suds.client import Client
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import settings

Game = namedtuple("Game", "home_name home_score away_name away_score")

url = "http://arf.webservice.sportsflash.com.au/WebService.asmx?WSDL"

client = Client(url)

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
def get_comp_afl():
    """Return the in progress competition (NAB cup or Finals or whatever)
    """
    # Afl premiership = code 1
    return 1


def get_comp(league):
    """This will select the function to run to get the current competition for
    the legue specified"""
    if league == 'afl':
        return get_comp_afl()


def get_current_season(client, competition_id):
    """Return the unique id for the current season for the competition
    requested.

    The competition id can be obtained from 'GetSportCompetitionsByCode()'.
    A short list of the more important ones are shown above.
    """
    result = client.service.GetCurrentSportSeasonByCompetition(competition_id)
    return result.Id, result.StartDate.year

def get_current_round_id(client, season_id):
    """Return the unique round id (it is unique across all sports and comps).
    """
    result = client.service.GetCurrentSportRoundBySeason(season_id)
    return result.Id

def get_games_from_fixture(client, round_id):
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
            home_score = None
            away_score = None
        else:
            home_score = match.HomeScore
            away_score = match.AwayScore
            if home_score == 0 and away_score == 0:
                home_score = away_score = None

        games.append(Game(home, home_score, away, away_score))

    return games

def store_games_in_db(league, year, weekno, games):
    """
    Store the games into the database. Create the records then post to the app
    server.
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

    competition_id = get_comp(league)
    season_id, year = get_current_season(client, competition_id)
    current_round_id = get_current_round_id(client, season_id)

    # get games from the fixture table for this week.
    games = get_games_from_fixture(client, current_round_id)

    # save in the database.
    store_games_in_db(league, year, current_round_id, games)


if __name__ == "__main__":
    print client
    # print client.service.GetCompetitionFixture(11235813, 138, roundid, teamid, venueid)
    # print client.service.GetCompetitionFixture(11235813, 138, 1, 16, 42)
    # print client.service.GetCompetitionFixture(11235813, 138, 1, 16, 42)
    # print client.service.GetFixture(1,138)
    print client.service.GetSeriesTeam(1,138)
    # print client.service.GetCompetitionList(1)
