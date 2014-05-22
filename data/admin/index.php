<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin</title>
    <script type="text/javascript" src="./scripts/md5.js"></script>
    <style>
html {
    background-color:#EFEFEF;
    border-top:5px solid #FF9311;
}
#wrapper {
    width:800px;
    margin:0 auto;
}
#wrapper label {
    font-family:Consolas, Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono, monospace, serif;
}
#post {
    width:100%;
    height:1000px;

}
#submit {
    background-color:#EFEFEF;
}
#submit:hover {
    box-shadow:0px 0px 3px black inset;
}
#submit:active {
    background-color:#AAEEFF;
}
.input {
    outline:none;
    padding:5px;
    border:1px solid #DEDEDE;
    border-radius:5px;
    box-shadow:0px 0px 3px #DEDEDE inset;
}
    </style>
</head>
<body>
    <div id="wrapper">
<?php

if (isset($_GET['location']) && isset($_GET['post'])) {
  require_once( dirname( __FILE__) . '/HTML_To_Markdown.php' );
  $data = json_decode(file_get_contents($_GET['location']), TRUE);
  $out = "";
  foreach ($data[$_GET['post']] as $key => $val) {
    if ($key !== "content") {
      $out = $out . $key . "=" . $val . ", ";
    }
  }
  $_SESSION['vars'] = $out;
  $_SESSION['post'] = new HTML_To_Markdown($data[$_GET['post']]['content']);
}
?>
        <form id="update" action="./post.php" method="post" onsubmit="return validate();">
            <label>Password :</label><input id="password" name="password" type="password" class="input"/><input type="submit" id="submit" class="input"/><br />
            <label>Variables:</label><input id="vars" name="vars" type="text" class="input" value="<?php echo $_SESSION['vars']; ?>"/><br />
            <label>Location :</label><input id="loc" name="loc" type="text" class="input" value="<?php echo $_GET['location']; ?>"/><br />
            <textarea id="post" name="post" form="update" class="input"><?php echo $_SESSION['post']; ?></textarea>
        </form>
    </div>
    <script type="text/javascript">
function validate() {
    document.getElementById("password").value = md5(document.getElementById("password").value + <?php
            function generateRandomString($length = 10) {
                $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
                $randomString = '';
                for ($i = 0; $i < $length; $i++) {
                    $randomString .= $characters[rand(0, strlen($characters) - 1)];
                }
                return $randomString;
            }
            $_SESSION['salt'] = generateRandomString(10);
            $salt = $_SESSION['salt'];
            echo "'$salt'";
            ?>);
    return true;
}
    </script>
</body>
</html>
