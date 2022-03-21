from kafka import KafkaProducer
from constants import BROKER_EP, ENTERPRISE_EP, ENCODING, SUMO_CMD, M50_Northbound, M50_Southbound, NB_PARTITION, SB_PARTITION
from kafka_helper import sendCamData, sendProbeData, getLoopData, sendTollData, sendData, appendLoopCount, initTopics
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

initTopics()

while True:
        print("Starting simulation...")
        traci.start(SUMO_CMD)
        print("Simulation has began")   
        step = 1
        loopData = []
        sCount = [0,0,0,0]
        nCount = [0,0,0,0]
        while step:
            traci.simulationStep()
            vehIDs = traci.vehicle.getIDList()
            t = traci.simulation.getTime()
            timestamp = getTimeStamp(date, t)
            
            nCount = appendLoopCount(M50_Northbound, nCount)
            sCount = appendLoopCount(M50_Southbound, sCount)

            if t%1 == 0:
                sendProbeData(vehIDs, enterprise_producer, timestamp, "enterprise_probe_vehicles") 
                sendCamData(vehIDs, enterprise_producer, timestamp, "enterprise_motorway_cameras")
                sendTollData(vehIDs, enterprise_producer, timestamp, "enterprise_toll_bridge_cameras") 
                sendData(getLoopData(M50_Northbound, timestamp, nCount), producer, "inductive_loops", NB_PARTITION)
                sendData(getLoopData(M50_Southbound, timestamp, sCount), producer, "inductive_loops", SB_PARTITION)
                sCount = [0,0,0,0]
                nCount = [0,0,0,0]

            step = step + 1
        traci.close()

#toDo
#latency measurements, diff placement of brokers, latency measurements of stuff
#estimate added latency of camera video processing
