import json, pathlib

#KAFKA
PORT = '9092'
BROKER_EP = '18.203.222.104:'+PORT 
ENTERPRISE_EP = '34.243.204.178:'+PORT

ENCODING = (lambda v: json.dumps(v).encode('utf-8'))
DECODING = (lambda v: json.loads(v))
TOPICS = ["inductive_loops","probe_vehicles","toll_bridge_cameras","motorway_cameras"]
ENTERPRISE_TOPICS = ["enterprise_probe_vehicles","enterprise_motorway_cameras","enterprise_toll_bridge_cameras"]
TOPIC_LOOKUP = { "enterprise_probe_vehicles":"probe_vehicles", 
                "enterprise_motorway_cameras":"motorway_cameras",
                "enterprise_toll_bridge_cameras":"toll_bridge_cameras"}

#SUMO
pathToConfigs = '\ITSC2020_CAV_impact\ITSC2020_CAV_impact\workspace'
currentPath = str(pathlib.Path().resolve())
sumoBinary = "sumo-gui"
SUMO_CMD = [sumoBinary, "-c", currentPath+pathToConfigs+"\M50_simulation.sumo.cfg"]
truckVehicleTypes = ["CAT4", "CAT2", "HDT"]
passengerVehicleTypes = ["CAV4", "CAV2", "HDC"]
autonomousVehicles = ["CAV4", "CAV2", "CAT4", "CAT2"] #equates to 20% of vehicles

#Camera locations represent real cameras located on M50 ref: https://traffic.tii.ie/
CAMERA_LOOKUP = {"M50(S) After J9 (N7)": 
                {
                    "coordinates": "53.31353873270574,-6.363575673942173", 
                    "northEdges": "345616204#1.655",
                    "southEdges": "75259388-AddedOffRampEdge",
                },
                "M50(S) At J9 (N7)": 
                {
                    "coordinates": "53.32105761034455,-6.3702774491561724",
                    "northEdges": "4937552#1-AddedOnRampEdge,22941416,4937552",
                    "southEdges": "gneE0,11955830",
                }, 
                "M50(S) 1.4km Before J9 (N7)":  
                {
                    "coordinates": "53.33335994735108,-6.382773162408997",
                    "northEdges": "360361373.981",
                    "southEdges": "48290550.1878",
                 }, 
                "M50(N) 0.6km Before J7 (N4)": 
                {
                    "coordinates": "53.34727008589719,-6.386567333598459", 
                    "northEdges": "360361373.2643",
                    "southEdges": "48290550 ",   
                },
                "M50(N) Before J7 (N4)": 
                {
                    "coordinates": "53.35269470355068,-6.38544365135953",
                    "northEdges": "492226831,4414080#0.187",
                    "southEdges": "61047111,492229071,gneJ14,61047111.165", 
                },
                "M50(S) At J7 (N4)": 
                {
                    "coordinates": "53.35885146892749,-6.3834896661669625", 
                    "northEdges": "4414080#0.756.47,71324924,4414080#1-AddedOnRampEdge",
                    "southEdges": "16403446,4402297", 
                },
                "M50(S) Before West Link":         
                {
                    "coordinates": "53.363722242995145,-6.382086740810554", 
                    "northEdges": "4414080#1-AddedOnRampEdge.343",
                    "southEdges": "106130759.2098", 
                },
                "M50(S) Before ORT Gantry": 
                {
                    "coordinates": "53.37334705444544,-6.373142233357861" ,
                    "northEdges": "gneE7,gneE6",
                    "southEdges": "106130759.791", 
                }
}

TOLL_BRIDGE = {
    "coordinates": "53.3617409,-6.3829509" ,
    "northEdges": "4414080#1-AddedOnRampEdge.343",
    "southEdges": "106130759.2098", 
}




