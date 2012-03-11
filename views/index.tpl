%rebase theme_base title=title
<style>

td .btn, table {
  width: 100%;
}
</style>
<form class="pick hidden" method="POST" action="/">
  <div class='row-fluid'>
    <div class="span12">
      <div class="hero-unit">
        <h1>Pick your team!</h1>
        <table style="width: 100%;">
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
  </div>
</form>
  <div class='row-fluid results hidden'>
    <div class="span12">
      <div class="hero-unit">
        <h1>Game Results</h1>
        <table style="width: 100%;">
          %for game in games:
            <tr>
              <td>
                {{ game.home_name}}
              </td>
              <td>
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
              <td>
                {{ game.away_name}}
              </td>
            </tr>
          %end
        </table>
      </div>
    </div>
  </div>
