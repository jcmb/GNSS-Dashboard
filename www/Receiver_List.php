<html>
<head>
<title>GNSS Receivers</title>
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
<H1>GNSS Receivers</H1>

<form name="input" action="Edit_GNSS.php" method="get">

<?php
   include 'error.php.inc';
   include 'db.inc.php';
   include 'security.inc.php';

   $user_id = gnss_require_user_id(new SQLite3($databaseFile));
   echo '<input name="User_ID" type="hidden" value="'.h($user_id).'">';
?>


<?php


   function displayGNSS($result, $user_id)
   {
       // Start a table, with column headers

      echo "\n<table border='1' id=\"Receivers\" class='tablesorter'>\n<thead>\n<tr>\n" .
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
          "\n<th>DynDNS</th>" .
          "\n<th>NTRIP</th>" .
          "\n<th>GLN</th>" .
          "\n<th>GAL</th>" .
          "\n<th>BDS</th>" .
          "\n<th>QZSS</th>" .
          "\n<th>DEL</th>" .
          "\n</tr>\n</thead>\n<tbody>\n";

     // Until there are no rows in the result set,
     // fetch a row into the $row array and ...
     while ($row = @ $result->fetchArray(SQLITE3_ASSOC))
        {
//        var_dump($row);
        // ... start a TABLE row ...
        echo "\n<tr>";

        // ... and print out each of the attributes
        // in that row as a separate TD (Table Data).
       echo '<td><a href="Edit_GNSS.php?GNSS_ID='.h($row["id"]).'&User_ID='. h($user_id).'">Edit</a></td>';
       echo '<td><a href="Edit_GNSS.php?DUP=1&GNSS_ID='.h($row["id"]).'&User_ID='. h($user_id).'">Dup</a></td>';
       echo "\n<td> ".h($row["name"])." </td>";
       echo "\n<td> ".($row["Enabled"]?"Enabled":"Disabled")." </td>";
       echo "\n<td> ".$row["Firmware"]." </td>";
       echo "\n<td> ".$row["Loc_Group"]." </td>";
       echo "\n<td> ".$row["Address"]." </td>";
       echo "\n<td> ".$row["Port"]." </td>";
       echo "\n<td> ";
       switch ($row["Reciever_Type"]) {
          case "112":
            echo "Ag542";
            break;
          case "162":
            echo "Alloy";
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
          case "164":
            echo "BX992-INS";
            break;
          case "509":
            echo "BX992-MS";
            break;
          case "509":
            echo "BX992-SPS";
            break;
          case "193":
            echo "MPS566-2";
            break;
          case "330":
            echo "MP86";
            break;
          case "331":
            echo "MS86";
            break;
          case "138":
            echo "SPS356";
            break;
          case "38":
            echo "SPS850";
            break;
          case "250":
            echo "SPS585";
            break;
          case "59":
            echo "SPS851";
            break;
          case "107":
            echo "SPS852";
            break;
          case "118":
            echo "SPS855";
            break;
          case "101":
            echo "SPS985";
            break;
          case "169":
            echo "SPS986";
            break;
          case "100":
            echo "R10";
            break;
          case "188":
            echo "R750";
            break;
          case "191":
            echo "R750-2";
            break;
          case "327":
            echo "R780";
            break;
          case "329":
            echo "R780-2";
            break;
          case "76":
            echo "NetR9";
            break;

          default:
            echo "Unknown ID ". $row["Reciever_Type"];
       }
       echo " </td>";
       echo "\n<td> ".h(gnss_display_receiver_password($row["Password"]))." </td>";
       echo "\n<td> ".h($row["Pos_Type"])." </td>";
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
       echo "\n<td> ".(!empty($row["DynDNS_Enabled"]) ? $row["DynDNS_Host"] : "Disabled")." </td>";

       // Build accurate NTRIP Status string
       $ntrip_status = array();
       if (!empty($row['NTRIP_Client_1_Enabled']) || !empty($row['NTRIP_Client_2_Enabled']) || !empty($row['NTRIP_Client_3_Enabled'])) $ntrip_status[] = "Client";
       if (!empty($row['NTRIP_Server_1_Enabled']) || !empty($row['NTRIP_Server_2_Enabled']) || !empty($row['NTRIP_Server_3_Enabled'])) $ntrip_status[] = "Server";
       if (!empty($row['NTRIP_Caster_1_Enabled']) || !empty($row['NTRIP_Caster_2_Enabled']) || !empty($row['NTRIP_Caster_3_Enabled'])) $ntrip_status[] = "Caster";

       $ntrip_str = empty($ntrip_status) ? "Disabled" : implode("/", $ntrip_status);
       echo "\n<td> ".$ntrip_str." </td>";
       echo "\n<td> ".($row["GLN"] ? 'True' : 'False') ." </td>";
       echo "\n<td> ".($row["GAL"] ? 'True' : 'False')." </td>";
       echo "\n<td> ".($row["BDS"] ? 'True' : 'False')." </td>";
       echo "\n<td> ".($row["QZSS"] ? 'True' : 'False')." </td>";
       echo '<td><a href="DEL_GNSS.php?GNSS_ID='.h($row["id"]).'&User_ID='. h($user_id).'">Delete</a></td>';

       echo "\n</tr>";

     }

     // Then, finish the table
     echo "\n</tbody>\n</table>\n";
     echo "<p>\n";
  }


// Connect to sqlite

$db = new SQLite3($databaseFile);

if (! $db) {
   die ("Failed to open GNSS.db");
   }

$stmt = $db->prepare('SELECT * FROM GNSS WHERE User_ID=?');
$stmt->bindValue(1, $user_id, SQLITE3_INTEGER);
$result = $stmt->execute();

if (!($result))
  {
  showerror();
  }

displayGNSS($result, $user_id);


  // Close the connection
if (!($db->close()))
  showerror();


?>

<input type="submit" value="Add a GNSS Receiver" />
<p/>

<?php
if ($user_id) {
    echo 'View <a href="/cgi-bin/Dashboard/List_Status.php?User_ID='.h($user_id).'">Receiver Status</a>';
    }
?>
</form>
</div>
</div>
</div>

</html>

