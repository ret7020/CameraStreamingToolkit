var img = document.getElementById("liveImg");
var wsProtocol = (location.protocol === "https:") ? "wss://" : "ws://";

var ws = new WebSocket(wsProtocol + location.host + "/image");
ws.binaryType = 'arraybuffer';
var data;
let last_time = performance.now();
ws.onmessage = (evt) => {
	data = new Uint8Array(evt.data);
	data = pako.ungzip(data);
	img.src = window.URL.createObjectURL(new Blob([data], { type: "image/jpeg" }));
	console.log(1 / ((performance.now() - last_time) / 1000))
	last_time = performance.now();

}
