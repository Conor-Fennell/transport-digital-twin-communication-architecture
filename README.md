# transport-digital-twin-communication-architecture

Repository for Communication Architecture for Transportation Digital Twins MAI Dissertation (Electronic & Computer Engineering). 

Author: Conor Fennell 

Academic Supervisor: Prof Vinny Cahill

#----------------------------------------------------------------------

## Abstract ##

A digital twin is a virtual representation of a system which is updated from real-time data, providing accurate information about the current state of the system and allows for predictions on future states of the system. 

Motorway traffic has been growing year on year with the ever increasing people and vehicle population. With this growth comes the risk of increased congestion, traffic accidents, and roadworks. These issues could be reduced with real-time traffic monitoring. A method of real-time traffic monitoring could be possible with a digital twin of the motorway. 

In order to create a digital twin, traffic data from the motorway is needed. This data must be real time and readily available. Several sensors exist on modern motorways such as inductive loops, road gantry cameras, and radar detectors. Others data sources can be found directly on vehicles such as GPS devices. The data from these sensors can be used to feed the digital twin. 

Apache Kafka is a distributed messaging service which is based on a publisher-subscriber architecture. In Apache Kafka data can be partitioned into 'partitions' which are within different 'topics'. 

This research explores the use of Apache Kafka as the communication service between the motorway sensors and the digital twin. The objective is to create a highly available system which can provide high throughput and low latency. The proposed system implements topics per sensor group and partitioning per individual sensor. The research also explores the properties of the motorway sensors, focusing on the type of data they produce and the associated latency.

The proposed Apache Kafka data delivery architecture is evaluated using simulated data streams. These simulated data streams are taken from virtual sensors which draw data from a SUMO (Simulation of Urban Mobility) simulation of the M50 motorway in Dublin. 

This report evaluates the simulations conducted. It was found that single broker designs offer the highest performance in terms of latency, however these systems have a single point of failure. It was found that compression can decrease the latency by approximately 7\%. Compression also increases the throughput of the system by 40\%. The use of multiple consumers also improves the throughput of the system by a further 21\%.

The final solution is a 3 broker configuration. This systems uses compression to decrease the latency of the system. The system has replication across the brokers in order to increase the availability of the service. The final solution has a dedicated consumer per topic. This system experiences approximately 200 ms of latency in low traffic simulations, and 275 ms latency in high traffic simulations. 