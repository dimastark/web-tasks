var state = false;
setInterval(checkuser, 1);

function erase() {
	state = false;
	document.getElementById("user_res").style.background = 'red';
}

function gettime() {
    var xmlhttp = new XMLHttpRequest();
	xmlhttp.open('GET', 'http://localhost:8080/time');
	xmlhttp.onreadystatechange = function () {
		if (xmlhttp.readyState !== 4) {
			return;
		}

		res.innerText = xmlhttp.responseText;
	}

	xmlhttp.send();
}

function checkuser() {
    var xmlhttp = new XMLHttpRequest();
    var name = document.getElementById("user_name").value;
	xmlhttp.open('GET', 'http://localhost:8080/user/' + name);
	xmlhttp.onreadystatechange = function () {
		if (!state) {
			if (xmlhttp.readyState !== 4) {
				return;
			}
			state = xmlhttp.responseText == 'True';
			if (state) {
				document.getElementById("user_res").style.background = 'green';
			}
		}
	}

	xmlhttp.send();
}
