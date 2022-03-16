from kafka import KafkaProducer
from constants import BROKER_EP, ENTERPRISE_EP, ENCODING, SUMO_CMD, LOOPS, M50_Northbound, M50_Southbound
from kafka_helper import sendCamData, sendProbeData, sendLoopData, sendTollData
from sumo_helper import SUMO_HOME_TOOLS, getTimeStamp
from datetime import date
import traci

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
        print("Simulation has began")   
        step = 1
        while step:
            traci.simulationStep()
            vehIDs = traci.vehicle.getIDList()
            t = traci.simulation.getTime()
            timestamp = getTimeStamp(date, t)
            
            sendLoopData(LOOPS, producer, timestamp, "inductive_loops")
            sendProbeData(vehIDs, enterprise_producer, timestamp, "enterprise_probe_vehicles") 
            sendCamData(vehIDs, enterprise_producer, timestamp, "enterprise_motorway_cameras") 
            sendTollData(vehIDs, enterprise_producer, timestamp, "enterprise_toll_bridge_cameras")

            step = step + 1
        traci.close()

#toDo
#add data noise, add time compilations of data 
#latency measurements, diff placement of brokers, latency measurements of stuff
#estimate added latency of camera video processing
#create partitions among the topics
