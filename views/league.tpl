%rebase theme_base title=title
<form class="pick hidden" method="POST" action="/{{ league }}">
  <div class='row'>
    <div class="span4">
      <h2>{{ league_long_name }}<br>Pick your team!</h2>
      <table class='game table table-bordered table-striped'>
        %for game in games:
          <tr>
            <td>
              <button value="{{ game.home_name }}"
                      class="btn select" name="team"
                      type="sumit">{{ game.home_name}}</button>
            </td>
            <td>
              <button value="{{ game.away_name }}"
                      class="btn select" name="team"
                      type="sumit">{{ game.away_name}}</button>
            </td>
          </tr>
        %end
      </table>
    </div>
  </div>
</form>
<div class='row results hidden'>
  <div class="span4">
    <h2>{{ league_long_name }}<br>Game Results</h2>
    <table class="game table table-bordered table-striped">
      <thead>
       <tr><th class="home">Home</th><th class="score">vs</th><th class="away">Away</th></tr>
      </thead>
      <tbody>
      %for game in games:
        <tr>
          <td class='home'>
            {{ game.home_name}}
          </td>
          <td class='score'>
            %if game.home_score == None:
                <div class='noscore score {{ game.home_name.replace(" ", "-") }} 
                            {{game.away_name.replace(" ", "-")}}'>
                                    vs</div>
            %else:
                <div class='score hidden {{game.home_name.replace(" ", "-")}}
                            {{game.away_name.replace(" ", "-")}}'>
                    {{ game.home_score }} - {{ game.away_score }}
                </div>
                <div class='noscore {{game.home_name.replace(" ", "-")}}
                            {{game.away_name.replace(" ", "-")}}'>
                    ? - ?
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
