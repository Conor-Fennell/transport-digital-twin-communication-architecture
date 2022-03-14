from kafka import KafkaConsumer, KafkaProducer
from constants import DECODING, ENTERPRISE_TOPICS, BROKER_EP, ENTERPRISE_EP, ENCODING, TOPIC_LOOKUP

consumer = KafkaConsumer(bootstrap_servers=ENTERPRISE_EP, value_deserializer=DECODING)
print("Starting enterprise consumer...") 
producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING)
print("Starting enterprise producer...") 
consumer.subscribe(topics=ENTERPRISE_TOPICS)
for msg in consumer:
    print(msg)
    producer.send(TOPIC_LOOKUP[msg.topic], msg.value)