import time
from confluent_kafka import Producer

bootstrap_servers = 'kafka:9092' 
print(f'Connecting to {bootstrap_servers}')

p = Producer({'bootstrap.servers': bootstrap_servers})

while True:
    p.produce('test', 'message every 1 second')
    p.flush()
    print('message sent')
    time.sleep(1)