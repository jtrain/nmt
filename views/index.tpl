%rebase theme_base title=title
<form method="POST" action="/">
  <div class='row alert alert-info offset2 span8'>
      <h2 class="alert-heading">Pick your team!</h2>
          %for i, game in enumerate(games):
            %if not i%2:
              <div class='row'>
            %end
            <div class='span2'>
              <h3>{{ game.home_name }}</h3>
              <p>
              <button value={{ game.home_name }} name='team' type='submit'
                  class='btn btn-primary'>
                {{ game.home_name }}
              </button>
            </p>
            </div>
            <div class='span2'>
              <h3>{{ game.away_name }}</h3>
              <p>
              <button value={{ game.away_name }} name='team' type='submit'
                  class='btn btn-primary'>
                {{ game.away_name }}
              </button>
            </p>
            </div>
            %if i%2:
              </div>
            %end
          %end
          %if not i%2:
            <!-- need to close out the final divs -->
            </div>
          %end
    </div>
  </div> <!--row -->
</form>

{{ games }}
