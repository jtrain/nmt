%rebase theme_base title=title

<div class='row-fluid'>
  <div class="span3">
    <h2>Pick your game!</h2>
      %for league, long_name in leagues.items():
        <p>
            <a href="/{{ league }}" class="btn"
                style='width:100%'>{{ long_name }}</a>
        </p>
      %end
  </div>
</div>
