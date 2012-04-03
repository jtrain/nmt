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
        <div class="container">
          <a class="brand" href="{{ get_url('index') }}">{{ sitename }}</a>
          <div class="repick repick-league navbar-text">Change your <a class='label label-info' href="{{ get_url('index') }}">League</a></div>
          <div class="repick repick-team navbar-text"><span class='team-rocks'>You rock!</span></div>
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
     
     

     var league = window.location.pathname.slice(1);
     var team = getCookie(league);
     try {
     if ( team === undefined) {
       // show the pick team view.
       $('.pick').removeClass('hidden');
     } else if ($('.score').filter('.' + team.replace(/ /g, '-')).length > 0) {
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
       var switchurl = "'/" + league + "/switch'";
       $('span.team-rocks').replaceWith("<span class='team-rocks'>"
                         + team + " rock" + plural + "!"
                         + " (not <a class='label label-info' href=" + switchurl
                         + " title='change teams'>your team</a>?)</span>");
     } else {
       // show the pick team view.
       $('.pick').removeClass('hidden');
     }
     } catch(err) {
       $('.pick').removeClass('hidden');
     }
       
    </script>
  </body>
</html>
