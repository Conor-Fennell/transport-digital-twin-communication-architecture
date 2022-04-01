from kafka import KafkaConsumer
from constants import DECODING, TOPICS, BROKER_EP
import file_tools as file
from multiprocessing import Process
from network_test_helper import run_ping_tests
import time

def consume(EP):
     consumer = KafkaConsumer(bootstrap_servers=EP, value_deserializer=DECODING)
     consumer.subscribe(topics=TOPICS)
     print("Consumer is running...")
     for msg in consumer:  
          latency = (time.time() - float(msg.value['sent_timestamp']))*1000    
          file.writeLatencyToFile(msg.topic, latency)
          file.writeMessageToFile(msg.partition, msg.topic, msg.value)

if __name__ == '__main__':
     print("Starting consumer...") 
     Process(target=consume, args=(BROKER_EP, )).start()
     Process(target=run_ping_tests).start()
     
  
    

     