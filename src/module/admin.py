import yaml

def getPages(template,settings,name,page):
	blogdb = getBlogDB()
	index = """
<!DOCTYPE html>
<html>
	<head>
		<title>Admin Page</title>
		<style>
html {
    background-color:#EFEFEF;
    border-top:5px solid #FF9311;
}
.container {
	margin-left:50px;
}
		</style>
	</head>
	<body>
	<a href="/admin" class="nav">Home</a>
<?php

$databases = [%db%];

foreach ($databases as $db) {
	$data = json_decode(file_get_contents($db),TRUE);
	echo "<h1>".$db."</h1>";
	echo "<div class='container'>";
	echo "<a href=\\"edit.php?location=".$db."\\">New Post</a><br/>";
	foreach ($data as $val) {
		echo "<a href=\\"edit.php?location=".$db."&post=".$val["post"]."\\">".$val["title"]."</a><br/>";
	}
	echo "</div>";
}
?>
	</body>
</html>
	"""

	edit = """
<!DOCTYPE html>
<html>
<head>
	<title>Admin</title>
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
		<a href="/admin" class="nav">Home</a>
<?php

if (isset($_GET['location']) && isset($_GET['post'])) {
	$data = json_decode(file_get_contents($_GET['location']), TRUE);
	$out = "";
	foreach ($data[$_GET['post']] as $key => $val) {
		if ($key !== "content") {
			$out = $out . $key . "=" . $val . ", ";
		}
	}
	$_SESSION['vars'] = $out;
	$_SESSION['post'] = $data[$_GET['post']]['content'];
} else {
	$_SESSION['post'] = "";
	$_SESSION['vars'] = "";
	$_GET['location'] = "";
}
?>
		<form id="update" action="./post.php" method="post" onsubmit="return validate();">
			<label>Variables:</label><input id="vars" name="vars" type="text" class="input" value="<?php echo $_SESSION['vars']; ?>"/><input type="submit" id="submit" class="input"/><br />
			<label>Location :</label><input id="loc" name="loc" type="text" class="input" value="<?php echo $_GET['location']; ?>"/><br />
			<textarea id="post" name="post" form="update" class="input"><?php echo $_SESSION['post']; ?></textarea>
		</form>
	</div>
</body>
</html>
"""

	post = """
<!DOCTYPE html>
<html>
	<head>
		<title>Admin</title>
		<style>
html {
	background-color:#EFEFEF;
	border-top:5px solid #FF9311;
}
.example {
	width:700px;
	margin:0 auto;
}
		</style>
	</head>
	<body>
		<a href="/admin" class="nav">Home</a>
<?php
$posts = json_decode(file_get_contents($_POST['loc']),TRUE);
parse_str(str_replace(",", "&", $_POST['vars']), $data);

echo "<div class=\\"example\\">";

$posts[$data["post"]] = array_merge($data,array("content" => $_POST["post"]));
$fp = fopen($_POST['loc'], 'w');
fwrite($fp, json_encode($posts));
fclose($fp);
$output = json_decode(file_get_contents($_POST['loc']),TRUE);
echo $output[$data["post"]]["content"];
echo "</div>";
echo "<hr/>";
echo "<plaintext>". shell_exec("build %destination% -d %root%");
?>
"""

	return {"php:index":index.replace("%db%",blogdb[:-1]),"php:edit":edit,"php:post":post.replace("%root%",settings['root']).replace("%destination%",settings['dest'])}

def getBlogDB():
	dbs = ""

	data = yaml.load(file("pages.yml").read())

	for k,v in data.items():
		for m,md in v['pagemod'].items():
			if md['mod'] == "blog":
				dbs = dbs + "\""+md['settings']['data']+"\","

	return dbs

