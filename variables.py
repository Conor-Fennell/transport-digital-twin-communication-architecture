import json

BROKER_EP = "broker-ip:9092" 
ENCODING = (lambda v: json.dumps(v).encode('utf-8'))
DECODING = (lambda v: json.loads(v))
TOPIC = "test"
