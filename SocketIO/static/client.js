var img = document.getElementById("liveImg");

var socket = io();
socket.on('connect', function() {
	console.log("Connected");
});
socket.on('img', (...args) => {
	data = new Uint8Array(args[0]);
	//data = pako.ungzip(data);
	img.src = window.URL.createObjectURL(new Blob([data], { type: "image/jpeg" }));
	
});

