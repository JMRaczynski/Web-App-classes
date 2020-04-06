<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head>
    <title>PHP</title>
    <meta charset='UTF-8' />
</head>
<body>
<?php
    require("funkcje.php");
    if (isSet($_POST["zaloguj"])) {
        $login = test_input($_POST["login"]);
        $haslo = test_input($_POST["haslo"]);

        if (strcmp($login, $osoba1->login) == 0 && strcmp($haslo, $osoba1->haslo) == 0) {
            $_SESSION['zalogowanyImie'] = $osoba1->imieNazwisko;
            $_SESSION['zalogowany'] = 1;
            header("Location: user.php");
        }
        else if (strcmp($login, $osoba2->login) == 0 && strcmp($haslo, $osoba2->haslo) == 0) {
            $_SESSION['zalogowanyImie'] = $osoba2->imieNazwisko;
            $_SESSION['zalogowany'] = 1;
            header("Location: user.php");
        }
        else {
            header("Location: index.php");
        }
        //echo "Przesłany login: " . $login . "<br>";
        //echo "Przesłane hasło: " . $haslo . "<br>";
    }
    ?>
</body>
</html>