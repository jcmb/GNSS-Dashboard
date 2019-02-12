<html>
<head>
<title>GNSS Receiver System Users</title>
</head>
</head>
<body>
<H1>User List</H1>
<form name="input" action="Edit_User.php" method="get">


<?php
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';


   function displayUsers($result)
   {
       // Start a table, with column headers

      echo "\n<table border='1'>\n<tr>\n" .
          "\n<th>ID</th>".
          "\n<th>Name</th>" .
          "\n<th>Email</th>" .
          "\n</tr>";

     // Until there are no rows in the result set,
     // fetch a row into the $row array and ...
     while ($row = @ $result->fetchArray(SQLITE3_ASSOC))
        {
//        var_dump($row);
        // ... start a TABLE row ...
        echo "\n<tr>";
        // ... and print out each of the attributes
        // in that row as a separate TD (Table Data).
       echo '<td><a href="Edit_User.php?User_ID='.$row["ID"].'">Edit</a></td>';
       echo "\n<td> ".$row["Name"]." </td>";
       echo "\n<td> ".$row["Email"]." </td>";
       echo "\n</tr>";

     }

     // Then, finish the table
     echo "\n</table>\n";
     echo "<p>\n";
  }


// Connect to sqlite

$db = new SQLite3($databaseFile); 

if (! $db) {
   die ("Failed to open GNSS.db");
   }
//$handle = sqlite_open($db) or die("Could not open database");
//if (!(mysql_select_db($databaseName, $connection)))
//  showerror();

// Run the query on the connection

$query = "SELECT * FROM Users";

$result = $db->query($query);

if (!($result))
  {
  showerror();
  }

   // Display the results
displayUsers($result);


  // Close the connection
if (!($db->close()))
  showerror();


?>

<input type="submit" value="Add a user" />
<p/>
</form>
