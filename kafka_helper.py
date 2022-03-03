from sumo_helper import getProbeData, getLoopData, getProbeVehicleIDs, getCamVehicleIDs, getCamData, getTollData, getTollVehicleIDs, getTollData
from constants import TOPIC_LOOKUP, CAMERA_LOOKUP
import traci

def sendProbeData(vehicleIDs, producer):
    probes = getProbeVehicleIDs(vehicleIDs)
    for vehID in probes:
        data = getProbeData(vehID)  
        producer.send(TOPIC_LOOKUP["probes"], data) 

def sendLoopData(IDsOfLoops, producer):
    for loopID in IDsOfLoops:
        data = getLoopData(loopID)
        producer.send(TOPIC_LOOKUP["loops"], data) 

def sendCamData(vehicleIDs, producer):
    for cam in CAMERA_LOOKUP:
        camVehicles = getCamVehicleIDs(cam, vehicleIDs)
        for vehID in camVehicles:
            data = getCamData(vehID, cam)
            producer.send(TOPIC_LOOKUP["cameras"], data)

def sendTollData(vehicleIDs, producer):
    x, y = traci.simulation.convertGeo(float("-6.3829509"), float("53.3617409"), fromGeo=True)
    p1 = [x, y]
    tollVehicles = getTollVehicleIDs(vehicleIDs, p1)
    for vehID in tollVehicles:
        data = getTollData(vehID, p1)
        producer.send(TOPIC_LOOKUP["toll"], data)