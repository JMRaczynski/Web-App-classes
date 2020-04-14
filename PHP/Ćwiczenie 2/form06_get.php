<?php session_start(); ?>
<html>
<head>
    <meta charset=utf-8"/>
</head>
<body>
<?php
     if (isSet($_SESSION['successMessage'])) {
         echo $_SESSION['successMessage'] . "<br>";
         $_SESSION['successMessage'] = null;
     }
    $link = mysqli_connect("localhost", "scott", "tiger", "instytut");
    if (!$link) {
        printf("Connect failed: %s\n", mysqli_connect_error());
        exit();
    }
    $sql = "SELECT * FROM pracownicy";
    $result = $link->query($sql);
    foreach ($result as $v) {
        echo $v["ID_PRAC"]." ".$v["NAZWISKO"]."<br/>";
    }
    $result->free();
    $link->close();
?>
<a href="form06_post.php">Dodaj pracownika</a>
</body>
</html>
