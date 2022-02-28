from math import prod
from kafka import KafkaProducer
from constants import BROKER_EP, ENCODING, SUMO_CMD, CAMERA_LOOKUP
from kafka_helper import sendCamData, sendProbeData, sendLoopData
from sumo_helper import SUMO_HOME_TOOLS, getCamVehicleIDs
import traci

SUMO_HOME_TOOLS()

print("Starting producer...")
producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING)
print("Connecting to broker at:", BROKER_EP)

while True:
        print("Starting simulation...")
        traci.start(SUMO_CMD)
        print("M50 Camera locations")
        for cam in CAMERA_LOOKUP:
            print(cam, CAMERA_LOOKUP[cam])
            
        step = 0
        IDsOfEdges=traci.edge.getIDList()      
        IDsOfJunctions=traci.junction.getIDList()   
        IDsOfLoops = traci.inductionloop.getIDList()

        while step < 10:
            traci.simulationStep()
            vehIDs = traci.vehicle.getIDList()
            
            sendCamData(vehIDs, producer) 
            sendProbeData(vehIDs, producer)
            sendLoopData(IDsOfLoops, producer)

        traci.close()
        
#implement toll bridge data collection
#implement 2nd kafka server to act as enterprise servers: 
# #traci -> enterprise producer -> enterprise broker -> our enterprise conssumer -> regular producer...
#the data should be produced here, then consumer is here, then to our producer here to our kafka broker
