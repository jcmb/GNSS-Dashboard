<html>
<head>
<title>GNSS Receivers</title>
<link rel="stylesheet" type="text/css" href="/Dashboard/style.css"></link>
<link rel="stylesheet" type="text/css" href="/Dashboard/tcui-styles.css">
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="/jquery.tablesorter.min.js"></script>
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
<H1>GNSS Receivers</H1>

<form name="input" action="Edit_GNSS.php" method="get">

<?php
if ($_REQUEST["User_ID"]) {
    echo '<input name="User_ID" type="hidden" value="'.$_REQUEST["User_ID"] . '">';
    }
else {
    die ("Internal Error: Missing User ID");
   }
?>


<?php
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';


   function displayGNSS($result)
   {
       // Start a table, with column headers

      echo "\n<table border='1' id=\"Receivers\" class='tablesorter'>\n<tr>\n" .
          "\n<th>EDIT</th>".
          "\n<th>DUP</th>".
          "\n<th>Name</th>" .
          "\n<th>Enabled</th>" .
          "\n<th>Firmware Release</th>" .
          "\n<th>Group</th>" .
          "\n<th>IP</th>" .
          "\n<th>Port</th>" .
          "\n<th>Type</th>" .
          "\n<th>Password</th>" .
          "\n<th>Pos Type</th>" .
          "\n<th>Static</th>" .
          "\n<th>Logging</th>" .
          "\n<th>Email</th>" .
          "\n<th>Auth</th>" .
          "\n<th>NTRIP</th>" .
          "\n<th>IBSS</th>" .
          "\n<th>GLN</th>" .
          "\n<th>GAL</th>" .
          "\n<th>BDS</th>" .
          "\n<th>QZSS</th>" .
          "\n<th>DEL</th>" .
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
       echo '<td><a href="Edit_GNSS.php?GNSS_ID='.$row["id"].'&User_ID='. $_REQUEST["User_ID"].'">Edit</a></td>';
       echo '<td><a href="Edit_GNSS.php?DUP=1&GNSS_ID='.$row["id"].'&User_ID='. $_REQUEST["User_ID"].'">Dup</a></td>';
       echo "\n<td> ".$row["name"]." </td>";
       echo "\n<td> ".($row["Enabled"]?"Enabled":"Disabled")." </td>";
       echo "\n<td> ".$row["Firmware"]." </td>";
       echo "\n<td> ".$row["Loc_Group"]." </td>";
       echo "\n<td> ".$row["Address"]." </td>";
       echo "\n<td> ".$row["Port"]." </td>";
       echo "\n<td> ";
       switch ($row["Reciever_Type"]) {
          case "118":
            echo "SPS855";
            break;
          case "107":
            echo "SPS852";
            break;
          case "101":
            echo "SPS985";
            break;
          case "169":
            echo "SPS986";
            break;
          case "138":
            echo "SPS356";
            break;
          case "248":
            echo "Brewster Upgradable";
            break;
          case "249":
            echo "Brewster Heading";
            break;
          case "38":
            echo "SPS850";
            break;
          case "59":
            echo "SPS851";
            break;
          case "240":
            echo "BD935";
            break;
          case "250":
            echo "SPS585";
            break;

          default:
            echo "Unknown ID ". $row["Reciever_Type"];
       }
       echo " </td>";
       echo "\n<td> ".$row["Password"]." </td>";
       echo "\n<td> ".$row["Pos_Type"]." </td>";
       echo "\n<td> ".($row["Static"] ? 'True' : 'False')." </td>";
       if ($row["Logging_Enabled"] == 0 ) {
           echo "\n<td> Disabled </td>";
           }
       else {
           echo "\n<td> ".$row["Logging_Duration"]."m, ".$row["Logging_Position_Interval"].", ".$row["Logging_Measurement_Interval"]." </td>";
           }

       if ($row["Email_Enabled"] == 0 ) {
           echo "\n<td> Disabled </td>";
           }
        else {
           echo "\n<td> ".$row["Email_To"]." </td>";
           }

       echo "\n<td> ".$row["Auth"]." </td>";
       echo "\n<td> ".($row["NTRIP_Enabled"] ? 'True' : 'False') ." </td>";
       echo "\n<td> ".($row["IBSS_Enabled"] ? 'True' : 'False') ." </td>";
       echo "\n<td> ".($row["GLN"] ? 'True' : 'False') ." </td>";
       echo "\n<td> ".($row["GAL"] ? 'True' : 'False')." </td>";
       echo "\n<td> ".($row["BDS"] ? 'True' : 'False')." </td>";
       echo "\n<td> ".($row["QZSS"] ? 'True' : 'False')." </td>";
       echo '<td><a href="DEL_GNSS.php?GNSS_ID='.$row["id"].'&User_ID='. $_REQUEST["User_ID"].'">Delete</a></td>';

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

$query = "SELECT * FROM GNSS WHERE User_ID=" . $_REQUEST["User_ID"];


$result = $db->query($query);

if (!($result))
  {
  showerror();
  }

   // Display the results
displayGNSS($result);


  // Close the connection
if (!($db->close()))
  showerror();


?>

<input type="submit" value="Add a GNSS Receiver" />
<p/>

<?php
if ($_REQUEST["User_ID"]) {
    echo 'View <a href="/cgi-bin/Dashboard/List_Status.php?User_ID='.$_REQUEST["User_ID"].'">Receiver Status</a>';
    }
?>
</form>
</div>
</div>
</div>

</html>

