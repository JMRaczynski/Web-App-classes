<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head>
    <title>PHP</title>
    <meta charset='UTF-8' />
</head>
<body>
<?php
    echo "<h1>Nasz system</h1>";
    if (isSet($_POST["wyloguj"])) {
        $_SESSION['zalogowany'] = 0;
        header("Location: index.php");
    }
    if (isset($_COOKIE["CIASTKO"])) {
        echo $_COOKIE["CIASTKO"];
    }
?>
<form action="logowanie.php" method="post">
    <fieldset>
        <legend>Credentials:</legend>
        <label>
            Login <input type="text" name="login">
        </label><br>
        <label>
            Hasło <input type="password" name="haslo">
        </label><br>
    <button type="submit" name="zaloguj">Zaloguj</button>
    </fieldset>
</form>
<form action="cookie.php" method="get">
    <fieldset>
        <legend>Ciastko:</legend>
    <input type="number" name="czas">
    <button type="submit" name="utworzCookie">Utworz Cookie</button>
    </fieldset>
</form>
<a href="user.php">USER</a>
</body>
</html>