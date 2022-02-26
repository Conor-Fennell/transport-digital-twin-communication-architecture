import json, pathlib

#KAFKA
BROKER_EP = "54.155.203.80:9092" 
ENCODING = (lambda v: json.dumps(v).encode('utf-8'))
DECODING = (lambda v: json.loads(v))
TOPIC = "test"

#SUMO
pathToConfigs = '\ITSC2020_CAV_impact\ITSC2020_CAV_impact\workspace'
currentPath = str(pathlib.Path().resolve())
sumoBinary = "sumo"
SUMO_CMD = [sumoBinary, "-c", currentPath+pathToConfigs+"\M50_simulation.sumo.cfg"]

truckVehicleTypes = ["CAT4", "CAT2", "HDT"]
passengerVehicleTypes = ["CAV4", "CAV2", "HDC"]




