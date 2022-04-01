from kafka import KafkaProducer
from constants import BROKER_EP, ENTERPRISE_EP, ENCODING, SUMO_CMD, M50_Northbound, M50_Southbound, NB_PARTITION, SB_PARTITION, SIMULATION_DURATION
from kafka_helper import sendCamData, sendProbeData, getLoopData, sendTollData, sendData, appendLoopCount, initTopics
from sumo_helper import SUMO_HOME_TOOLS, getTimeStamp
from datetime import date, datetime
import file_tools as file
import traci, time

SUMO_HOME_TOOLS()

linger = 0
print("Starting producers...")
north_loop_producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING, linger_ms=linger)
south_loop_producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING, linger_ms=linger)
print("Connecting to broker at:", BROKER_EP)

print("Starting enterprise producers...")
toll_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING)
camera_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING)
probe_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING)
print("Connecting to enterprise broker at:", ENTERPRISE_EP)
date = date.today()

initTopics()

while True:
        print("Waiting to start simulation...")
        traci.start(SUMO_CMD)
        print("Simulation started...")
        start_t = time.time()
        t = 0
        step = 0
        loopData = []
        sCount = [0,0,0,0]
        nCount = [0,0,0,0]
        print("SIMULATION_DURATION",SIMULATION_DURATION)
        while t<SIMULATION_DURATION:
            traci.simulationStep()
            vehIDs = traci.vehicle.getIDList()
            t = traci.simulation.getTime()
            timestamp = getTimeStamp(date, t)
            
            nCount = appendLoopCount(M50_Northbound, nCount)
            sCount = appendLoopCount(M50_Southbound, sCount)

            if t%1 == 0:
                sendProbeData(vehIDs, probe_producer, timestamp, "enterprise_probe_vehicles") 
                sendCamData(vehIDs, camera_producer, timestamp, "enterprise_motorway_cameras")
                sendTollData(vehIDs, toll_producer, timestamp, "enterprise_toll_bridge_cameras") 
                sendData(getLoopData(M50_Northbound, timestamp, nCount), north_loop_producer, "inductive_loops", NB_PARTITION)
                sendData(getLoopData(M50_Southbound, timestamp, sCount), south_loop_producer, "inductive_loops", SB_PARTITION)
                sCount = [0,0,0,0]
                nCount = [0,0,0,0]
                print("completed "+str((step/7200)*100)+"%")

            step = step+1

        end_time = datetime.now()
        real_duration_s = time.time()-start_t
        print('Simulation finished at', end_time)
        print('total sim time seconds: ', real_duration_s)
        file.writeTestInfoToFile(end_time, real_duration_s, SIMULATION_DURATION, BROKER_EP, ENTERPRISE_EP)
        
        traci.close()

