"""
Use the afl SOAP web app (see here for details:
http://xml.afl.com.au/mobilewebservices.asmx) to get the latest game scores.
"""
from collections import namedtuple
import datetime
import json
import os
import sys

import requests
from suds.client import Client
import pytz

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import settings
import afl_model

ARBITRARY_UID = 11235813
STARTDATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"

# It appears that game times are given in Eastern daylight savings time.
MELBOURNE_TIME = pytz.timezone('Australia/Melbourne')

Game = namedtuple("Game", "home_name home_score away_name away_score")

url = "http://arf.webservice.sportsflash.com.au/WebService.asmx?WSDL"

client = Client(url)

# Process:
# Get fixture
# - only request once per day
# Compute latest round
# Compute games that need to be fetched
# Look up teamid from team name
#  - Scrape team names if necessary
# Update games active games
# Send latest round details to server
def get_fixture_and_store_in_db(conn, client, uid):
    methodname = 'GetFixture'
    now = datetime.datetime.now()
    melb_now = MELBOURNE_TIME.localize(now)
    today = melb_now.date()
    last_fetch = afl_model.get_fetchtime(conn, methodname)
    if last_fetch:
        # We have already received this today. It doesn't change very much.
        if today == last_fetch.checkdatetime.date():
            return

    fixture = client.service.GetFixture(uid)
    fixture_records = []
    for record in fixture.Fixture.Event:
        # Match text = "Carlton vs. Richmond"
        teams = record.Match.split(' vs. ')
        startdatetime = datetime.datetime.strptime(record.StartDateTime,
                                                    STARTDATETIME_FMT)
        fixture_records.append(afl_model.FixtureRecord(
                                            seriesId=record._seriesId,
                                            roundId=record._roundId,
                                            matchId=record._matchId,
                                            venueId=record.Venue._venueId,
                                            team_one=teams[0],
                                            team_two=teams[1],
                                            startdatetime=startdatetime
                                            )
                                        )
    afl_model.update_fixture(conn, fixture_records)
    afl_model.update_fetchtime(conn, methodname, melb_now)

def update_and_get_teamid(conn, match):
    seriesId = match.seriesId
    result = client.service.GetSeriesTeam(ARBITRARY_UID, seriesId)
    teams = result.SeriesTeams.Header.Teams.Team

    name_records = []
    for team in teams:
        name_records.append(afl_model.TeamNameRecord(seriesId=seriesId,
                                                    teamId=team._teamId,
                                                    longname=team.LongName,
                                                    shortname=team.ShortName)
                                                    )

    afl_model.update_teamnamemap(conn, name_records)

    return afl_model.get_teamid(conn, match.seriesId, match.home_name)

def get_teamid(conn, match):
    teamid = afl_model.get_teamid(conn, match.seriesId,  match.home_name)

    if not teamid:
        teamid = update_and_get_teamid(conn, match)

    return teamid

def update_aflgames(conn, matches):
    for match in matches:
        teamid = get_teamid(conn, match)
        matchinfo = client.service.GetCompetitionFixture(ARBITRARY_UID,
                                                        match.seriesId,
                                                        match.roundId,
                                                        teamid,
                                                        match.venueId)
        fixture_match = matchinfo.Fixture.Series.Rounds.Round.Matches.Match

        aflgame = afl_model.AFLGameRecord(seriesId=match.seriesId,
                                roundId=match.roundId,
                                matchId=match.matchId,
                                venueId=match.venueId,
                                home_name=fixture_match._homeTeamName,
                                home_score=fixture_match._homeTeamScore,
                                away_name=fixture_match._awayTeamName,
                                away_score=fixture_match._awayTeamScore,
                                currentstatus=fixture_match._currentStatus
                                )

        afl_model.update_AFLGame(conn, aflgame)


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

def update_server_afl(conn, league, round):

    year = round.start.year
    games = afl_model.get_current_round_scores(conn)
    store_games_in_db('afl', year, round.roundId, games)

def scrape_league(league):
    """Does the scrape of the league and sends it to the db.

    Pass in the unque string for the league you want to scrape.
    """

    now = datetime.datetime.now()
    melb_now = MELBOURNE_TIME.localize(now)
    today = melb_now.date()

    conn = afl_model.create_db_and_get_connection(afl_model.AFL_DB_FILE)
    get_fixture_and_store_in_db(conn, client, ARBITRARY_UID)
    round = afl_model.get_round(conn, today)
    afl_model.refresh_AFLGame_table_round(conn, round.seriesId, round.roundId)
    active_games = afl_model.get_active_games(conn)
    update_aflgames(conn, active_games)
    update_server_afl(conn, league, round)

if __name__ == "__main__":
    scrape_league('afl')
