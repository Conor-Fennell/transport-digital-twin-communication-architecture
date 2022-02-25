from kafka import KafkaConsumer
from variables import BROKER_EP, DECODING, TOPIC
import time

print("Starting consumer...")
consumer = KafkaConsumer(bootstrap_servers=BROKER_EP, value_deserializer=DECODING)
consumer.subscribe(topics=TOPIC)
for msg in consumer:
     print (msg.value)
     print('Message end to end time: ', round(((time.time() - msg.value['time'])*1000), 3), 'ms')