<?php
include("./smtp.php");

$x = new Smtp("smtp.office365.com",25,true,"ad_xyz@outlook.com","mr021009%");
$r=$x->sendmail("1204543076@qq.com","ad_xyz@outlook.com","Test","Test","hhh","TXT");
print_r($r);
?>