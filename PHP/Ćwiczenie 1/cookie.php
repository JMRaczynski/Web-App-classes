<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head>
    <title>PHP</title>
    <meta charset='UTF-8' />
</head>
<body>
<?php
    if (isSet($_GET["utworzCookie"])) {
        echo $_GET["czas"];
        setcookie("CIASTKO", "2000", time() + $_GET["czas"], "/");
    }
?>
<h1> COOOOOOOOKIE</h1>
<a href="index.php">WSTECZ</a>
</body>
</html>