function startTime() {
	var today = new Date();

	var h = today.getHours();
	var m = today.getMinutes();
	var s = today.getSeconds();
	m = checkTime(m);
	s = checkTime(s);

	var pm = false
	if (h > 12) {
		h -= 12;
		pm = true;
	}

	document.getElementById('txt').innerHTML = "<p style=\"text-align:center;\"><font size=\"18\">"+h+":"+m+":"+s+" "+((pm)?"PM":"AM")+"</font></p>";
	var t = setTimeout(function(){startTime()}, 500);
}

function checkTime(i) {
	if (i < 10) {i = "0" + i};
	return i;
}