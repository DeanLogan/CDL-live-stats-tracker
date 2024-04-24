import time
from confluent_kafka import Producer, KafkaException

time.sleep(15)

while True:
    bootstrap_servers = 'kafka:9092' 
    print(f'Connecting to {bootstrap_servers}')

    p = Producer({'bootstrap.servers': bootstrap_servers})

    try:
        # Try to flush the messages. If it returns 0, break the loop.
        if p.flush(timeout=10.0) == 0:
            print('Connected successfully.')
            break
    except KafkaException as e:
        print(f'Failed to connect: {e}')
        time.sleep(5)
        continue

i = 0

while True:
    print(f'Producing message {i}')
    p.produce('test', f'message {i}')
    p.flush()
    i += 1
    time.sleep(3)