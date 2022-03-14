from kafka import KafkaProducer
from constants import BROKER_EP, ENTERPRISE_EP, ENCODING, SUMO_CMD, CAMERA_LOOKUP
from kafka_helper import sendCamData, sendProbeData, sendLoopData, sendTollData
from sumo_helper import SUMO_HOME_TOOLS, getTimeStamp
from datetime import date
import traci, math

SUMO_HOME_TOOLS()

print("Starting producer...")
producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING)
print("Connecting to broker at:", BROKER_EP)

print("Starting enterprise producer...")
enterprise_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING)
print("Connecting to enterprise broker at:", ENTERPRISE_EP)
date = date.today()
while True:
        print("Starting simulation...")
        traci.start(SUMO_CMD)
        print("M50 Camera locations")
        for cam in CAMERA_LOOKUP:
            print(cam, CAMERA_LOOKUP[cam]["coordinates"])
            
        step = 1
        IDsOfEdges=traci.edge.getIDList()      
        IDsOfJunctions=traci.junction.getIDList()   
        IDsOfLoops = traci.inductionloop.getIDList()

        while step:
            traci.simulationStep()
            vehIDs = traci.vehicle.getIDList()
            t = traci.simulation.getTime()
            timestamp = getTimeStamp(date, t)

            if t % 3 == 0:
                sendLoopData(IDsOfLoops, producer, timestamp, "inductive_loops")

            if t % 5 == 0:
                sendProbeData(vehIDs, enterprise_producer, timestamp, "enterprise_probe_vehicles")
            
            if t % 7 == 0:
                sendCamData(vehIDs, enterprise_producer, timestamp, "enterprise_motorway_cameras") 
                sendTollData(vehIDs, enterprise_producer, timestamp, "enterprise_toll_bridge_cameras")

            step = step + 1
        traci.close()

#toDo

#make gui for road, parsing data

#get data correctly from sensors, make sure is right

#latency measurements, diff placement of brokers, latency measurements of stuff

#estimate added latency of camera video processing

#improve the North or South destinction of camera field of view

#create partitions among the topics

#put sensors into classes, make vehIDs, cam locations etc class constructors, will improve performance
