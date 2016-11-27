

function dodajTemo() {
	var ul = document.getElementById("teme_foruma");
	  var li = document.createElement("li");
	  var ime = document.getElementById("ime_nove_teme").value;
	  var a = document.createTextNode("a");
	  a.textContent = ime;
	  li.appendChild(a);
	  ul.appendChild(li);
}


function poslji_novo_objavo(){
	var string = "<div class = \"post samsung\">\
              <div class = \"tekst_objave\">\
                <a class = \"wholePost\" href=\"lookPost.html\">More</a>\
                <p class = \"Title\">" + document.getElementById("naslov_objave").value+"</p>\
                <p>" + document.getElementById("teskt_nove_objave").value + "</p>\
                <textarea name=\"comment\" required placeholder=\"Vaš komentar\"></textarea>\
                <input class=\"button_comment\" type=\"submit\" value=\"Komentiraj!\"/>\
              </div>\
          </div>";

	document.getElementById("popular_posts_regUser").innerHTML += string;


}	
