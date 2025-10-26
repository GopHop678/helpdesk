document.addEventListener('DOMContentLoaded', function() {
    const socket = new WebSocket("ws://localhost:8000/ws/tmp/");
    socket.onmessage = function(event) {
        console.log(JSON.parse(event.data));
    }
});