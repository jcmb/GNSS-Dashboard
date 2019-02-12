<html>
<head>
<title>
<?php
if ($_REQUEST["User_ID"]) {
   echo "Edit User";
   $Editing=TRUE;
   }
else {
   echo "Add User";
   $Editing=FALSE;
   }
?>
</title>
</head>
<body>
<H1>

<?php
   error_reporting(E_ALL);
   include 'error.php.inc';
   include 'db.inc.php';
   $db = new SQLite3($databaseFile);

   if ($Editing) {
        // create a new table in the file  
      $query="SELECT * FROM Users WHERE id='".$_REQUEST["User_ID"]."'";
   //   echo $query;
      $result = $db->query($query);
      if (!($result))
         {
         showerror();
         }     
      $row = $result->fetchArray(SQLITE3_ASSOC);
      }
   else {
      echo "Add User";
      $Editing=FALSE;
#      $row=[];
   }
?>

</H1>

<form name="input" action="/cgi-bin/Dashboard/Do_Edit_User.py" method="get">

<?php
//var_dump($row);

echo '<input name="User_ID" type="hidden" value="'.$_REQUEST["User_ID"] . '">';
$User_ID=$_REQUEST["User_ID"];
?>
<p/>

<form name="input" action="/cgi-bin/Dashboard/Do_Edit_User.py" method="get">

<table border="0">
<tr><td>
Name:
</td><td>
<input name="Name" type="text" value="<?php echo $row["Name"] ?>"/>
</td></tr>

<tr><td>
Email:
</td><td>
<input name="Email" type="text" value="<?php echo $row["Email"]?>"/>
</td></tr>

<tr><td>
Password:
</td><td>
<input name="Password" type="password" value="<?php echo $row["Loc_Group"]?>"/>
</td></tr>


</table>

<?php
if ($Editing ) {
   echo '<input type="submit" value="Edit User" />';
   }
else {
   echo '<input type="submit" value="Add User" />';
   }
echo '<p/>';

echo '<a href="User_List.php">Back</a>';

if ($Editing) {
   $db->close();
   }
?>

</form>
</body>
</html>



