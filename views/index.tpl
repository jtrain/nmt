%rebase theme_base title=title

<div class='row-fluid league-select'>
  <div class="span4">
    <h2>Pick your game!</h2>
      %for league, long_name in leagues.items():
        <p>
            <button type='button'
                    value='{{ long_name }}'
                    class="btn select"
                    onclick="pick_league('{{ league }}')">{{ long_name }}</button>
        </p>
      %end
  </div>
</div>

%for league, long_name in leagues.items():
  <div class='league-block {{ league }} hidden'>
    <form class="pick {{ league }} hidden" method="POST" action="/{{ league }}">
      <div class='row'>
        <div class="span4">
          <h2>{{ long_name }}<br>Pick your team!</h2>
          <table class='game table table-bordered table-striped'>
            %for game in games[league]:
              <tr>
                <td>
                  <button value="{{ game.home_name }}"
                          class="btn select" name="team"
                          onclick="pick_team('{{ league }}', '{{ game.home_name }}')"
                          type="button">{{ game.home_name}}</button>
                </td>
                <td>
                  <button value="{{ game.away_name }}"
                          class="btn select" name="team"
                          onclick="pick_team('{{ league }}', '{{ game.away_name }}')"
                          type="button">{{ game.away_name}}</button>
                </td>
              </tr>
            %end
          </table>
        </div>
      </div>
    </form>
    <div class='row results {{ league }} hidden'>
      <div class="span4">
        <h2>{{ long_name }}<br>Game Results</h2>
        <table class="game table table-bordered table-striped">
          <thead>
           <tr><th class="home">Home</th><th class="score">vs</th><th class="away">Away</th></tr>
          </thead>
          <tbody>
          %for game in games[league]:
            <tr>
              <td class='home'>
                {{ game.home_name}}
              </td>
              <td class='score'>
                %if game.home_score == None:
                    <div class='noscore score {{ league }} {{ game.home_name.replace(" ", "-") }}
                                {{game.away_name.replace(" ", "-")}}'>
                                        vs</div>
                %else:
                    <div class='score {{ league }} hidden {{game.home_name.replace(" ", "-")}}
                                {{game.away_name.replace(" ", "-")}}'>
                        {{ game.home_score }} - {{ game.away_score }}
                    </div>
                    <div class='noscore {{ league }} {{game.home_name.replace(" ", "-")}}
                                {{game.away_name.replace(" ", "-")}}'>
                        ? - ?
                        <br>
                        <button type='button'
                                value='Reveal!'
                                class="btn btn-primary"
                                onclick="pick_league('{{ league }}')">Reveal!</button>
                    </div>
                %end
              </td>
              <td class='away'>
                {{ game.away_name}}
              </td>
            </tr>
          %end
          </tbody>
        </table>
      </div>
    </div>
  </div>
%end
