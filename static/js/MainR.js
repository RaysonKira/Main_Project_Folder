var modal = document.getElementById('sidemodal');

var btn = document.getElementById('modalopen');

var span = document.getElementById("closemodal");

btn.onclick = function() {
    sidemodal.style.display = "block";
}

span.onclick = function() {
    sidemodal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == sidemodal) {
        sidemodal.style.display = "none";
    }
}

  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyBkxo8edLZyfwLJhTZ1K7KXzzpAA3VWxq0",
    authDomain: "mynotawesomeproject-81927.firebaseapp.com",
    databaseURL: "https://mynotawesomeproject-81927.firebaseio.com",
    projectId: "mynotawesomeproject-81927",
    storageBucket: "",
    messagingSenderId: "1009685214434"
  };
  firebase.initializeApp(config);

  var database = firebase.database();
  var red = database.ref("Emails");

  // var email =