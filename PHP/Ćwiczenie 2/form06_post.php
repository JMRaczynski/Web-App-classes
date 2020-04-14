<?php session_start(); ?>
<html>
<head>
    <meta charset=utf-8"/>
</head>
<body>
<?php
    if (isset($_SESSION['errorMessage'])) {
        echo $_SESSION['errorMessage'] . "<br>";
        $_SESSION['errorMessage'] = null;
    }
?>
<form action="form06_redirect.php" method="POST">
    id_prac <input type="text" name="id_prac">
    nazwisko <input type="text" name="nazwisko">
    <input type="submit" value="Wstaw">
    <input type="reset" value="Wyczysc">
</form>
<a href="form06_get.php">Lista pracowników</a>
</body>
</html>
