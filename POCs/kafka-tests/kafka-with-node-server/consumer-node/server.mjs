const express = require("express");
const { Kafka } = require("kafkajs");

const app = express();
const port = 3000;

const kafka = new Kafka({
    clientId: 'my-app',
    brokers: ['kafka:9092']
});

const consumer = kafka.consumer({ groupId: 'test-group' });

const run = async () => {
    await consumer.connect();
    await consumer.subscribe({ topic: 'test', fromBeginning: true });

    await consumer.run({
        eachMessage: async ({ message }) => {
        const newData = JSON.parse(message.value.toString());
        console.log(newData);
        },
    });
};

run().catch(console.error);

app.get('/', (req, res) => {
    res.send('Welcome to my server!');
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
