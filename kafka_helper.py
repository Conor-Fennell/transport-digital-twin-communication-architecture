from sumo_helper import getLoopLaneCounts, getProbeData, getProbeVehicleIDs, getCamVehicleIDs, getCamData, getTollData, getTollVehicleIDs, getTollData, getLoopData
from constants import CAMERA_LOOKUP, BROKER_EP, ENTERPRISE_EP, ENTERPRISE_TOPICS, ENCODING
from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewPartitions, NewTopic
import traci, time
import numpy as np

def createTopics(TOPICS, broker):
    admin_client = KafkaAdminClient(bootstrap_servers=broker)
    admin_client.create_topics(new_topics=TOPICS, validate_only=False)
    print("Created topics in ", broker)
    for topic in TOPICS:
        print(topic.name)
        print("partitions:", get_partitions_number(broker, topic.name))

def appendTopics(topics, numPartitions, topic_name):
    topics.append(NewTopic(name=topic_name, num_partitions=numPartitions, replication_factor=1))
    return topics

def delete_topics(topics, broker):
    admin_client = KafkaAdminClient(bootstrap_servers=broker)
    try:
        admin_client.delete_topics(topics=topics)
    except  Exception as e:
        print(e)

def get_partitions_number(broker, topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=broker
    )
    partitions = consumer.partitions_for_topic(topic)
    return len(partitions)

def initTopics():
    for topic in list(KafkaConsumer(bootstrap_servers=BROKER_EP).topics()):
        delete_topics([topic], BROKER_EP)

    for topic in list(KafkaConsumer(bootstrap_servers=ENTERPRISE_EP).topics()):
        delete_topics([topic], ENTERPRISE_EP)

    topics = []
    enterprise_topics = []

    topics = appendTopics(topics, 2, "inductive_loops")
    topics = appendTopics(topics, 8, "motorway_cameras")
    topics = appendTopics(topics, 1, "toll_bridge_cameras")
    topics = appendTopics(topics, 1, "probe_vehicles")  

    for topic in ENTERPRISE_TOPICS:
        enterprise_topics = appendTopics(enterprise_topics, 1, topic)

    createTopics(topics, BROKER_EP)     
    createTopics(enterprise_topics, ENTERPRISE_EP)
        
def getPartition(msg):
    if msg.topic == 'enterprise_motorway_cameras':
        return CAMERA_LOOKUP[msg.value['camera_id']]["partition"]
    return None

def createNewPartitions(SERVER, TOPIC, PARTITIONS):
    admin_client = KafkaAdminClient(bootstrap_servers=SERVER)
    topic_partitions = {}
    topic_partitions[TOPIC] = NewPartitions(total_count=PARTITIONS)
    admin_client.create_partitions(topic_partitions)

def sendProbeData(vehicleIDs, producer, timestamp, topic):
    probes = getProbeVehicleIDs(vehicleIDs)
    for vehID in probes:
        data = getProbeData(vehID, timestamp)  
        sendData(data, producer, topic, 0) 

def appendLoopCount(loopID, currentCount):
    return np.add(currentCount, getLoopLaneCounts(loopID))

def sendCamData(vehicleIDs, producer, timestamp, topic):
    for cam in CAMERA_LOOKUP:
        camVehicles = getCamVehicleIDs(cam, vehicleIDs)
        for vehID in camVehicles:
            data = getCamData(vehID, cam, timestamp)
            sendData(data, producer, topic, 0)

def sendTollData(vehicleIDs, producer, timestamp, topic):
    x, y = traci.simulation.convertGeo(float("-6.3829509"), float("53.3617409"), fromGeo=True)
    p1 = [x, y]
    tollVehicles = getTollVehicleIDs(vehicleIDs, p1)
    for vehID in tollVehicles:
        data = getTollData(vehID, p1, timestamp)
        sendData(data, producer, topic, 0)

def sendData(data, producer, topic, partition):
    data['sent_timestamp'] = time.time()
    producer.send(topic=topic, value=data, partition=partition)