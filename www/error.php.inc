<?php
/*
Source code example for Web Database Applications

Unless otherwise stated, the source code distributed with this book can be
redistributed in source or binary form so long as an acknowledgment appears
in derived source files.
The citation should list that the code comes from Hugh E.
Williams and David Lane, "Web Database Application with PHP and MySQL"
published by O'Reilly & Associates.
This code is under copyright and cannot be included in any other book,
publication, or educational product without permission from O'Reilly &
Associates.
No warranty is attached; we cannot take responsibility for errors or fitness
for use.
*/
?>

<?php

   error_reporting (E_ALL);   

   function showerror()
   {
//      die("Error " . mysql_errno() . " : " . mysql_error());
	
//      print "Database is in use, try again soon";
      die("Database is in use, try again soon");
   }
?>
