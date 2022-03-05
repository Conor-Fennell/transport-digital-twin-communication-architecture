from sumo_helper import getProbeData, getLoopData, getProbeVehicleIDs, getCamVehicleIDs, getCamData, getTollData, getTollVehicleIDs, getTollData
from constants import CAMERA_LOOKUP
import traci, random, time

def sendProbeData(vehicleIDs, producer, topic):
    probes = getProbeVehicleIDs(vehicleIDs)
    for vehID in probes:
        data = getProbeData(vehID)  
        producer.send(topic, data) 

def sendLoopData(IDsOfLoops, producer, topic):
    for loopID in IDsOfLoops:
        data = getLoopData(loopID)
        producer.send(topic, data) 

def sendCamData(vehicleIDs, producer, topic):
    for cam in CAMERA_LOOKUP:
        camVehicles = getCamVehicleIDs(cam, vehicleIDs)
        for vehID in camVehicles:
            data = getCamData(vehID, cam)
            producer.send(topic, data)

def cameraDataExtractionLatency():
    #https://goodvisionlive.com/goodvision-live-traffic/
    #claims will notify API in under 1 second -> data processing done beforehand
    t = random.randint(500, 1000)
    time.sleep(t/1000)

def sendTollData(vehicleIDs, producer, topic):
    x, y = traci.simulation.convertGeo(float("-6.3829509"), float("53.3617409"), fromGeo=True)
    p1 = [x, y]
    tollVehicles = getTollVehicleIDs(vehicleIDs, p1)
    for vehID in tollVehicles:
        data = getTollData(vehID, p1)
        producer.send(topic, data)
        
def sendData(data, producer, topic):
    producer.send(topic, data)