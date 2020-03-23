function checkString(str) {
    return /^[\s\t\r\n]*$/.test(str);
}

function isEmailInvalid(str) {
    let email = /^[a-zA-Z_0-9\.]+@[a-zA-Z_0-9\.]+\.[a-zA-Z][a-zA-Z]+$/;
    if (email.test(str))
        return false;
    else {
        return true;
    }
}

function checkStringAndFocus(obj, msg, validatingFunction) {
    let str = obj.value;
    let errorFieldName = "e_" + obj.name.substr(2, obj.name.length);
    if (validatingFunction(str)) {
        document.getElementById(errorFieldName).innerHTML = msg;
        obj.focus();
        return false;
    }
    else {
        document.getElementById(errorFieldName).innerHTML = "";
        return true;
    }
}

function validate(form) {
    return checkStringAndFocus(form.elements["f_imie"], "Podaj imię", checkString) &&
        checkStringAndFocus(form.elements["f_nazwisko"], "Podaj nazwisko", checkString) &&
        checkStringAndFocus(form.elements["f_kod"], "Podaj kod pocztowy", checkString) &&
        checkStringAndFocus(form.elements["f_ulica"], "Podaj ulicę", checkString) &&
        checkStringAndFocus(form.elements["f_miasto"], "Podaj miasto", checkString) &&
        checkStringAndFocus(form.elements["f_email"], "Podaj właściwy email", isEmailInvalid);
}

function showElement(elementId) {
    document.getElementById(elementId).style.visibility = 'visible';
}
function hideElement(elementId) {
    document.getElementById(elementId).style.visibility = 'hidden';
}

function alterRows(i, e) {
    if (e) {
        if (i % 2 == 1) {
            e.setAttribute("style", "background-color: Aqua;");
        }
        e = e.nextSibling;
        while (e && e.nodeType != 1) {
            e = e.nextSibling;
        }
        alterRows(++i, e);
    }
}

function nextNode(e) {
    while (e && e.nodeType != 1) {
        e = e.nextSibling;
    }
    return e;
}
function prevNode(e) {
    while (e && e.nodeType != 1) {
        e = e.previousSibling;
    }
    return e;
}
function swapRows(b) {
    let tab = prevNode(b.previousSibling);
    let tBody = nextNode(tab.firstChild);
    let lastNode = prevNode(tBody.lastChild);
    tBody.removeChild(lastNode);
    let firstNode = nextNode(tBody.firstChild);
    tBody.insertBefore(lastNode, firstNode);
}

function cnt(form, msg, maxSize) {
    if (form.value.length > maxSize) form.value = form.value.substring(0, maxSize);
    else msg.innerHTML = maxSize - form.value.length;
}

submitButton = document.querySelectorAll("input[type=submit]")[0];
/*submitButton.onclick = function () {   TO DZIALA PRAWIDLOWO I FORMULARZ SIE NIE WYSYLA
    return validate(this.form);
};*/
submitButton.addEventListener('click', function(event) {
    // return validate(this.form); A TO NIE I FORMULARZ SIE WYSYLA, DLACZEGO?! (zmarnowałem na to 1,5h...)
    if (!validate(this.form)) event.preventDefault(); // A to na szczęście tak
});
womanButton = document.querySelectorAll("input[value=f_k]")[0];
manButton = document.querySelectorAll("input[value=f_m]")[0];
womanButton.onclick = function() {
    showElement("NazwiskoPanienskie");
};
manButton.onclick = function() {
    hideElement("NazwiskoPanienskie");
};

alterRows(1, document.getElementsByTagName("tr")[0]);

magicButton = document.getElementById("magicButton");
magicButton.onclick = function() {
    swapRows(magicButton);
}

