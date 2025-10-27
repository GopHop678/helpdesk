document.addEventListener('DOMContentLoaded', function() {
    const socket = new WebSocket("ws://" + window.location.host + "/ws/tmp/");
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log('Received data: ');
        console.log(data);
    }
});