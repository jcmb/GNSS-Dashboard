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


   function displayGNSSErrors($result)
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
       echo "\n<td> ".$row["id"]." </td>";
       echo '<td><a href="/cgi-bin/Dashboard/View_Error?HOST='.$row["Address"]."&PORT=".$row["Port"]."&USER=admin&PASS=".$row["Password"]."&NAME=".$row["name"].'">View</a>';
       echo '<td><a href="/cgi-bin/Dashboard/Download_Error?HOST='.$row["Address"]."&PORT=".$row["Port"]."&USER=admin&PASS=".$row["Password"]."&NAME=".$row["name"].'">Download</a>';
       echo '<td><a href="/cgi-bin/Dashboard/Download_Clone?HOST='.$row["Address"]."&PORT=".$row["Port"]."&USER=admin&PASS=".$row["Password"]."&NAME=".$row["name"].'">Clone</a>';
       echo "\n<td> ".$row["name"]." </td>";
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
          case "508":
            echo "BX992-MS";
            break;
          case "509":
            echo "BX992-SPS";
            break;

          default:
            echo "Unknown ID ". $row["Reciever_Type"];
       }
       echo " </td>";
       echo "\n<td> ".$row["Password"]." </td>";
       echo "\n<td> ".$row["Errors"]." </td>";
       echo "\n<td> ".$row["Warnings"]." </td>";
       echo "\n".'<td><a target="_blank" href="/cgi-bin/Dashboard/Delete_Errors?HOST='.$row["Address"]."&PORT=".$row["Port"]."&USER=admin&PASS=".$row["Password"]."&NAME=".$row["name"]."&ID=".$row["id"].'">Delete</a>';

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

$query = "SELECT * FROM GNSS JOIN STATUS on GNSS.id = STATUS.id WHERE User_ID=" . $_REQUEST["User_ID"];

$result = $db->query($query);

if (!($result))
  {
  showerror();
  }

   // Display the results
displayGNSSErrors($result);


  // Close the connection
if (!($db->close()))
  showerror();


?>

</div>
</div>
</div>

</html>

