from kafka import KafkaProducer
from constants import BROKER_EP, ENTERPRISE_EP, ENCODING, SUMO_CMD, CAMERA_LOOKUP
from kafka_helper import sendCamData, sendProbeData, sendLoopData, sendTollData
from sumo_helper import SUMO_HOME_TOOLS
import traci

SUMO_HOME_TOOLS()

print("Starting producer...")
producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING)
print("Connecting to broker at:", BROKER_EP)

print("Starting enterprise producer...")
enterprise_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING)
print("Connecting to enterprise broker at:", ENTERPRISE_EP)

while True:
        print("Starting simulation...")
        traci.start(SUMO_CMD)
        print("M50 Camera locations")
        for cam in CAMERA_LOOKUP:
            print(cam, CAMERA_LOOKUP[cam]["coordinates"])
            
        step = 0
        IDsOfEdges=traci.edge.getIDList()      
        IDsOfJunctions=traci.junction.getIDList()   
        IDsOfLoops = traci.inductionloop.getIDList()

        while step < 10:
            traci.simulationStep()
            vehIDs = traci.vehicle.getIDList()
            sendProbeData(vehIDs, producer, "probe_vehicles")
            sendLoopData(IDsOfLoops, producer, "inductive_loops")
            sendCamData(vehIDs, enterprise_producer, "motorway_cameras") 
            sendTollData(vehIDs, producer, "toll_bridge_cameras")

        traci.close()

#toDo

#implement 2nd kafka server to act as enterprise servers: 
# #traci -> enterprise producer -> enterprise broker -> our enterprise conssumer -> regular producer...
#the data should be produced here, then consumer is here, then to our producer here to our kafka broker

#estimate added latency of camera video processing

#improve probe vehicle selection + make them consistent

#implement sat nav vehicles + gps vehicles

#improve the North or South destinction of camera field of view

#create partitions among the topics

#put sensors into classes, make vehIDs, cam locations etc class constructors, will improve performance

#implement context subscriptions such as vehicle ids, also need to make all vehicle ids known before sim starts