%rebase theme_base title=title

<form method="POST" action="/">
  <div class='row alert alert-info offset2 span6'>
    <h2 class="alert-heading">Pick your team!</h2>
      <div class='row offset1'>
        <table>
          %for game in games:
            <tr>
              <td>
                <button value="{{ game.home_name }}"
                        class="btn" name="team"
                        type="sumit">{{ game.home_name}}</button>
              </td>
              <td>
                <button value="{{ game.away_name }}"
                        class="btn" name="team"
                        type="sumit">{{ game.away_name}}</button>
              </td>
            </tr>
          %end
      </table>
    </div>
  </div> <!--row -->
</form>
