from kafka import KafkaConsumer, KafkaProducer
from constants import DECODING, BROKER_EP, ENTERPRISE_EP, ENCODING, TOPIC_LOOKUP
from kafka_helper import getPartition
from multiprocessing import Process

def consume(producerEP, consumerEP, topic, linger):
     producer = KafkaProducer(bootstrap_servers=producerEP, value_serializer=ENCODING, linger_ms=linger)
     consumer = KafkaConsumer(bootstrap_servers=consumerEP, value_deserializer=DECODING)
     consumer.subscribe(topics=topic)

     print(topic[0], "server running...")
     for msg in consumer:  
          producer.send(TOPIC_LOOKUP[msg.topic], msg.value, partition=getPartition(msg))

if __name__ == '__main__':
     Process(target=consume, args=(BROKER_EP, ENTERPRISE_EP, ["enterprise_motorway_cameras"], 0)).start() 
     Process(target=consume, args=(BROKER_EP, ENTERPRISE_EP, ["enterprise_toll_bridge_cameras"], 0)).start()
     Process(target=consume, args=(BROKER_EP, ENTERPRISE_EP, ["enterprise_probe_vehicles"], 0)).start()