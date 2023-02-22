const express = require('express');
const { Kafka } = require('kafkajs');

const app = express();
const kafka = new Kafka({
  clientId: 'my-app2',
  brokers: ['kafka:29092'],
});

const consumer = kafka.consumer({ groupId: 'test-group' });

const run = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'events', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log({
        value: message.value.toString(),
      });
    },
  });
};

run().catch(console.error);

const port = 7003;
app.listen(port, () => {
  console.log(`Consumer is listening on port ${port}`);
});
