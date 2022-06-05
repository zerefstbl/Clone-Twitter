let loadUserData = () => {
	return (
		JSON.parse(localStorage.getItem("data")) || {
			loggedInUser: "null",
			loggedInName: "null"
		}
	);
};

let appState = loadUserData();

const getData = async () => {

	document.getElementById("displayHandle").innerText =
		`@${appState.loggedInUser}`;
	document.getElementById("displayName").innerText =
		`${appState.loggedInName}`;
}

getData();

let textArea = document.getElementById('contentsBox');
let tweetList = []
let id = 0;

let countChar = () => {
	let remainingChar = 140 - textArea.value.length;
	if (remainingChar < 0) {
		document.getElementById('charCountArea').innerHTML = `${remainingChar}`.fontcolor('red');

	} else {
		document.getElementById('charCountArea').innerHTML = `${remainingChar}`.fontcolor('white');

	}
}

textArea.addEventListener('input', countChar);

function showNotifications() {
	const container = document.getElementById('notification-container'); if (container.classList.contains('d-none')) {
		container.classList.remove('d-none');
	} else {
		container.classList.add('d-none')
	}
}

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
function removeNotification(removeNotificationURL, redirectURL) {
	var xmlhttp = new XMLHttpRequest();
	const csrftoken = getCookie('csrftoken');
	xmlhttp.onreadystatechange = function () {
		if (xmlhttp.readyState == XMLHttpRequest.DONE) {
			if (xmlhttp.status == 200) {
				window.location.replace(redirectURL);
			}
			else {
				alert('There was an error.');
			}
		}
	};
	xmlhttp.open("DELETE", removeNotificationURL, true);
	xmlhttp.setRequestHeader("X-CSRFToken", csrftoken)
	xmlhttp.send();
}
