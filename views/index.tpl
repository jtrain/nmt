%rebase theme_base title=title
<form method="POST" action="/">
  <div class='row alert alert-info offset2 span8'>
      <h2 class="alert-heading">Pick your team!</h2>
          %for i, game in enumerate(games):
            %if not i%2:
              <div class='row'>
            %end
            <div class='span2'>
              <h3>{{ game[2] }}</h3>
              <p>
              <button value={{ game[2] }} name='team' type='submit'
                  class='btn btn-primary'>
                {{ game[2] }}
              </button>
            </p>
            </div>
            <div class='span2'>
              <h3>{{ game[5] }}</h3>
              <p>
              <button value={{ game[5] }} name='team' type='submit'
                  class='btn btn-primary'>
                {{ game[5] }}
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
