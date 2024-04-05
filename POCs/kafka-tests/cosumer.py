# the below code does not work due to a version problem with kafka-python as it does not currently support python 3.12.2 

# from kafka import KafkaConsumer

# consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
# for msg in consumer:
#     print (msg)

from confluent_kafka import Consumer, KafkaException

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['test'])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            print('Received message: {}'.format(msg.value().decode('utf-8')))

except KeyboardInterrupt:
    pass

finally:
    c.close()