from ast import Pass
import os, sys, traci, datetime, random
from constants import CAMERA_LOOKUP, TOLL_BRIDGE, passengerVehicleTypes, truckVehicleTypes

def mpsToKph(speed):
    return (speed*3600)/1000

def probeVehicleProbability(p):
    return random.random() < p

def SUMO_HOME_TOOLS():
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
        print("SUMO_HOME environment variable present!")
    else:
        print("please declare environment variable 'SUMO_HOME'")
        sys.exit("please declare environment variable 'SUMO_HOME'")

def getVehicleLocationGeo(vehID):
    x, y = traci.vehicle.getPosition(vehID)
    lat, lon = traci.simulation.convertGeo(float(x), float(y), fromGeo=False)
    return (lon, lat)

def calcDistance(p1, p2):
    return traci.simulation.getDistance2D(x1=float(p1[0]), y1=float(p1[1]), x2=float(p2[0]), y2=float(p2[1]), isGeo=False)

def getDirection(vehID, cam):
    edge = str(traci.vehicle.getRoadID(vehID))
    for i in cam["northEdges"].split(","):
        if i in edge:   
            return 'N'
    for i in cam["southEdges"].split(","):
        if i in edge:       
            return 'S'           
    return False

def getVehiclesInView(vehicleIDs, cam, r, dir):
    lon, lat = cam["coordinates"].split(",")
    x, y = traci.simulation.convertGeo(float(lat), float(lon), fromGeo=True)
    p1 = [x, y]
    vehicles = [] 
    for vehID in vehicleIDs:
        x, y = traci.vehicle.getPosition(vehID)
        p2 = [x, y]
        if (dir == 'N' and p2[1] > p1[1]) or (dir == 'S' and p2[1] < p1[1]): 
        #crude way of checking if in cameras field of view, change this to distance on road with respect to camera
            if calcDistance(p1, p2) < r and getDirection(vehID, cam):   
                vehicles.append(vehID)
    return vehicles

def getCamVehicleIDs(camera_id, vehicleIDs):
    return getVehiclesInView(vehicleIDs, CAMERA_LOOKUP[camera_id], 150, camera_id[4])

def getCamData(vehID, camera_id):
    lon, lat = CAMERA_LOOKUP[camera_id]["coordinates"].split(",")
    x, y = traci.simulation.convertGeo(float(lat), float(lon), fromGeo=True)
    p1 = [x, y]
    x, y = traci.vehicle.getPosition(vehID)
    p2 = [x, y]
    data = {
        'camera_id': str(camera_id),
        'lane_id': str(traci.vehicle.getRoadID(vehID)),
        'lane_index': str(traci.vehicle.getLaneIndex(vehID)),
        'direction': str(getDirection(vehID, CAMERA_LOOKUP[camera_id])),
        'distance': str(calcDistance(p1, p2)),
        'speed': str(round(mpsToKph(traci.vehicle.getSpeed(vehID)), 2)),
        'timestamp': str(datetime.datetime.now())
    }
    return data

def getLoopData(loopID):
    data = { 
        'loop_id': str(loopID),
        'lane': traci.inductionloop.getLaneID(loopID),
        'count': str(traci.inductionloop.getLastStepVehicleNumber(loopID)),
        'timestamp': str(datetime.datetime.now())
    }
    return data

def getProbeVehicleIDs(IDsOfVehicles):
    probes = []
    for vehID in IDsOfVehicles:      
        if traci.vehicle.getTypeID(vehID) in passengerVehicleTypes:
            if probeVehicleProbability(0.1):
                probes.append(vehID)
        else:
            if probeVehicleProbability(0.2):
                probes.append(vehID) 
    return probes

def getProbeData(vehID):
    data = {
        'probe_id': str(vehID),
        'location': str(getVehicleLocationGeo(vehID)),
        'speed': str(round(mpsToKph(traci.vehicle.getSpeed(vehID)), 2)),
        'timestamp': str(datetime.datetime.now())
    }
    return data

def getTollVehicleIDs(vehicleIDs, p1):
    return getVehiclesInViewToll(vehicleIDs, 100, p1)

def getVehiclesInViewToll(vehicleIDs, r, p1):
    vehicles = [] 
    for vehID in vehicleIDs:
        x, y = traci.vehicle.getPosition(vehID)
        p2 = [x, y]
        if calcDistance(p1, p2) < r and getDirection(vehID, TOLL_BRIDGE):   
                vehicles.append(vehID)
    return vehicles

def getTollData(vehID, p1):
    x, y = traci.vehicle.getPosition(vehID)
    p2 = [x, y]
    data = {
        'lane_id': str(traci.vehicle.getRoadID(vehID)),
        'lane_index': str(traci.vehicle.getLaneIndex(vehID)),
        'direction': str(getDirection(vehID, TOLL_BRIDGE)),
        'distance': str(calcDistance(p1, p2)),
        'speed': str(round(mpsToKph(traci.vehicle.getSpeed(vehID)), 2)),
        'class': str(traci.vehicle.getVehicleClass(vehID)),
        'timestamp': str(datetime.datetime.now())
    }
    return data



 