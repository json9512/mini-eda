const express = require('express');
const { Kafka } = require('kafkajs');

const app = express();
const kafka = new Kafka({
  clientId: 'producer',
  brokers: ['kafka:29092'],
});

const admin = kafka.admin();

const run = async () => {
  await admin.connect();
  await admin.createTopics({
    topics: [{ topic: 'test-topic', numPartitions: 1 }],
    waitForLeaders: true,
  });
  await admin.disconnect();
};

run().catch(console.error);

app.get('/topics', async (req, res) => {
  const topics = await kafka.admin().listTopics();
  res.json(topics);
});

app.get('/topics/:topic/messages', async (req, res) => {
  const topic = req.params.topic;
  const consumer = kafka.consumer({ groupId: 'test-group' });
  await consumer.connect();
  await consumer.subscribe({ topic, fromBeginning: true });
  let messages = [];
  await consumer.run({
    eachMessage: async ({ message }) => {
      messages.push({
        value: message.value.toString(),
        timestamp: message.timestamp,
      });
    },
  });
  await consumer.disconnect();
  res.json(messages);
});

app.post('/topics', async (req, res) => {
  const topic = req.body.topic;
  const topics = [{ topic, numPartitions: 1 }];
  await admin.createTopics({ topics });
  res.send(`Created topic: ${topic}`);
});

app.post('/topics/:topic', async (req, res) => {
  const topic = req.params.topic;
  const message = req.body.message;
  const producer = kafka.producer();
  await producer.connect();
  await producer.send({
    topic,
    messages: [{ value: message }],
  });
  await producer.disconnect();
  res.send(`Published message: ${message}`);
});

const port = 7001;
app.listen(port, () => {
  console.log(`Producer server listening at http://localhost:${port}`);
});
