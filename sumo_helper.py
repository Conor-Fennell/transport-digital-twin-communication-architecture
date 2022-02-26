import os, sys, traci, datetime, random
from constants import passengerVehicleTypes, truckVehicleTypes

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
        

def getLoopData(loopID):
    data = {
        'id': str(loopID),
        'lane': traci.inductionloop.getLaneID(loopID),
        'count': str(traci.inductionloop.getLastStepVehicleNumber(loopID)),
        'timestamp': str(datetime.datetime.now())
    }
    return data


def getProbeVehicleIDs(IDsOfVehicles):
    passengerProbeVehicles = []
    truckProbeVehicles = []
    for vehID in IDsOfVehicles:
       
        if traci.vehicle.getTypeID(vehID) in passengerVehicleTypes:
            if probeVehicleProbability(0.1):
                passengerProbeVehicles.append(vehID)
        else:
            if probeVehicleProbability(0.2):
                truckProbeVehicles.append(vehID) 

    return passengerProbeVehicles, truckProbeVehicles

def getProbeData(vehID):
    data = {
        'id': str(vehID),
        'location': str(traci.vehicle.getPosition(vehID)),
        'speed': str(round(mpsToKph(traci.vehicle.getSpeed(vehID)), 2)),
        'timestamp': str(datetime.datetime.now())
    }
    return data
