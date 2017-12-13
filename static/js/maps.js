var modal = document.getElementById('sidemodal');

var btn = document.getElementById('modalopen');

var span = document.getElementById("closemodal");

btn.onclick = function(){
    sidemodal.style.display = "block";
};

span.onclick = function() {
    sidemodal.style.display = "none";
};

window.onclick = function(event) {
    if (event.target === sidemodal) {
        sidemodal.style.display = "none";
    }
};