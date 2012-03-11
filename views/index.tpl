%rebase theme_base title=title
<form method="POST" action="/">
  <div class='row'>
    <div class='offset2 span8'>
      <h4 class="alert-heading">Pick your team!</h4>
        %for i in range(4):
          %for team in teams[i::4]:
            <div class='span2'>
              <h3>{{ team.name }}</h3>
              <p>
              <button value={{ team.name }} name='team' type='submit'
                  class='btn btn-primary'>
                {{ team.name }}
              </button>
            </p>
            </div>
          %end
        %end
    </div>
  </div> <!--row -->
</form>

{{ games }}
