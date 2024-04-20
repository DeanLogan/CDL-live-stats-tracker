import time
from confluent_kafka import Producer

bootstrap_servers = 'kafka:9092' 
print(f'Connecting to {bootstrap_servers}')

p = Producer({'bootstrap.servers': bootstrap_servers})

while True:
    print("what")
    p.produce('test', 'message every 15 seconds')
    p.flush()
    time.sleep(15)