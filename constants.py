import json, pathlib

#KAFKA
BROKER_EP = "63.33.211.221:9092" 
ENCODING = (lambda v: json.dumps(v).encode('utf-8'))
DECODING = (lambda v: json.loads(v))
TOPICS = ["inductive_loops", "probe_vehicles"]
TOPIC_LOOKUP = { "loops":"inductive_loops", "probes":"probe_vehicles", "cameras":"motorway_cameras"}

#SUMO
pathToConfigs = '\ITSC2020_CAV_impact\ITSC2020_CAV_impact\workspace'
currentPath = str(pathlib.Path().resolve())
sumoBinary = "sumo"
SUMO_CMD = [sumoBinary, "-c", currentPath+pathToConfigs+"\M50_simulation.sumo.cfg"]
truckVehicleTypes = ["CAT4", "CAT2", "HDT"]
passengerVehicleTypes = ["CAV4", "CAV2", "HDC"]

#Camera locations represent real cameras located on M50 ref: https://traffic.tii.ie/
CAMERA_LOOKUP ={"M50(S) At J9 (N7)": "53.3172103,-6.3869086", 
                "M50(S) 1.4km Before J9 (N7)":  "53.3332738,-6.3829498",
                "M50(N) 0.6km Before J7 (N4)": "53.347292,-6.386747",
                "M50(N) Before J7 (N4)": "53.352888,-6.385446",
                "M50(S) At J7 (N4)": "53.359124,-6.383339",
                "M50(S) Before West Link": "53.3638538,-6.382078",
                "M50(S) Before ORT Gantry": "53.3734362,-6.3728859"
                }

TOLL_LOCATION = "53.3617409,-6.3829509"




