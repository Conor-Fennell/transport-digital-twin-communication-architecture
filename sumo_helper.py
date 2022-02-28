import os, sys, traci, datetime, random
from constants import CAMERA_LOOKUP, passengerVehicleTypes, truckVehicleTypes

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
   
def getVehiclesInView(vehicleIDs, coordinates, r, dir):
    lon, lat = coordinates.split(",")
    x, y = traci.simulation.convertGeo(float(lat), float(lon), fromGeo=True)
    p1 = [x, y]
    vehicles = [] 
    for vehID in vehicleIDs:
        x, y = traci.vehicle.getPosition(vehID)
        p2 = [x, y]
        if (dir == 'N' and p2[1] > p1[1]) or (dir == 'S' and p2[1] < p1[1]):
            if calcDistance(p1, p2) < r:
                vehicles.append(vehID)
    return vehicles

def getCamVehicleIDs(camera_id, vehicleIDs):
    return getVehiclesInView(vehicleIDs, CAMERA_LOOKUP[camera_id], 500, camera_id[4])

def getCamData(vehID, cam):
    data = {
        'camera_id': str(cam),
        'lane': str(traci.vehicle.getLaneIndex(vehID)),
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

def getTollData():
    pass

 