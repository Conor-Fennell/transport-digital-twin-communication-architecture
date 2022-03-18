from kafka import KafkaConsumer, KafkaProducer
from constants import DECODING, BROKER_EP, ENTERPRISE_EP, ENCODING, TOPIC_LOOKUP, CAMERA_LOOKUP
from kafka_helper import getPartition


consumer = KafkaConsumer(bootstrap_servers=ENTERPRISE_EP, value_deserializer=DECODING)
print("Starting enterprise consumer...") 

producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING, linger_ms=5000)
print("Starting enterprise producer...") 

consumer.subscribe(topics=["enterprise_toll_bridge_cameras"])

for msg in consumer:
    print(msg.value)
    producer.send(TOPIC_LOOKUP[msg.topic], msg.value, partition=getPartition(msg))