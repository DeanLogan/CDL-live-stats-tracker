const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

wss.on('connection', function connection(ws) {
    console.log('Client connected');

    ws.on('message', function incoming(message) {
        console.log('received: %s', message);
    });

    // Sending message to the client every second
    let counter = 0;
    const interval = setInterval(() => {
        counter++;
        ws.send(JSON.stringify({ message: `Hello from server! Message number: ${counter}` }));
    }, 1000);

    ws.on('close', function close() {
        console.log('Client disconnected');
        clearInterval(interval);
    });
});

server.listen(8080, function listening() {
    console.log('Server started on port 8080');
});