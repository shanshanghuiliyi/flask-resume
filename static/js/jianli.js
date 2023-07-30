AOS.init({
	anchorPlacement: 'top-left',
	duration: 1000
});
window.onload = function() {
	var file = document.getElementById("file");
	var image = document.getElementById("image");
	window.imgclick = function() {
		file.click();
	}
	file.onchange = function() {
		var files = event.target.files,
			file;
		var URL = window.URL || window.webkitURL;
		var imgURL = URL.createObjectURL(files[0]);
		image.src = imgURL;
	}
}
