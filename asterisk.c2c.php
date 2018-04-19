<?php
$from = $_GET['from'];
$to = $_GET['to'];

$from = preg_replace('/\+/', '', $from);

if($from == $to) {
print "Invalid number: You cannot call yourself :)\n";
exit;
}


if(strlen($from) >= 10 && strlen($to) >= 10 && is_numeric($to) && is_numeric($from)) {
$socket = fsockopen("127.0.0.1","5038");
fputs($socket, "Action: Login\r\n");
fputs($socket, "Username: admin\r\n");
fputs($socket, "Secret: x\r\n\r\n");
fputs($socket, "Action: originate\r\n");
fputs($socket, "Exten: 8$to\r\n");
fputs($socket, "Context: default\r\n");
fputs($socket, "Channel: Local/8$from\r\n");
fputs($socket, "Priority: 1\r\n");
fputs($socket, "Timeout: 30000\r\n");
fputs($socket, "Callerid: WebCall <$from> to <$to>\r\n\r\n");
fputs($socket, "Action: Logoff\r\n\r\n");

$wrets="";
while (!feof($socket)) {
      $wrets .= fread($socket, 2048);
}
#echo $wrets;
fclose($socket);
print "Calling $to\n";
$err_datetime = date("D M j G:i:s T Y");
error_log("$err_datetime: IP=$_SERVER[REMOTE_ADDR] PHONE #: $from --> $to\n", 3 ,"/var/log/call.log");
} else {

print "Invalid number: $to\n";
}
?>
