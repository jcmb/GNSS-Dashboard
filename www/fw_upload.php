<html>
<head>
</head>
<body>
<h1>Upload Firmware Files</h1>


<script type="text/javascript">

function check_file(file_control,name) {
   console.log("Checking file " + file_control);
   var input = document.getElementById(file_control);
   console.log(input);
   console.log(input.files);
   if (input.value == "") {
      alert("You must select a file to upload for receivers of type "+name)
      return false
      }
   return true
   }
   
          

  function check_files() {
  return check_file("GamelUpload","SPS855") && 
         check_file("RockyUpload","SPS985") && 
         check_file("TennisBallUpload","SPS585") && 
         check_file("MetallicaUpload","SPS356") && 
         check_file("ZeppelinUpload","BD935"); 
  }
</script>

<form method="post" action="do_fw_upload.php" enctype="multipart/form-data" onsubmit="return check_files()">
<p><strong>Firmware Information:</strong> <br>

<?php
//var_dump($row);

echo '<input name="User_ID" type="hidden" value="'.$_REQUEST["User_ID"] . '">';
?>

<table>
<tr>
<td>
Firmware Level:
</td><td>
<select required name="Firmware">
  <option value="Released">Released</option>
  <option value="Beta" >Beta</option>
  <option value="Branch" selected>Branch</option>
  <option value="Trunk">Trunk</option>
</select>
</td>
</tr>
<tr>
<td>
Firmware Version:
</td><td>
<input name="version" type="text"><br/>
</td>
</tr>
</table>

<?php
$User_ID=$_REQUEST["User_ID"];
if ($User_ID=="") {
    exit ("Internal Error: No User ID");
    }

?>

<p><strong>Upload Files:</strong> <br>

<table width="100%">
<tr>
<td width="33%">
SPS852/SPS855: (Gamel)
</td>
<td width="67%">
<input size="50" type="file" name="GamelUpload" id="GamelUpload" accept=".timg" required/></br>
</td>
</tr>
<tr>
<td>
SPS356: (Metallica)
</td><td>
<input size="50" type="file" name="MetallicaUpload" id="MetallicaUpload" accept=".timg" required/></br>
</td>
</tr>
<tr>
<tr>
<td>
SPS985: (Rockhopper)
</td><td>
<input size="50" type="file" name="RockyUpload" id="RockyUpload" accept=".timg"  required/></br>
</td>
</tr>
<td>
SPS585: (TennisBall)
</td><td>
<input size="50" type="file" name="TennisBallUpload" id="TennisBallUpload" accept=".timg" required/></br>
</td>
</tr>
<tr>
<td>
BD935: (Zeppelin)
</td><td>
<input size="50" type="file" name="ZeppelinUpload" id="ZeppelinUpload" accept=".timg" required/></br>
</td>
</tr>
</table>

<input type="submit">
</form>


</body>
</html>
