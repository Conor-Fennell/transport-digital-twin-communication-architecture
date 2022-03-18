from sumo_helper import getLoopLaneCounts, getProbeData, getLoopData, getProbeVehicleIDs, getCamVehicleIDs, getCamData, getTollData, getTollVehicleIDs, getTollData
from constants import CAMERA_LOOKUP
from kafka import KafkaAdminClient
from kafka.admin import NewPartitions
import traci, random, time
import numpy as np

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
        producer.send(topic, data) 

def appendLoopCount(loopID, currentCount):
    return np.add(currentCount, getLoopLaneCounts(loopID))

def sendCamData(vehicleIDs, producer, timestamp, topic):
    for cam in CAMERA_LOOKUP:
        camVehicles = getCamVehicleIDs(cam, vehicleIDs)
        for vehID in camVehicles:
            data = getCamData(vehID, cam, timestamp)
            producer.send(topic, data)

def cameraDataExtractionLatency():
    #https://goodvisionlive.com/goodvision-live-traffic/
    #claims will notify API in under 1 second -> data processing done beforehand
    t = random.randint(500, 1000)
    time.sleep(t/1000)

def sendTollData(vehicleIDs, producer, timestamp, topic):
    x, y = traci.simulation.convertGeo(float("-6.3829509"), float("53.3617409"), fromGeo=True)
    p1 = [x, y]
    tollVehicles = getTollVehicleIDs(vehicleIDs, p1)
    for vehID in tollVehicles:
        data = getTollData(vehID, p1, timestamp)
        producer.send(topic, data)

def sendData(data, producer, topic, partition):
    producer.send(topic=topic, value=data, partition=partition)