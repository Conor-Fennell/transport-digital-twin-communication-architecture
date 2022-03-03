from kafka import KafkaConsumer
from constants import BROKER_EP, DECODING, TOPICS
import file_tools as file

print("Starting consumer...")
consumer = KafkaConsumer(bootstrap_servers=BROKER_EP, value_deserializer=DECODING)
consumer.subscribe(topics=TOPICS)
for msg in consumer:
     print (msg)
     file.writeMessageToFile(msg.partition, msg.topic, msg.value)

     