function submit() {
    document.getElementById("main_form").submit();
    }

function clearInputs() {
    let x = document.getElementsByTagName("input");
    let i;
    for (i = 0; i < 81; i++) {
        console.log(x[i]);
        x[i].value = '';
        }
    }
function sendData() {
    let httpRequest = new XMLHttpRequest();
    let form = document.getElementById("main_form");
    let myForm = new FormData(form);
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === 4) {
                fillInValues(httpRequest.response)
                }
            }
    httpRequest.open('POST', '/');
    httpRequest.send(myForm)
    }

function fillInValues(results) {
    let obj = JSON.parse(results);
    let j = document.getElementsByName("(7, 6)");
    console.log(j.item(0));
    for (var prop in obj) {
        let j = document.getElementsByName(prop)[0];
        j.value = obj[prop];
    }
}
