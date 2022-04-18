from constants import BROKER1_IP, ENTERPRISE_IP
from pythonping import ping
from datetime import datetime
import file_tools as file
import time

def ping_host(host):
    ping_result = ping(target=host, count=10, timeout=2)
    print("Pinging host at", host)
    return {
        'host': host,
        'avg_latency': ping_result.rtt_avg_ms,
        'min_latency': ping_result.rtt_min_ms,
        'max_latency': ping_result.rtt_max_ms,
        'packet_loss': ping_result.packet_loss,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    }

def run_ping_tests(): 
    while True:
        file.writePingToFile('Digital Twin Broker', ping_host(BROKER1_IP))
        file.writePingToFile('Enterprise Broker', ping_host(ENTERPRISE_IP))
        print("\n")
        time.sleep(60)