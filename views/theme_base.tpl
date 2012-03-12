<!DOCTYPE html>
<html lang="en-us">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{title}}</title>
        <!-- HTML5 shim, for IE6-8 support of HTML elements -->
        <!--[if lt IE 9]>
            <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->
          <link rel="shortcut icon" href="{{ get_url('static', path='img/favicon.ico') }}" />
          <link rel="stylesheet" href="{{ get_url('static', path='css/bootstrap.css') }}">

          <style type="text/css">
            body {
              padding-top: 60px;
              padding-bottom: 40px;
            }
          </style>
          <link href="{{ get_url('static', path="css/bootstrap-responsive.css") }}" rel="stylesheet">
          <link rel="stylesheet" href="{{ get_url('static', path='css/nmt.css') }}">

    </head>
    <body>

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="{{ get_url('index') }}">{{ sitename }}</a>
        </div>
      </div>
    </div>

    <div class="container-fluid">
        %include
    </div>

    <div id="footer">
        <div class="inner">
            <div class="container">
                %include _footer
            </div>
        </div>
    </div>

    %include js_base get_url=get_url
    <script type="text/javascript">

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

     var team = getCookie('not_my_team_name');
     if ( team === undefined){
       // show the pick team view.
       $('.pick').removeClass('hidden');
     } else {
       // hide the ?s for games you want to see and show the scores.
       var teamclass = team.replace(/ /g, '-');
       $('.noscore').not('.' + teamclass).addClass('hidden');
       $('.score').not('.' + teamclass).removeClass('hidden');

       // now show the entire results container.
       $('.results').removeClass('hidden');

       // add a message about which team rocks.
       var plural = 's';
       if (team.charAt(team.length - 1) === 's') {
         plural = '';
       }
       $('.brand').after("<p class='navbar-text'>"
                         + team + " rock" + plural + "!"
                         + " (not <a href='/switch' title='change teams'>your team</a>?)</p>");
     }
    </script>
  </body>
</html>
