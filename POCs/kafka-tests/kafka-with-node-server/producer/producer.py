import time
from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'localhost:9092'})

while True:
    p.produce('test', 'message every 15 seconds')
    p.flush()
    time.sleep(15)