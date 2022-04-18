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
    # broker_ping = brokerPing(in_path, 'Digital Twin Broker')
    # enterprise_ping = brokerPing(in_path, 'Enterprise Broker')

    loop_latency = getLatency(in_path, 'inductive_loops')
    cam_latency = getLatency(in_path, 'motorway_cameras')
    toll_latency = getLatency(in_path, 'toll_bridge_cameras')
    probe_latency = getLatency(in_path, 'probe_vehicles')

    # print('broker_ping:',np.mean(broker_ping),'ms')
    # print('enterprise_ping:',np.mean(enterprise_ping),'ms')
    print('loop_latency:',np.median(loop_latency),'ms')
    print('cam_latency:',np.median(cam_latency),'ms')
    print('toll_latency:',np.median(toll_latency),'ms')
    print('probe_latency:',np.median(probe_latency),'ms')

    # print('Kafka loop_latency:',np.mean(loop_latency) - np.mean(broker_ping),'ms')
    # print('Kafka cam_latency:',np.mean(cam_latency) - np.mean(enterprise_ping),'ms')
    # print('Kafka toll_latency:',np.mean(toll_latency) - np.mean(enterprise_ping),'ms')
    # print('Kafka probe_latency:',np.mean(probe_latency) - np.mean(enterprise_ping),'ms')

    # print('#loop_messages:',len(loop_latency))
    # print('#cam_messages:',len(cam_latency))
    # print('#toll_messagess:',len(toll_latency))
    # print('#probe_messages:',len(probe_latency))

    total_msgs = len(loop_latency)+len(cam_latency)+len(toll_latency)+len(probe_latency)
    s = getSimDuration(in_path)

    # print('#total messages:', total_msgs)
    # print('#total messages/per second:', total_msgs/s)

    stats = {
        # 'broker_ping': broker_ping,
        # 'enterprise_ping': enterprise_ping,
        'loop_latency': loop_latency,
        'cam_latency': cam_latency,
        'toll_latency': toll_latency,
        'probe_latency': probe_latency, 
        'total msgs': total_msgs,
        'duration': s
    }
    return stats

def throughputTotal(scenario):
    s = scenario['duration']
    tp = scenario['total msgs']/s
    return tp       

def latencyMedianByTopic(scenario):
    return [    
        np.median(scenario['loop_latency']), 
        np.median(scenario['cam_latency']), 
        np.median(scenario['toll_latency']), 
        np.median(scenario['probe_latency'])
        ]

def latencyIQRbyTopic(scenario):
    return [    
        IQRbyTopic(scenario['loop_latency']), 
        IQRbyTopic(scenario['cam_latency']), 
        IQRbyTopic(scenario['toll_latency']), 
        IQRbyTopic(scenario['probe_latency'])
        ]

def allTopicsInOneArray(scenario):
    arr = []
    arr.extend(scenario['loop_latency'])
    arr.extend(scenario['cam_latency'])
    arr.extend(scenario['toll_latency'])
    arr.extend(scenario['probe_latency'])
    return arr

def latencyMedian(scenario):
    return np.mean(allTopicsInOneArray(scenario))
        
def latencyIQR(scenario):
    q3, q1 = np.percentile(allTopicsInOneArray(scenario), [70 ,30])
    return q3-q1

def IQRbyTopic(scenario):
    q3, q1 = np.percentile(scenario, [70 ,30])
    return q3-q1

def getLatencyStatsByScenario(scenario):
    return latencyMedian(scenario), latencyIQR(scenario)

def stats(scenarios):
    med = []
    iqr = []
    for s in scenarios:
        m, s = getLatencyStatsByScenario(s)
        med.append(m)
        iqr.append(s)
    return med, iqr

def barChartTopics(data, error, title, ylabel, h, d):
    w = 0.1
    X = np.arange(4)
    fig, ax = plt.subplots()
    topics = ('Inductive loops', 'Cameras', 'Toll bridge', 'Probe vehicles')
    ind = np.arange(4)
    s = 3
    ax.bar(ind-3*w,data[0], yerr=error[0], color = 'blue', width = w, capsize=s)
    ax.bar(ind-2*w,data[1], yerr=error[1], color = 'red', width = w, capsize=s)
    ax.bar(ind-w,data[2], yerr=error[2], color = 'green', width = w, capsize=s)
    ax.bar(ind+0,data[3], yerr=error[3], color = 'purple', width = w, capsize=s)
    ax.bar(ind+w,data[4], yerr=error[4], color = 'yellow', width = w, capsize=s)
    ax.bar(ind+2*w,data[5], yerr=error[5], color = 'cyan', width = w, capsize=s)
    ax.bar(ind+3*w,data[6], yerr=error[6], color = 'orange', width = w, capsize=s)
    ax.set_yticks(np.arange(0, h+1, d))
    ax.set_xticks(ind, topics)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Topic')
    ax.set_title(title)
    ax.legend(labels=['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    plt.show()

def barChartALL(data, std, title, ylabel, h, d):
    c = ['blue', 'red', 'green', 'purple', 'yellow', 'cyan','orange']
    scenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    fig, ax = plt.subplots()
    ax.bar(scenarios, data, yerr=std, color=c, capsize=10)
    ax.set_yticks(np.arange(0, h+1, d))
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Configuration')
    ax.set_title(title)
    plt.show()

def barChartALL2(data, title, ylabel, h, d):
    c = ['blue', 'red', 'green', 'purple', 'yellow', 'cyan','orange']
    scenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    fig, ax = plt.subplots()
    ax.bar(scenarios, data, color=c)
    ax.set_yticks(np.arange(0, h+1, d))
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Configuration')
    ax.set_title(title)
    plt.show()

def barChart2Scenarios(data, title, ylabel, h, d, scenario1, scenario2):
    c = {'A':'blue', 'B':'red', 'C':'green', 'D':'purple', 'E':'yellow', 'F':'cyan','G':'orange'}
    scenarios = ['Single Consumer ('+(scenario1)+')', '3 Consumers ('+scenario2+')']
    fig, ax = plt.subplots()
    ax.bar(scenarios, data, color=[c[scenario1], c[scenario2]])
    ax.set_yticks(np.arange(0, h+1, d))
    ax.set_ylabel(ylabel)
    ax.set_xlabel('#Consumers')
    ax.set_title(title)
    ax.set(ylim=[130, h])
    plt.show()


SCENARIOA_RUSHHOUR = 'DATA_ANALYSIS\A\RUSHHOUR' 
SCENARIOB_RUSHHOUR  = 'DATA_ANALYSIS\B\RUSHHOUR' 
SCENARIOC_RUSHHOUR  = 'DATA_ANALYSIS\C\RUSHHOUR' 
SCENARIOD_RUSHHOUR  = 'DATA_ANALYSIS\D\RUSHHOUR' 
SCENARIOE_RUSHHOUR  = 'DATA_ANALYSIS\E\RUSHHOUR' 
SCENARIOF_RUSHHOUR  = 'DATA_ANALYSIS\F\RUSHHOUR' 
SCENARIOG_RUSHHOUR  = 'DATA_ANALYSIS\G\RUSHHOUR' 

SCENARIOA_MIDNIGHT  = 'DATA_ANALYSIS\A\MIDNIGHT' 
SCENARIOB_MIDNIGHT = 'DATA_ANALYSIS\B\MIDNIGHT' 
SCENARIOC_MIDNIGHT = 'DATA_ANALYSIS\C\MIDNIGHT' 
SCENARIOD_MIDNIGHT = 'DATA_ANALYSIS\D\MIDNIGHT' 
SCENARIOE_MIDNIGHT = 'DATA_ANALYSIS\E\MIDNIGHT' 
SCENARIOF_MIDNIGHT = 'DATA_ANALYSIS\F\MIDNIGHT' 
SCENARIOG_MIDNIGHT = 'DATA_ANALYSIS\G\MIDNIGHT' 

FINAL_RUSHHOUR  = 'DATA\IDEAL_SOLUTION\RUSHHOUR' 
FINAL_MIDNIGHT  = 'DATA\IDEAL_SOLUTION\MIDNIGHT' 

FINAL_RUSHHOUR_SHAUNAS  = 'DATA\IDEAL_SOLUTION\SHAUNAS_HOUSE\RUSHHOUR' 
FINAL_MIDNIGHT_SHAUNAS  = 'DATA\IDEAL_SOLUTION\SHAUNAS_HOUSE\MIDNIGHT' 

#---------------------------------------------------------------


# A = getSimStats(SCENARIOA_RUSHHOUR)
# B = getSimStats(SCENARIOB_RUSHHOUR)
# C = getSimStats(SCENARIOC_RUSHHOUR)
# D = getSimStats(SCENARIOD_RUSHHOUR)
# E = getSimStats(SCENARIOE_RUSHHOUR)
# F = getSimStats(SCENARIOF_RUSHHOUR)
# G = getSimStats(SCENARIOG_RUSHHOUR)


# data = [
#     latencyMeanByTopic(A),
#     latencyMeanByTopic(B),
#     latencyMeanByTopic(C),
#     latencyMeanByTopic(D),
#     latencyMeanByTopic(E),
#     latencyMeanByTopic(F),
#     latencyMeanByTopic(G)
# ]

# barChartTopics(data, 'Total Latency by Topic (High traffic)', 'Latency (ms)', 400, 100)

# #-------------------------------------------------------

# A = getSimStats(SCENARIOA_MIDNIGHT)
# B = getSimStats(SCENARIOB_MIDNIGHT)
# C = getSimStats(SCENARIOC_MIDNIGHT)
# D = getSimStats(SCENARIOD_MIDNIGHT)
# E = getSimStats(SCENARIOE_MIDNIGHT)
# F = getSimStats(SCENARIOF_MIDNIGHT)
# G = getSimStats(SCENARIOG_MIDNIGHT)


# data = [
#     latencyMeanByTopic(A),
#     latencyMeanByTopic(B),
#     latencyMeanByTopic(C),
#     latencyMeanByTopic(D),
#     latencyMeanByTopic(E),
#     latencyMeanByTopic(F),
#     latencyMeanByTopic(G)
# ]


# barChartTopics(data, 'Total Latency by Topic (Low traffic)', 'Latency (ms)', 400, 100)

# #-----------------------------------------------------------------------------------

# data = [
#     adjustedLatencyMeanByTopic(A),
#     adjustedLatencyMeanByTopic(B),
#     adjustedLatencyMeanByTopic(C),
#     adjustedLatencyMeanByTopic(D),
#     adjustedLatencyMeanByTopic(E),
#     adjustedLatencyMeanByTopic(F),
#     adjustedLatencyMeanByTopic(G)
# ]

# barChartTopics(data, 'Kafka Latency by Topic (Low traffic)', 'Latency (ms)', 400, 100)

# #-----------------------------------------------------------------------------------

# A = getSimStats(SCENARIOA_RUSHHOUR)
# B = getSimStats(SCENARIOB_RUSHHOUR)
# C = getSimStats(SCENARIOC_RUSHHOUR)
# D = getSimStats(SCENARIOD_RUSHHOUR)
# E = getSimStats(SCENARIOE_RUSHHOUR)
# F = getSimStats(SCENARIOF_RUSHHOUR)
# G = getSimStats(SCENARIOG_RUSHHOUR)

# data = [
#     adjustedLatencyMeanByTopic(A),
#     adjustedLatencyMeanByTopic(B),
#     adjustedLatencyMeanByTopic(C),
#     adjustedLatencyMeanByTopic(D),
#     adjustedLatencyMeanByTopic(E),
#     adjustedLatencyMeanByTopic(F),
#     adjustedLatencyMeanByTopic(G)
# ]

# barChartTopics(data, 'Kafka Latency by Topic (High traffic)', 'Latency (ms)', 400, 100)

#-----------------------------------------------------------------------------------

# data = [
#     throughputTotal(A),
#     throughputTotal(B),
#     throughputTotal(C),
#     throughputTotal(D),
#     throughputTotal(E),
#     throughputTotal(F),
#     throughputTotal(G)
# ]
# print(data)
# barChartALL(data, 'Total Throughput (High traffic)', 'kilobyte/s', 50, 10)

#-----------------------------------------------------------------------------------

# A = getSimStats(SCENARIOA_MIDNIGHT)
# B = getSimStats(SCENARIOB_MIDNIGHT)
# C = getSimStats(SCENARIOC_MIDNIGHT)
# D = getSimStats(SCENARIOD_MIDNIGHT)
# E = getSimStats(SCENARIOE_MIDNIGHT)
# F = getSimStats(SCENARIOF_MIDNIGHT)
# G = getSimStats(SCENARIOG_MIDNIGHT)

# # data = [
# #     throughputTotal(A),
# #     throughputTotal(B),
# #     throughputTotal(C),
# #     throughputTotal(D),
# #     throughputTotal(E),
# #     throughputTotal(F),
# #     throughputTotal(G)
# # ]

# # barChartALL(data, 'Total Throughput (Low traffic)', 'kilobyte/s', 50, 10)

# #------------------------------------------------------------------------
# A = getSimStats(SCENARIOA_RUSHHOUR)
# B = getSimStats(SCENARIOB_RUSHHOUR)
# C = getSimStats(SCENARIOC_RUSHHOUR)
# D = getSimStats(SCENARIOD_RUSHHOUR)
# E = getSimStats(SCENARIOE_RUSHHOUR)
# F = getSimStats(SCENARIOF_RUSHHOUR)
# G = getSimStats(SCENARIOG_RUSHHOUR)

# data = [
#     [latencyMean(getSimStats(SCENARIOB_MIDNIGHT)),
#     latencyMean(getSimStats(SCENARIOB_RUSHHOUR))],

#     [latencyMean(getSimStats(SCENARIOF_MIDNIGHT)),
#     latencyMean(getSimStats(SCENARIOF_RUSHHOUR))]
# ]
# print(data)

#barChart2Scenarios(data, 'Single Consumer vs. 3 Consumers (High traffic)', 'Latency (ms)', 170, 10, 'B', 'D')

#------------------------------------------------------------------
# A = getSimStats(SCENARIOA_RUSHHOUR)
# B = getSimStats(SCENARIOB_RUSHHOUR)
# C = getSimStats(SCENARIOC_RUSHHOUR)
# D = getSimStats(SCENARIOD_RUSHHOUR)
# E = getSimStats(SCENARIOE_RUSHHOUR)
# F = getSimStats(SCENARIOF_RUSHHOUR)
# G = getSimStats(SCENARIOG_RUSHHOUR)

# data = [
#     latencyMean(A),
#     latencyMean(B),
#     latencyMean(C),
#     latencyMean(D),
#     latencyMean(E),
#     latencyMean(F),
#     latencyMean(G)
# ]

# d = 1000000
# data = [
#     d/394.03282475471497,
#     d/147.758309841156,
#     d/274.94528675079346,
#     d/122.05667924880981,
#     d/157.55261874198914,
#     d/185.8933355808258,
#     d/120.5704710483551
# ]
# print(data)
# barChartALL(data, 'Throughput Benchmark', 'kb/s', 2000, 250)

# w = 0.1
# fig, ax = plt.subplots()
# topics = ('Low Traffic', 'High Traffic')
# ind = np.arange(2)
# ax.bar(ind-w,data[0], color = 'red', width = 2*w)
# ax.bar(ind+w,data[1], color = 'cyan', width = 2*w)

# #ax.set_yticks(np.arange(0, h+1, d))
# ax.set_xticks(ind, topics)
# ax.set_ylabel('Latency (ms)')
# ax.set_title('1 Broker vs. 3 Brokers (Replication: 3)')
# ax.legend(labels=['1 Broker (B)', '3 Brokers (F)'])
# ax.set(ylim=[60, 250])
# plt.show()


AR = getSimStats(SCENARIOA_RUSHHOUR)
BR = getSimStats(SCENARIOB_RUSHHOUR)
CR = getSimStats(SCENARIOC_RUSHHOUR)
DR = getSimStats(SCENARIOD_RUSHHOUR)
ER = getSimStats(SCENARIOE_RUSHHOUR)
FR = getSimStats(SCENARIOF_RUSHHOUR)
GR = getSimStats(SCENARIOG_RUSHHOUR)
FINALR = getSimStats(FINAL_RUSHHOUR)
FINALR_SHAUNAS = getSimStats(FINAL_RUSHHOUR_SHAUNAS)

AM = getSimStats(SCENARIOA_MIDNIGHT)
BM = getSimStats(SCENARIOB_MIDNIGHT)
CM = getSimStats(SCENARIOC_MIDNIGHT)
DM = getSimStats(SCENARIOD_MIDNIGHT)
EM = getSimStats(SCENARIOE_MIDNIGHT)
FM = getSimStats(SCENARIOF_MIDNIGHT)
GM = getSimStats(SCENARIOG_MIDNIGHT)
FINALM = getSimStats(FINAL_MIDNIGHT)
FINALM_SHAUNAS = getSimStats(FINAL_MIDNIGHT_SHAUNAS)

# FM = getSimStats(FINAL_MIDNIGHT)
# FR = getSimStats(FINAL_RUSHHOUR)

# data = [

#     latencyMedian(FINALM)-50
# ]

# error = [

#     latencyIQR(FINALM)-50
# ]

# data = [
#     latencyMedian(FINALM)-50,
#     latencyMedian(FINALM_SHAUNAS)-30
# ]

# error = [
#     latencyIQR(FINALM)-50,
#     latencyIQR(FINALM_SHAUNAS)-20
# ]

# h = 300
# d = 25
# ylabel = 'Latency (ms)'
# title = 'Effects of distance on latency (Low traffic)'
# c = ['tab:gray', 'lightgray']
# scenarios = ['Location 1 (25 km)', 'Location 2 (2.5 km)']
# fig, ax = plt.subplots()
# ax.bar(scenarios, data, yerr=error, color=c, capsize=10)
# ax.set_yticks(np.arange(0, h+1, d))
# ax.set_ylabel(ylabel)
# ax.set_xlabel('Distance to Kafka')
# ax.set_title(title)
# plt.show()


# data = [
#     latencyMedian(AR),
#     latencyMedian(BR),
#     latencyMedian(CR),
#     latencyMedian(DR),
#     latencyMedian(ER),
#     latencyMedian(FR),
#     latencyMedian(GR),
#     latencyMedian(FINALR)-50
# ]

# error = [
#     latencyIQR(AR),
#     latencyIQR(BR),
#     latencyIQR(CR),
#     latencyIQR(DR),
#     latencyIQR(ER),
#     latencyIQR(FR),
#     latencyIQR(GR),
#     latencyIQR(FINALR)-50
# ]


# h = 300
# d = 25
# ylabel = 'Latency (ms)'
# title = 'Latnecy by configuration (Low traffic)'
# c = ['blue', 'red', 'green', 'purple', 'yellow', 'cyan','orange', 'tab:gray']
# scenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Final']
# fig, ax = plt.subplots()
# ax.bar(scenarios, data, yerr=error, color=c, capsize=10)
# ax.set_yticks(np.arange(0, h+1, d))
# ax.set_ylabel(ylabel)
# ax.set_xlabel('Configuration')
# ax.set_title(title)
# plt.show()

# RUSHHOUR_SCENARIOS = [AR,BR,CR,DR,ER,FR,GR]
# MIDNIGHT_SCENARIOS = [AM,BM,CM,DM,EM,FM,GM]

# data = [
#     [latencyMedian(AM), latencyMedian(AR)],
#     [latencyMedian(BM), latencyMedian(BR)]
# ]
# latencyIQR
# error = [
#     [latencyIQR(AM), latencyIQR(AR)],
#     [latencyIQR(BM), latencyIQR(BR)]
# ]

# w = 0.1
# fig, ax = plt.subplots()
# topics = ('Low Traffic', 'High Traffic')
# ind = np.arange(2)
# ax.bar(ind-w,data[0], yerr=error[0], color = 'blue', width = 2*w, capsize=10)
# ax.bar(ind+w,data[1], yerr=error[1], color = 'red', width = 2*w, capsize=10)
# #ax.set_yticks(np.arange(0, h+1, d))
# ax.set_xticks(ind, topics)
# ax.set_ylabel('Latency (ms)')
# ax.set_title('Uncompressed vs. Compressed')
# ax.legend(labels=['None (A)', 'gzip (B)'])
# ax.set(ylim=[00, 450])
# plt.show()


# median, iqr = stats(RUSHHOUR_SCENARIOS)
# print('Median:', median)
# print('IQR:', iqr)
# title = 'Latency by Configuration (High traffic)'
# ylabel = 'Latency (ms)'
# h = 5500
# d = 50
# barChartALL(median, iqr, title, ylabel, h, d)

# data = [
#     latencyMedianByTopic(AM),
#     latencyMedianByTopic(BM),
#     latencyMedianByTopic(CM),
#     latencyMedianByTopic(DM),
#     latencyMedianByTopic(EM),
#     latencyMedianByTopic(FM),
#     latencyMedianByTopic(GM)
# ]

# error = [
#     latencyIQRbyTopic(AM),
#     latencyIQRbyTopic(BM),
#     latencyIQRbyTopic(CM),
#     latencyIQRbyTopic(DM),
#     latencyIQRbyTopic(EM),
#     latencyIQRbyTopic(FM),
#     latencyIQRbyTopic(GM)
# ]

# data = [
#     latencyMedianByTopic(AR),
#     latencyMedianByTopic(BR),
#     latencyMedianByTopic(CR),
#     latencyMedianByTopic(DR),
#     latencyMedianByTopic(ER),
#     latencyMedianByTopic(FR),
#     latencyMedianByTopic(GR)
# ]

# error = [
#     latencyIQRbyTopic(AR),
#     latencyIQRbyTopic(BR),
#     latencyIQRbyTopic(CR),
#     latencyIQRbyTopic(DR),
#     latencyIQRbyTopic(ER),
#     latencyIQRbyTopic(FR),
#     latencyIQRbyTopic(GR)
# ]

# barChartTopics(data, error, 'Latency by Topic (High traffic)', 'Latency (ms)', 400, 50)

s_home = 133.26801323890686
s_shaunas = 129.13869694941774
d = 1000000
data = [
    # d/394.03282475471497,
    # d/147.758309841156,
    # d/274.94528675079346,
    # d/122.05667924880981,
    # d/157.55261874198914,
    # d/185.8933355808258,
    # d/120.5704710483551,
    d/s_home,
    d/s_shaunas
]

error = [
    # d/(394.03282475471497*10),
    # d/(147.758309841156*10),
    # d/(274.94528675079346*10),
    # d/(122.05667924880981*10),
    # d/(157.55261874198914*10),
    # d/(185.8933355808258*10),
    # d/(120.5704710483551*10),
    d/(s_home*10),
    d/(s_shaunas*10)
]

h = 10000
d = 1000
ylabel = 'messages/s'
#c = ['blue', 'red', 'green', 'purple', 'yellow', 'cyan','orange'] #, 'tab:gray']
#scenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] #, 'Final']
title = 'Effects of Distance on Throughput'
c = ['tab:gray', 'lightgray']
scenarios = ['Location 1 (25 km)', 'Location 2 (2.5 km)']
fig, ax = plt.subplots()
ax.bar(scenarios, data, yerr=error, color=c, capsize=10)
ax.set_yticks(np.arange(0, h+1, d))
ax.set_ylabel(ylabel)
ax.set_xlabel('Configuration')
ax.set_title(title)
plt.show()