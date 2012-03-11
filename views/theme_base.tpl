<!DOCTYPE html>
<html lang="en-us">
    <head>
        <meta charset="utf-8" />
        <title>{{title}}</title>
        <!-- HTML5 shim, for IE6-8 support of HTML elements -->
        <!--[if lt IE 9]>
            <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->
          <link rel="shortcut icon" href="{{ get_url('static', path='favicon.ico') }}" />
          <link rel="stylesheet" href="{{ get_url('static', path='css/bootstrap.css') }}">
          <link href="{{ get_url('static', path="css/bootstrap-responsive.css") }}" rel="stylesheet">

          <style type="text/css">
            body {
              padding-top: 60px;
              padding-bottom: 40px;
            }
          </style>

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
          <a class="brand" href="#">{{ sitename }}</a>
          <div class="nav-collapse">
            <ul class="nav">
              <li class="active"><a href="{{get_url('index')}}">Home</a></li>
            </ul>
          </div><!--/.nav-collapse -->
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
    </body>
</html>
