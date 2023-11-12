var img = document.getElementById("liveImg");
var curr_fps = document.getElementById("current_fps");
var lowest_fps = document.getElementById("lowest_fps");
var peak_fps = document.getElementById("peak_fps");
var avg_fps = document.getElementById("avg_fps");

var wsProtocol = (location.protocol === "https:") ? "wss://" : "ws://";

var ws = new WebSocket(wsProtocol + location.host + "/image");
ws.binaryType = 'arraybuffer';
var data;
let ll_fps = 1000;
let pk_fps = -1;
let cr_fps;

let fps_sum = 0;
let fps_count = 0;

let last_time = performance.now();
ws.onmessage = (evt) => {
	data = new Uint8Array(evt.data);
	data = pako.ungzip(data);
	img.src = window.URL.createObjectURL(new Blob([data], { type: "image/jpeg" }));
	cr_fps = ~~(1 / ((performance.now() - last_time) / 1000)); 
	curr_fps.innerHTML = cr_fps;
	if (ll_fps > cr_fps){
		ll_fps = cr_fps;
		lowest_fps.innerHTML = ll_fps;
	}
	if (pk_fps < cr_fps && cr_fps < 70){
		pk_fps = cr_fps;
		peak_fps.innerHTML = pk_fps;
	}
	fps_sum += cr_fps;
	fps_count += 1;
	if (fps_count > 100){
		fps_sum = 0;
		fps_count = 0;
		console.log("Flushing avg")

	}
	avg_fps.innerHTML = ~~(fps_sum / fps_count);

	last_time = performance.now();

}
