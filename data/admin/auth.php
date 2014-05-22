<?php
$config = json_decode(file_get_contents("./config.json"),TRUE);
$user = "root";
$pass = "";
$con = mysqli_connect($config['db_hostname'],$config['db_username'],$config['db_password'],$config['db_name']);
var_dump($_POST);
if (isset($_POST['u']) && isset($_POST['p'])) {
    if (!isset($_POST['new'])) {
        $guser = mysql_real_escape_string($_POST['u']);
        echo 'SELECT hash, username FROM usr WHERE username = "'.$guser.'"';
        $user = mysqli_query($con,'SELECT hash, username FROM usr WHERE `username` = "$guser"');
        $user = mysqli_fetch_array($user);
        if ( crypt($_POST['p'], $user['hash']) == $user['hash'] ) {
            echo "Yes!";
        } else {
            
        }
    } else {
        $sth = $dbh->prepare('
        INSERT INTO usr (username, hash)
        VALUES (:user, :hash)
        ');
        $username = $_POST['u'];
        $hash = crypt($_POST['p']);
        $sth->bindParam(':user',$username);
        $sth->bindParam(':hash',$hash);
        $sth->execute();
        echo "$hash, $username";
    }
}
?>