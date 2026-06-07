<html>
<head>
<title>GNSS Receivers Errors & Warnings</title>
<link rel="stylesheet" type="text/css" href="/Dashboard/style.css"></link>
<link rel="stylesheet" type="text/css" href="/Dashboard/tcui-styles.css">
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="/Dashboard/jquery.tablesorter.min.js"></script>
<body class="page">
<div class="container clearfix">
  <div style="padding: 10px 10px 10px 0 ;"> <a href="http://construction.trimble.com/">
        <img src="/Dashboard/trimble-logo.png" alt="Trimble Logo" id="logo"> </a>
      </div>
  <!-- end #logo-area -->
</div>
<div id="top-header-trim"></div>
<div id="content-area">
<div id="content">
<div id="main-content" class="clearfix">


<style>

table.tablesorter tbody td.Issue {
    color: red;
}

</style>

<script>
$(document).ready(function()
    {
        $("#Receivers").tablesorter();
    }
);
</script>


</head>
<body>

<H1>GNSS Receivers Errors and Warnings</H1>

<?php
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';
   include 'security.inc.php';
   $user_id = gnss_require_user_id(new SQLite3($databaseFile));
?>


   function displayGNSSErrors($result, $user_id)
   {
       // Start a table, with column headers

      echo "\n<table border='1' id=\"Receivers\" class=\"tablesorter\">\n<thead><tr>\n" .
          "\n<th>ID</th>" .
          "\n<th>Details</th>" .
          "\n<th>Download</th>" .
          "\n<th>Clone</th>" .
          "\n<th>Name</th>" .
          "\n<th>Firmware Release</th>" .
          "\n<th>Group</th>" .
          "\n<th>IP</th>" .
          "\n<th>Port</th>" .
          "\n<th>Type</th>" .
          "\n<th>Password</th>" .
          "\n<th>Errors</th>" .
          "\n<th>Warnings</th>" .
          "\n<th>Clear</th>" .
          "\n</tr></thead><tbody>";

     // Until there are no rows in the result set,
     // fetch a row into the $row array and ...
     while ($row = @ $result->fetchArray(SQLITE3_ASSOC))
        {
        if (!$row["Enabled"] ) {
            continue;
            }

        if ($row["Firmware"] == "EOL" ) {
            continue;
            }
//        var_dump($row);
        // ... start a TABLE row ...
        echo "\n<tr>";

        // ... and print out each of the attributes
        // in that row as a separate TD (Table Data).
       $action_base = '/cgi-bin/Dashboard/Do_Receiver_Errors.py?User_ID=' . urlencode((string)$user_id) . '&GNSS_ID=' . urlencode((string)$row["id"]);
       echo "\n<td> ".h($row["id"])." </td>";
       echo '<td><a href="' . h($action_base . '&action=view') . '">View</a>';
       echo '<td><a href="' . h($action_base . '&action=download') . '">Download</a>';
       echo '<td><a href="' . h($action_base . '&action=clone') . '">Clone</a>';
       echo "\n<td> ".h($row["name"])." </td>";
       echo "\n<td> ".$row["Firmware"]." </td>";
       echo "\n<td> ".$row["Loc_Group"]." </td>";
       echo "\n<td> ".$row["Address"]." </td>";
       echo "\n<td> ".$row["Port"]." </td>";
       echo "\n<td> ";
       switch ($row["Reciever_Type"]) {
          case "38":
            echo "SPS850";
            break;
          case "59":
            echo "SPS851";
            break;
          case "76":
            echo "NetR9";
            break;
          case "100":
            echo "R10";
            break;
          case "101":
            echo "SPS985";
            break;
          case "107":
            echo "SPS852";
            break;
          case "118":
            echo "SPS855";
            break;
          case "138":
            echo "SPS356";
            break;
          case "162":
            echo "Alloy";
            break;
          case "169":
            echo "SPS986";
            break;
          case "188":
            echo "R750";
            break;
          case "240":
            echo "BD935";
            break;
          case "248":
            echo "Brewster Upgradable";
            break;
          case "249":
            echo "Brewster Heading";
            break;
          case "250":
            echo "SPS585";
            break;
          case "509":
            echo "BX992-SPS";
            break;

          default:
            echo "Unknown ID ". $row["Reciever_Type"];
       }
       echo " </td>";
       echo "\n<td> ".h(gnss_display_receiver_password($row["Password"]))." </td>";
       echo "\n<td> ".h($row["Errors"])." </td>";
       echo "\n<td> ".h($row["Warnings"])." </td>";
       echo "\n<td>";
       echo '<form style="display:inline" method="post" action="/cgi-bin/Dashboard/Do_Receiver_Errors.py">';
       echo '<input type="hidden" name="User_ID" value="'.h($user_id).'">';
       echo '<input type="hidden" name="GNSS_ID" value="'.h($row["id"]).'">';
       echo '<input type="hidden" name="action" value="clear">';
       echo gnss_csrf_field((string)$user_id);
       echo '<input type="submit" value="Clear">';
       echo '</form></td>';

       echo "\n</tr>";

     }

     // Then, finish the table
     echo "\n</tbody></table>\n";
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

$stmt = $db->prepare('SELECT * FROM GNSS JOIN STATUS on GNSS.id = STATUS.id WHERE User_ID=?');
$stmt->bindValue(1, $user_id, SQLITE3_INTEGER);
$result = $stmt->execute();

if (!($result))
  {
  showerror();
  }

displayGNSSErrors($result, $user_id);


  // Close the connection
if (!($db->close()))
  showerror();


?>

</div>
</div>
</div>

</html>

