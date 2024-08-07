const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const { deflate } = require('zlib');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const CLAN_TAGS_TO_DISPLAY_NAME = {
    "itori": "Toronto Ultra",
    "iseai": "Seattle Surge",
    "ilati": "Los Angeles Thieves",
    "iatli": "Atlanta Faze",
    "itxi": "Optic Texas",
    "inyi": "New York Subliners",
    "ilvi": "Vegas Legion",
    "icari": "Carolina Royal Ravens",
    "ilagi": "Los Angeles Guerrillas",
    "ibosi": "Boston Breach",
    "imiai": "Miami Heretics",
    "imini": "Minnesota Rokkr"
};

wss.on('connection', function connection(ws) {
    console.log('Client connected');

    ws.on('message', function incoming(message) {
        const parsedMessage = JSON.parse(message);
        let team1Name = CLAN_TAGS_TO_DISPLAY_NAME[parsedMessage.team1];
        let team2Name = CLAN_TAGS_TO_DISPLAY_NAME[parsedMessage.team2];
        let team1Arr = [];
        let team2Arr = [];
        console.log('received: %s', message);
        
        const playerDataForTables = {};

        for (const key in parsedMessage.kills) {
            if (parsedMessage.kills.hasOwnProperty(key)) {
                let name = key.substring(4, key.length - 1);
                playerDataForTables[name] = {
                    name: name,
                    kills: parsedMessage.kills[key],
                    deaths: 0,
                    kd: 0,
                };
            }
        }
        
        for (const key in parsedMessage.deaths) {
            if (parsedMessage.deaths.hasOwnProperty(key)) {
                let name = key.substring(4, key.length - 1);
                playerDataForTables[name].deaths = parsedMessage.deaths[key];
                playerDataForTables[name].kd = playerDataForTables[name].kills / parsedMessage.deaths[key];
                if (parsedMessage.team1.includes(name)) {
                    team1Arr.push(playerDataForTables[name]);
                } else {
                    team2Arr.push(playerDataForTables[name]);
                }
            }
        }

        // Send message to the client
        ws.send(JSON.stringify({
            message: 'Game update',
            team1Name: team1Name,
            team2Name: team2Name,
            team1: team1Arr,
            team2: team2Arr
        }));
    });

    ws.on('close', function close() {
        console.log('Client disconnected');
    });
});

server.listen(8080, function listening() {
    console.log('Server started on port 8080');
});