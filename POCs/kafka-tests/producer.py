# the below code does not work due to a version problem with kafka-python as it does not currently support python 3.12.2 

# import time
# from kafka import KafkaProducer

# producer = KafkaProducer(bootstrap_servers='localhost:9092')

# for i in range(100):
#     producer.send('test', b'message %d' % i)
#     time.sleep(1)

import time
from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'localhost:9092'})

for i in range(100):
    p.produce('test', 'message %d' % i)
    p.flush()
    time.sleep(1)