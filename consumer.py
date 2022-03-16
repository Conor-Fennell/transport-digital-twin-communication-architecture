from kafka import KafkaConsumer
from constants import DECODING, TOPICS, BROKER_EP
import file_tools as file
from multiprocessing import Process

def consume(EP):
     consumer = KafkaConsumer(bootstrap_servers=EP, value_deserializer=DECODING)
     consumer.subscribe(topics=TOPICS)
     for msg in consumer:
          print (msg.value)
          file.writeMessageToFile(msg.partition, msg.topic, msg.value)

if __name__ == '__main__':
     print("Starting consumer...") 
     Process(target=consume, args=(BROKER_EP,)).start()
  
    

     