<?php
move_uploaded_file($_FILES["up_file"]["tmp_name"], "upload/" . $_FILES["up_file"]["name"]);
header("Access-Control-Allow-Origin:*");
echo json_encode(['img' => 'http://localhost/upload/'.$_FILES["up_file"]["name"]]);