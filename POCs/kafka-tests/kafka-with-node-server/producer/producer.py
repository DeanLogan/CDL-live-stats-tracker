import time
from confluent_kafka import Producer

bootstrap_servers = 'localhost:9092' 
print(f'Connecting to {bootstrap_servers}')

p = Producer({'bootstrap.servers': bootstrap_servers})

while True:
    p.produce('test', 'message every 15 seconds')
    print('message sent')
    p.flush()
    time.sleep(15)