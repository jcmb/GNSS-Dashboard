<html>
<head>
<title>GNSS Receivers Errors &amp; Warnings</title>
<link rel="stylesheet" type="text/css" href="/Dashboard/style.css"></link>
<link rel="stylesheet" type="text/css" href="/Dashboard/tcui-styles.css">
<body class="page">
<div class="container clearfix">
  <div style="padding: 10px 10px 10px 0 ;"> <a href="http://construction.trimble.com/">
        <img src="/Dashboard/trimble-logo.png" alt="Trimble Logo" id="logo"> </a>
      </div>
</div>
<div id="top-header-trim"></div>
<div id="content-area">
<div id="content">
<div id="main-content" class="clearfix">

<H1>GNSS Receivers Errors and Warnings</H1>

<?php
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';
   include 'security.inc.php';
   $user_id = gnss_require_user_id(new SQLite3($databaseFile));
?>

<p>Errors and Warnings is temporarily unavailable due to a receiver firmware change.</p>
<p><a href="/cgi-bin/Dashboard/List_Status.php?User_ID=<?php echo h($user_id); ?>">Back to Receiver Dashboard</a></p>

</div>
</div>
</div>
</body>
</html>
