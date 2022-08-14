<html>
<head>
<title>GNSS Receivers for Upgrading</title>
<link rel="stylesheet" type="text/css" href="/Dashboard/style.css"></link>
<link rel="stylesheet" type="text/css" href="/Dashboard/tcui-styles.css">
<style>
.td_header{text-align:center;font-weight:bold;}
</style>

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

<script>
function AdjustSelections(val) {
//   alert(val);
   $(".Released").prop( "checked", val=="Released");
   $(".Beta").prop( "checked", val=="Beta" );
   $(".Branch").prop( "checked", val=="Branch" );
   $(".Trunk").prop( "checked", val=="Trunk");
   $(".Beta").prop( "checked", val=="Beta" || val=="Released");
   $(".Branch").prop( "checked", val=="Branch" || val=="Beta" || val=="Released");
//   $(".Trunk").prop( "checked", val=="Trunk");
}

function AllOff() {
//   alert(val);
   $(".Released").prop( "checked", false);
   $(".Beta").prop( "checked", false);
   $(".Branch").prop( "checked", false);
   $(".Trunk").prop( "checked", false);
}

function AllOn() {
//   alert(val);
   $(".Released").prop( "checked", true);
   $(".Beta").prop( "checked", true);
   $(".Branch").prop( "checked", true);
   $(".Trunk").prop( "checked", true);
}
</script>

</head>
<body>
<H1>GNSS Receivers</H1>
<form name="input" action="/cgi-bin/Dashboard/Upgrade_GNSS.py" method="get">

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


   // Connect to sqlite

   $db = new SQLite3($databaseFile);

   if (! $db) {
      die ("Failed to open GNSS.db");
      }
   //$handle = sqlite_open($db) or die("Could not open database");
   //if (!(mysql_select_db($databaseName, $connection)))
   //  showerror();

   $query = 'SELECT * FROM Firmware;';

   $result = $db->query($query);

   if (!($result))
     {
     showerror();
     }

      // Display the results

   $versions=array();
   while ($row = @ $result->fetchArray(SQLITE3_ASSOC))
        {
        $versions[$row["Type"]]=$row["Version"];
//        var_dump($versions);
//        print "<br/>";
        }
?>

Upgrade To:
<select required name="Firmware" onchange="AdjustSelections(this.value)">
  <option value="Released">Released (<?php echo $versions["Released"]?>)</option>
  <option value="Beta">Beta (<?php echo $versions["Beta"]?>)</option>
  <option value="Branch">Branch (<?php echo $versions["Branch"]?>)</option>
  <option selected value="Trunk">Trunk (<?php echo $versions["Trunk"]?>)</option>
</select>
<p/>


<?php
   function displayGNSSForUpgrade($result)
   {
       // Start a table, with column headers

      echo "\n<table border='1'>\n<tr>\n" .
          "\n<th>Upgrade</th>".
          "\n<th>Name</th>" .
          "\n<th>Firmware Release</th>" .
          "\n<th>Group</th>" .
          "\n</tr>";

     // Until there are no rows in the result set,
     // fetch a row into the $row array and ...
     $Current_Loc=""; //The ungrouped ones come first in the search

     while ($row = @ $result->fetchArray(SQLITE3_ASSOC))
        {
//        var_dump($row);
        // ... start a TABLE row ...
        if ($row["Loc_Group"] != $Current_Loc) {
           echo "\n<tr>";
           echo "\n<td colspan=\"4\" class=\"td_header\"> ".$row["Loc_Group"]." </td>";
           echo "\n</tr>";
           $Current_Loc = $row["Loc_Group"];
           }
        echo "\n<tr>";

        // ... and print out each of the attributes
        // in that row as a separate TD (Table Data).
       echo '<td><input type="checkbox" class="' .$row["Firmware"].'" name="Upgrade_'.$row["id"].'">Upgrade</td>';
       echo "\n<td> ".$row["name"]." </td>";
       echo "\n<td> ".$row["Firmware"]." </td>";
       echo "\n<td> ".$row["Loc_Group"]." </td>";
       echo "\n</tr>";

     }

     // Then, finish the table
     echo "\n</table>\n";
     echo "<p>\n";
  }


// Run the query on the connection

$query = "SELECT * FROM GNSS WHERE User_ID=" . $_REQUEST["User_ID"]. " ORDER BY Loc_Group";


$result = $db->query($query);

if (!($result))
  {
  showerror();
  }

   // Display the results
displayGNSSForUpgrade($result);


  // Close the connection
if (!($db->close()))
  showerror();


?>

<button type="button" onclick="AllOff()">Unselect all</button>
<button type="button" onclick="AllOn()">Select all</button>
<br/>
<input type="submit" value="Upgrade GNSS Receivers" />
<p/>
</form>

<script>
$( document).ready(function() {

//   alert( "welcome" );
   AdjustSelections("Trunk");
   });

</script>
</div>
</div>
</div>
</body>
</html>
