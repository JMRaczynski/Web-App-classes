<?php session_start(); ?>
<!DOCTYPE html>
<html>
<head>
    <title>PHP</title>
    <meta charset='UTF-8' />
</head>
<body>
<?php
    require_once("funkcje.php");
    if (isset($_SESSION["zalogowany"])) {
        if ($_SESSION["zalogowany"] == 1) {
            echo "Zalogowano<br>";
            echo $_SESSION["zalogowanyImie"] . "<br>";
        }
        else header("Location: index.php");
    }
    else header("Location: index.php");
    if (isSet($_POST["wrzuc"])) {
        $currentDir = getcwd();
        $uploadDirectory = "/";
        $fileName = $_FILES['myfile']['name'];
        $fileSize =$_FILES['myfile']['size'];
        $fileTmpName = $_FILES['myfile']['tmp_name'];
        $fileType = $_FILES['myfile']['type'];
        if ($fileName != "" and
            ($fileType == 'image/png' or $fileType == 'image/jpeg'
                or $fileType == 'image/jpeg' or $fileType == 'image/PNG')) {
            $uploadPath = $currentDir . $uploadDirectory . $fileName;
            if (move_uploaded_file($fileTmpName, $uploadPath)) {
                echo "Zdjecie zostało załadowane na serwer";
            }
        }
    }
?>
<a href="index.php">INDEX</a>
<form action='user.php' method='POST' enctype='multipart/form-data'>
    <fieldset>
        <legend>Obrazek:</legend>
        <input name="myfile" type="file">
        <button type="submit" name="wrzuc" value="wrzuc">Wrzuc</button>
    </fieldset>
</form>
<img src="kek.jpg" alt="Ratajczak">
<form action="index.php" method="post">
    <fieldset>
        <legend>Wyloguj:</legend>
    <button type="submit" name="wyloguj" value="wyloguj">Wyloguj</button>
    </fieldset>
</form>
</body>
</html>