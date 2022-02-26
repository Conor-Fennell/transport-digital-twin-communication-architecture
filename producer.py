from kafka import KafkaProducer
from constants import BROKER_EP, ENCODING, TOPIC, SUMO_CMD
from sumo_helper import SUMO_HOME_TOOLS, getLoopData, getProbeVehicleIDs, getProbeData
import traci

SUMO_HOME_TOOLS()

print("Starting producer...")
producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING)
print("Connecting to broker at:", BROKER_EP)
while True:
        print("Starting simulation...")
        traci.start(SUMO_CMD)
        step = 0
        IDsOfEdges=traci.edge.getIDList()      
        IDsOfJunctions=traci.junction.getIDList()   
        IDsOfLoops = traci.inductionloop.getIDList()
   
        while step < 10:
            traci.simulationStep()

            for loopID in IDsOfLoops:
                data = getLoopData(loopID)
                producer.send(TOPIC, data)

            pProbes, tProbes = getProbeVehicleIDs(traci.vehicle.getIDList())    
            
            for vehID in pProbes:
                data = getProbeData(vehID) 
                producer.send(TOPIC, data)

            for vehID in tProbes:
                data = getProbeData(vehID) 
                producer.send(TOPIC, data) 

        traci.close()
        

