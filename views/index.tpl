%rebase theme_base title=title
<style>


</style>
<form class="pick hidden" method="POST" action="/">
  <div class='row-fluid'>
    <div class="span12">
        <h2>English Premier League Pick your team!</h2>
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
  <div class='row-fluid results hidden'>
    <div class="span12">
        <h2>English Premier League Game Results</h2>
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
                    vs
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
