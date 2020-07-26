function submit() {
    document.getElementById("main_form").submit();
    }

function clearInputs() {
    var x = document.getElementsByTagName("input");
    var i;
    for (i = 0; i < 81; i++) {
        x[i].value = ''
        }
    }