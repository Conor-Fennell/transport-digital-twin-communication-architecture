from sumo_helper import getProbeData, getLoopData, getProbeVehicleIDs, getCamVehicleIDs, getCamData
from constants import TOPIC_LOOKUP, CAMERA_LOOKUP

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