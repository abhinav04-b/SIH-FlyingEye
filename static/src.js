var i = 0;
var txt = "Where Innovation Meets Cultivation: Drones for Smarter Agriculture."
;
var speed = 50;

function typeWriter() {
    if (i < txt.length) {
      document.getElementById("m_abt").innerHTML += txt.charAt(i);
      i++;
      setTimeout(typeWriter, speed);
    }
  }

window.onload = typeWriter;

function openNewFile() {
  window.open('chat.html');
}