%rebase theme_base title=title

<div class='row-fluid'>
  <div class="span4">
    <h2>Pick your game!</h2>
      %for league, long_name in leagues.items():
        <p>
            <a href="/{{ league }}" class="btn">{{ long_name }}</a>
        </p>
      %end
  </div>
</div>
