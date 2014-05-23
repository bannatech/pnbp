<?php
$PASSWD = "notapassword";
require_once 'markdown.php';
session_start();
if ($_POST['password'] == md5($PASSWD . $_SESSION['salt'])) {
    $posts = json_decode(file_get_contents($_POST['loc']),TRUE);
    parse_str(str_replace(",", "&", $_POST['vars']), $data);
    echo "SUCESS <br />";
    $posts[$data["post"]] = array_merge($data,array("content" => Parsedown::instance()->parse($_POST["post"])));
    $fp = fopen($_POST['loc'], 'w');
    fwrite($fp, json_encode($posts));
    fclose($fp);
    $output = json_decode(file_get_contents($_POST['loc']),TRUE);
    echo $output[$data["post"]]["content"];
}
?>
