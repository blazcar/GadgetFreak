function dodajTemo() {
	var ul = document.getElementById("teme_foruma");
	  var li = document.createElement("li");
	  var ime = document.getElementById("ime_nove_teme").value;
	  var a = document.createTextNode("a");
	  a.textContent = ime;
	  li.appendChild(a);
	  ul.appendChild(li);
}