import ast
from pydoc_data.topics import topics
import numpy as np
import matplotlib.pyplot as plt

def brokerPing(in_path, broker):
    path = in_path+'\\test_results\ping_results\\'+str(broker)+'.txt'
    with open(path) as f:
        lines = f.readlines()
        latency = []
        for line in lines:
            latency.append(ast.literal_eval(line)['avg_latency'])
        arr = np.array(latency)
        return arr

def getLatency(in_path, topic):
    path = in_path+'\\test_results\latency_results\\'+str(topic)+'.txt'
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            latency = line.split(",")
        arr = np.array(latency[:-1], dtype=float)
        return arr

def getSimDuration(in_path):
    path = in_path+'\\test_results\\test_info.txt'
    with open(path) as f:
        for i, line in enumerate(f):
            if i == 1:
                duration = line.split(":")
        return float(duration[-1])

def getSimStats(in_path):
    print('Stats for:',in_path)
    broker_ping = brokerPing(in_path, 'Digital Twin Broker')
    enterprise_ping = brokerPing(in_path, 'Enterprise Broker')

    loop_latency = getLatency(in_path, 'inductive_loops')
    cam_latency = getLatency(in_path, 'motorway_cameras')
    toll_latency = getLatency(in_path, 'toll_bridge_cameras')
    probe_latency = getLatency(in_path, 'probe_vehicles')

    print('broker_ping:',np.mean(broker_ping),'ms')
    print('enterprise_ping:',np.mean(enterprise_ping),'ms')
    print('loop_latency:',np.mean(loop_latency),'ms')
    print('cam_latency:',np.mean(cam_latency),'ms')
    print('toll_latency:',np.mean(toll_latency),'ms')
    print('probe_latency:',np.mean(probe_latency),'ms')

    print('Kafka loop_latency:',np.mean(loop_latency) - np.mean(broker_ping),'ms')
    print('Kafka cam_latency:',np.mean(cam_latency) - np.mean(enterprise_ping),'ms')
    print('Kafka toll_latency:',np.mean(toll_latency) - np.mean(enterprise_ping),'ms')
    print('Kafka probe_latency:',np.mean(probe_latency) - np.mean(enterprise_ping),'ms')

    print('#loop_messages:',len(loop_latency))
    print('#cam_messages:',len(cam_latency))
    print('#toll_messagess:',len(toll_latency))
    print('#probe_messages:',len(probe_latency))

    total_msgs = len(loop_latency)+len(cam_latency)+len(toll_latency)+len(probe_latency)
    s = getSimDuration(in_path)

    print('#total messages:', total_msgs)
    print('#total messages/per second:', total_msgs/s)

    stats = {
        'broker_ping': broker_ping,
        'enterprise_ping': enterprise_ping,
        'loop_latency': loop_latency,
        'cam_latency': cam_latency,
        'toll_latency': toll_latency,
        'probe_latency': probe_latency, 
        'total msgs': total_msgs,
        'duration': s
    }
    return stats

#---------------------------------------------------------------


MIDNIGHT = 'DATA\SCENARIO_B\MIDNIGHT'
RUSHHOUR = 'DATA\SCENARIO_B\RUSHHOUR'

midnight_stats = getSimStats(MIDNIGHT)
rush_hour_stats = getSimStats(RUSHHOUR)

midnight_stats_bp = np.mean(midnight_stats['broker_ping'])
midnight_stats_ep = np.mean(midnight_stats['enterprise_ping'])
rush_hour_stats_bp = np.mean(rush_hour_stats['broker_ping'])
rush_hour_stats_ep = np.mean(rush_hour_stats['enterprise_ping'])

data = [
    [np.mean(midnight_stats['loop_latency']), 
    np.mean(midnight_stats['cam_latency']), 
    np.mean(midnight_stats['toll_latency']), 
    np.mean(midnight_stats['probe_latency'])],
    [np.mean(rush_hour_stats['loop_latency']), 
    np.mean(rush_hour_stats['cam_latency']), 
    np.mean(rush_hour_stats['toll_latency']), 
    np.mean(rush_hour_stats['probe_latency'])]
]

X = np.arange(4)
fig, ax = plt.subplots()
topics = ('inductive_loops', 'motorway_cameras', 'toll_bridge', 'probe_vehicles')
ind = np.arange(4)
ax.bar(ind,data[0], color = 'b', width = 0.25)
ax.bar(ind+0.25,data[1], color = 'r', width = 0.25)
ax.set_yticks(np.arange(0, 251, 50))
ax.set_xticks(ind, topics)
ax.set_ylabel('Latency (ms)')
ax.set_title('SCENARIO B - Total Latency by Topic')
ax.legend(labels=['Midnight', 'Rushhour'])
plt.show()


adjusted_data = [
    [np.mean(midnight_stats['loop_latency']) - midnight_stats_bp, 
    np.mean(midnight_stats['cam_latency']) - midnight_stats_ep, 
    np.mean(midnight_stats['toll_latency']) - midnight_stats_ep, 
    np.mean(midnight_stats['probe_latency']) - midnight_stats_ep],
    [np.mean(rush_hour_stats['loop_latency']) - rush_hour_stats_bp, 
    np.mean(rush_hour_stats['cam_latency']) - rush_hour_stats_ep, 
    np.mean(rush_hour_stats['toll_latency']) - rush_hour_stats_ep, 
    np.mean(rush_hour_stats['probe_latency']) - rush_hour_stats_ep]
]

fig, ax = plt.subplots()
ax.bar(ind,adjusted_data[0], color = 'b', width = 0.25)
ax.bar(ind+0.25,adjusted_data[1], color = 'r', width = 0.25)
ax.set_yticks(np.arange(0, 251, 50))
ax.set_xticks(ind, topics)
ax.set_ylabel('Latency (ms)')
ax.set_title('SCENARIO B - Kafka Latency by Topic')
ax.legend(labels=['Midnight', 'Rushhour'])
plt.show()


mid_s = midnight_stats['duration']
rush_s = rush_hour_stats['duration']

data = [
    [len(midnight_stats['loop_latency'])/mid_s,
    len(midnight_stats['cam_latency'])/mid_s,
    len(midnight_stats['toll_latency'])/mid_s,
    len(midnight_stats['probe_latency'])/mid_s],

    [len(rush_hour_stats['loop_latency'])/rush_s,
    len(rush_hour_stats['cam_latency'])/rush_s,
    len(rush_hour_stats['toll_latency'])/rush_s,
    len(rush_hour_stats['probe_latency'])/rush_s]
    ]

X = np.arange(4)
fig, ax = plt.subplots()
topics = ('Inductive Loops', 'Motorway Cameras', 'Toll Bridge', 'Probe Vehicles')
ind = np.arange(4)
ax.bar(ind,data[0], color = 'b', width = 0.25)
ax.bar(ind+0.25,data[1], color = 'r', width = 0.25)
ax.set_yticks(np.arange(0, 101, 10))
ax.set_xticks(ind, topics)
ax.set_ylabel('messages/second')
ax.set_title('SCENARIO B - Message Throughput by Topic')
ax.legend(labels=['Midnight', 'Rushhour'])
plt.show()
