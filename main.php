<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Saylua Dungeon Demo</title>
  <meta name="description" content="A new virtual petsite. ">
  <meta name="author" content="Saylua">

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.1/css/font-awesome.min.css">
  <link rel="stylesheet" href="static/css/styles.min.css">
  <script src="static/js/main.min.js"></script>
  <script src="static/js/dungeon.min.js"></script>

  <link href='https://fonts.googleapis.com/css?family=Kaushan+Script' rel='stylesheet' type='text/css'>
  <!--[if lt IE 9]>
  <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]-->
</head>

<body>
<div id="logo" class="container">
    <a href="#">Saylua</a>
</div>
<div id="navbar" class="container">
  <div class="content-width">
    <a href="#">Home</a>
    <a href="#">Explore</a>
    <a href="#">Adopt</a>
    <a href="#">Games</a>
    <a href="#">Whatever</a>

    <form class="search" action="/search.php">
      <input type="text" placeholder="Seach Saylua">
      <button><i class="fa fa-search" aria-hidden="true"></i></button>

    </form>
  </div>
</div>
<div class="container">
  <div class="content">
    <div class="sidebar left" id="left-bar">
      <img src="static/img/ha.jpg">
    </div>
    <div class="sidebar right" id="right-bar">
      Your Party
      <img src="static/img/SHC.png" class="left">
      <img src="static/img/SHC.png" style="width: 50%;" class="left">
      <img src="static/img/SHC.png" style="width: 50%;" class="left">
    </div>
    <div class="page-area">
      <div class="notification error">Error: You are too awesome. </div>

      <div class="random-event">
        <h3>Woah, a thing is happening! </h3>
        <p>You found some gum on the bottom of your shoe. </p>
      </div>

  	  <div id="dungeon"></div>
    </div>
  </div>
</div>

<div class="container footer">
  <div class="content-width">
    <p>
      <a href="#">Back to Top</a> &bull;
      <a href="#">About</a> &bull;
      <a href="#">Terms of Service</a> &bull;
      <a href="#">Contact Us</a> &bull;
      <a href="#">Staff</a>
    </p>
    <p>
      &copy; 2016 Saylua
    </p>
  </div>
</div>
<div class="clearfix"></div>
</body>
</html>
