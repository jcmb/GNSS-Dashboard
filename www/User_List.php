<html>
<head>
<title>GNSS Receiver System Users</title>
</head>
<body>
<H1>User List</H1>
<form name="input" action="Edit_User.php" method="get">


<?php
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';
   include 'security.inc.php';

   if (empty($_REQUEST['User_ID'])) {
      die('Internal Error: Missing User ID');
   }
   gnss_require_user_id(new SQLite3($databaseFile));

   function displayUsers($result)
   {
      echo "\n<table border='1'>\n<tr>\n" .
          "\n<th>ID</th>".
          "\n<th>Name</th>" .
          "\n<th>Email</th>" .
          "\n</tr>";

     while ($row = @ $result->fetchArray(SQLITE3_ASSOC))
        {
        echo "\n<tr>";
       echo '<td><a href="Edit_User.php?User_ID='.h($row["ID"]).'">Edit</a></td>';
       echo "\n<td> ".h($row["Name"])." </td>";
       echo "\n<td> ".h($row["Email"])." </td>";
       echo "\n</tr>";

     }

     echo "\n</table>\n";
     echo "<p>\n";
  }


$db = new SQLite3($databaseFile); 

if (! $db) {
   die ("Failed to open GNSS.db");
   }

$result = $db->query("SELECT * FROM Users");

if (!($result))
  {
  showerror();
  }

displayUsers($result);

if (!($db->close()))
  showerror();


?>

<input type="submit" value="Add a user" />
<p/>
</form>
</body>
</html>
