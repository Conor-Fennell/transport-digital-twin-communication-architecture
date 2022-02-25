from kafka import KafkaProducer
from variables import BROKER_IP, ENCODING, TOPIC
import time

print("Starting producer...")

try:
    producer = KafkaProducer(bootstrap_servers=BROKER_IP, value_serializer=ENCODING)
    print("Connected to broker at: ", BROKER_IP)
    while True:
        data = {
            'msg': 'Hello world',
            'time': time.time()
        }
        producer.send(TOPIC, data)
        print(data)
        time.sleep(5)

except:
    print("Connection to broker failed")

