const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const { deflate } = require('zlib');

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
        ws.send(JSON.stringify(
            {
                message: `Game update ${counter}`,
                players: [
                    {
                        name: 'Player 1',
                        kills: counter,
                        deaths: 1,
                        KD: 0
                    },
                    {
                        name: 'Player 2',
                        kills: 0,
                        deaths: counter,
                        KD: 0
                    }
                ]
            }
        )
    );
    }, 1000);

    ws.on('close', function close() {
        console.log('Client disconnected');
        clearInterval(interval);
    });
});

server.listen(8080, function listening() {
    console.log('Server started on port 8080');
});