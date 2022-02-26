from kafka import KafkaConsumer
from constants import BROKER_EP, DECODING, TOPIC

print("Starting consumer...")
consumer = KafkaConsumer(bootstrap_servers=BROKER_EP, value_deserializer=DECODING)
consumer.subscribe(topics=TOPIC)
for msg in consumer:
     print (msg.value)
     