%rebase theme_base title=title

<script>
function getCookie(c_name) {
  var i,x,y,ARRcookies=document.cookie.split(";");
  for (i=0;i<ARRcookies.length;i++) {

    x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
    y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
    x=x.replace(/^\s+|\s+$/g,"");
    if (x==c_name) {
      return unescape(y).replace(/"/g, '');
    }
  }
}
</script>
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
                    <div class='score hidden {{game.home_name}}
                                {{game.away_name}}'>
                        {{ game.home_score }} - {{ game.away_score }}
                    </div>
                    <div class='noscore {{game.home_name}}
                                {{game.away_name}}'>
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
