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
          <link href="{{ get_url('static', path="css/bootstrap-responsive.css") }}" rel="stylesheet">
          <link rel="stylesheet" href="{{ get_url('static', path='css/nmt.css') }}">
          <script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-13008285-8']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>

    </head>
    <body>

    <div class="navbar">
      <div class="navbar-inner">
        <div class="container my-nav">
          <a class="brand my-brand" href="javascript:void(0)" onclick='change_league()'>{{ sitename }}</a>
          <div class="repick repick-league navbar-text hidden">Change your <button class='btn btn-primary'
                value='League'
                onclick="change_league()"
                type='button'>League</button></div>
          <div class="repick repick-team navbar-text hidden"><span class='team-rocks'>You rock!</span></div>
        </div>
      </div>
    </div>

    <div class="container">
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

  var keyStr = "ABCDEFGHIJKLMNOP" +
               "QRSTUVWXYZabcdef" +
               "ghijklmnopqrstuv" +
               "wxyz0123456789+/" +
               "=";

  function encode64(input) {
        var output = "";
        var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
        var i = 0;


        while (i < input.length) {

            chr1 = input.charCodeAt(i++);
            chr2 = input.charCodeAt(i++);
            chr3 = input.charCodeAt(i++);

            enc1 = chr1 >> 2;
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
            enc4 = chr3 & 63;

            if (isNaN(chr2)) {
                enc3 = enc4 = 64;
            } else if (isNaN(chr3)) {
                enc4 = 64;
            }

            output = output +
            keyStr.charAt(enc1) + keyStr.charAt(enc2) +
            keyStr.charAt(enc3) + keyStr.charAt(enc4);

        }

    return output;
  }

  function decode64(input) {
     var output = "";
     var chr1, chr2, chr3 = "";
     var enc1, enc2, enc3, enc4 = "";
     var i = 0;
 
     // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
     var base64test = /[^A-Za-z0-9\+\/\=]/g;
     input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
 
     do {
        enc1 = keyStr.indexOf(input.charAt(i++));
        enc2 = keyStr.indexOf(input.charAt(i++));
        enc3 = keyStr.indexOf(input.charAt(i++));
        enc4 = keyStr.indexOf(input.charAt(i++));
 
        chr1 = (enc1 << 2) | (enc2 >> 4);
        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
        chr3 = ((enc3 & 3) << 6) | enc4;
 
        output = output + String.fromCharCode(chr1);
 
        if (enc3 != 64) {
           output = output + String.fromCharCode(chr2);
        }
        if (enc4 != 64) {
           output = output + String.fromCharCode(chr3);
        }
 
        chr1 = chr2 = chr3 = "";
        enc1 = enc2 = enc3 = enc4 = "";
 
     } while (i < input.length);
 
     return unescape(output);
  }



      function getCookie(c_name) {
        var i,x,y,ARRcookies=document.cookie.split(";");
        for (i=0;i<ARRcookies.length;i++) {

          x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
          y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
          x=x.replace(/^\s+|\s+$/g,"");
          if (x==c_name) {
            return unescape(decode64(y.replace(/"/g, '')));
          }
        }
      }
      function delCookie(name)
      {
        document.cookie = name + '=; expires=Thu, 01-Jan-70 00:00:01 GMT;';
      }

    function setCookie(c_name, val) {
        var max_age;
        var exp_date = new Date();
        exp_date.setDate(exp_date.getDate() + 365);
        exp_date.toGMTString();

        max_age = 3600*24*365;

        document.cookie = c_name + '="' + encode64(val) + '";path="/"; max-age=' +  max_age + '; expires="' + exp_date+'"';
    }

    function update_results(league, team) {
     try {
     if ( team === undefined) {
       // show the pick team view.
       $('.pick.' + league).removeClass('hidden');
     } else if ($('.score').filter('.' + team.replace(/ /g, '-')).length > 0) {
       // now show the entire results container.
       $('.results.' + league).removeClass('hidden');

       // hide the pick screen
       $('.pick.' + league).addClass('hidden');

       // add a message about which team rocks.
       var plural = 's';
       if (team.charAt(team.length - 1) === 's') {
         plural = '';
       }
       $('span.team-rocks').replaceWith("<span class='team-rocks'>"
                         + team + " rock" + plural + "!"
                         + " (not <button class='btn btn-primary'"
                         + " onclick='change_team()'"
                         + " value='your team'"
                         + " type='button'>your team</button>?)</span>");
       $('.repick-team').removeClass('hidden');
     } else {
       // show the pick team view.
       $('.pick.' + league).removeClass('hidden');
     }
     } catch(err) {
       $('.pick.' + league).removeClass('hidden');
     }
    }

    function is_first_time() {
        var is_first = getCookie('first_time');

        if (is_first === 'nope') {
            return false;
        }
        return true;
    }

    function update_league(league) {
        try {
            if ((league === undefined) || (league === '')) {
                if (is_first_time()) {
                    $('.intro-text').removeClass('hidden');
                }
                $('.league-select').removeClass('hidden');
            }
            else if ($('.league-block').filter('.' + league).length > 0) {
                update_results(league, getCookie(league));
                $('.intro-text').addClass('hidden');
                $('.league-select').addClass('hidden');
                $('.league-block.' + league).removeClass('hidden');
                $('.repick-league').removeClass('hidden');
            }
        } catch(err) {
            if (is_first_time()) {
                $('.intro-text').removeClass('hidden');
            }
            $('.league-select').removeClass('hidden');
        }
    }

    function reveal_score(league, home, away) {
        $('.score.'+league+'.'+home+'.'+away).removeClass('hidden');
        $('.noscore.'+league+'.'+home+'.'+away).addClass('hidden');
    }

    function initial_league(league) {
        if (league === undefined) {
            var url_path = window.location.pathname.slice(1);
            league = url_path;
            if (url_path === '') {
                league = getCookie('cur_league');
                if (league) {
                    history.pushState({league:league}, league, league);
                } else {
                    history.pushState({league:''}, '/', '/');
                }
            } else {
                setCookie('cur_league', league);
                history.pushState({league:league}, league, league);
            }
        } else if (league !== '') {
            setCookie('cur_league', league);
        }
        update_league(league);
    }

    function pick_league(league) {
        setCookie('first_time','nope');
        setCookie('cur_league', league);
        history.pushState({league:league}, league, league);
        update_league(league);
    }

    function pick_team(league, team) {
        setCookie(league, team);
        update_results(league, team);
    }

    function change_league() {
        var league = getCookie('cur_league');
        delCookie('cur_league');

        if (league) {
            $('.league-block.' + league).addClass('hidden');
            $('.repick-league').addClass('hidden');
            $('.repick-team').addClass('hidden');

            history.pushState({league:''}, '/', '/');
            update_league('');
        }
    }


    function reveal_all() {
        var league = getCookie('cur_league');
        $('td.score .noscore.' + league).addClass('hidden');
        $('td.score .score.' + league).removeClass('hidden');
    }

    $('.btn-revealall').click(reveal_all);

    function reveal_all_but_my_team() {
        var league = getCookie('cur_league');
        var team = getCookie(league);
        var teamclass = team.replace(/ /g, '-');

        $('td.score .noscore.' + league).not('.'+teamclass).addClass('hidden');
        $('td.score .score.' + league).not('.'+teamclass).removeClass('hidden');
    }
    $('.btn-revealnotmyteam').click(reveal_all_but_my_team);

    function change_team() {
        var league = getCookie('cur_league');
        var team = getCookie(league);
        var teamclass = team.replace(/ /g, '-');

        delCookie(league);
        $('.score.' + league).addClass('hidden');
        $('.noscore.' + league).removeClass('hidden');

        $('.results.' + league).addClass('hidden');

        $('.repick-team').addClass('hidden');

        update_results(league, '');
    }

    // Get the whole thing rolling.
    window.onpopstate = function(event) {
        if (event.state) {
            if (event.state.league === '') {
                $('.league-block').addClass('hidden');
                $('.repick-league').addClass('hidden');
                $('.repick-team').addClass('hidden');
                delCookie('cur_league');
            }
            initial_league(event.state.league);
        } else {
            initial_league();
        }
    };
    initial_league();
    </script>
  </body>
</html>
