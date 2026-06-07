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
   include 'security.inc.php';
   $db = new SQLite3($databaseFile);

   if ($Editing) {
      $user_id = gnss_require_user_id($db);
      $stmt = $db->prepare('SELECT * FROM Users WHERE id=?');
      $stmt->bindValue(1, $user_id, SQLITE3_INTEGER);
      $result = $stmt->execute();
      if (!($result))
         {
         showerror();
         }
      $row = $result->fetchArray(SQLITE3_ASSOC);
      $csrf_user = (string)$user_id;
      }
   else {
      echo "Add User";
      $Editing=FALSE;
      $csrf_user = "new";
      }
?>

</H1>

<form name="input" action="/cgi-bin/Dashboard/Do_Edit_User.py" method="post">

<?php
if ($Editing) {
   echo '<input name="User_ID" type="hidden" value="'.h($user_id).'">';
   }
echo gnss_csrf_field($csrf_user);
?>

<table border="0">
<tr><td>
Name:
</td><td>
<input name="Name" type="text" value="<?php echo h($row["Name"] ?? '') ?>"/>
</td></tr>

<tr><td>
Email:
</td><td>
<input name="Email" type="text" value="<?php echo h($row["Email"] ?? '')?>"/>
</td></tr>

<tr><td>
Password:
</td><td>
<input name="Password" type="password" value="" placeholder="Leave blank to keep current password"/>
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


