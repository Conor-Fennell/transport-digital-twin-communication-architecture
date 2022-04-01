# transport-digital-twin-communication-architecture

Repository for Communication Architecture for Transportation Digital Twins MAI Dissertation (Electronic & Computer Engineering). 

Author: Conor Fennell 

Academic Supervisor: Prof Vinny Cahill

----------------------------------------------
3 tests

test 1
start time: 0
end time: 3600

test 2
start time: 32400
end time: 36000

test 3
start time: 50400
end time: 54000
---------------------------------------------
SCENARIO-A
brokers:  single broker, Linux/UNIX t2.large, replication 1 (default)
enterprise server: Linux/UNIX t2.large, replication 1 (default)
producer/consumers: local machine WINDOWS 10, i5-9600k @ 3.70GHZ, 32GB RAM
kafka partitions:
    topics = appendTopics(topics, 2, "inductive_loops")
    topics = appendTopics(topics, 8, "motorway_cameras")
    topics = appendTopics(topics, 1, "toll_bridge_cameras")
    topics = appendTopics(topics, 1, "probe_vehicles")  

    for topic in ENTERPRISE_TOPICS:
        enterprise_topics = appendTopics(enterprise_topics, 1, topic)    
---------------------------------------------
SCENARIO-B
brokers:  single broker, Linux/UNIX t2.large, replication 1 (default)
enterprise server: Linux/UNIX t2.large, replication 1 (default)
producer/consumers: local machine WINDOWS 10, i5-9600k @ 3.70GHZ, 32GB RAM
kafka partitions:
    topics = appendTopics(topics, 2, "inductive_loops")
    topics = appendTopics(topics, 8, "motorway_cameras")
    topics = appendTopics(topics, 1, "toll_bridge_cameras")
    topics = appendTopics(topics, 5, "probe_vehicles")  

---------------------------------------------
SCENARIO-C
brokers:  single broker, Linux/UNIX t2.large, replication 1 (default)
enterprise server: Linux/UNIX t2.large, replication 1 (default)
producer/consumers: local machine WINDOWS 10, i5-9600k @ 3.70GHZ, 32GB RAM
kafka partitions:
    topics = appendTopics(topics, 2, "inductive_loops")
    topics = appendTopics(topics, 8, "motorway_cameras")
    topics = appendTopics(topics, 1, "toll_bridge_cameras")
    topics = appendTopics(topics, 1, "probe_vehicles")  

        Increased linger ms from 0 to 1000 on enterprise server producerss & loop producers
---------------------------------------------


  EnterpriseBroker:
    image: 'bitnami/kafka:latest'
    container_name: 'EnterpriseBroker'
    ports:
      - '9093:9093'
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_LISTENERS=PLAINTEXT://:9093
      - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9093
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
    depends_on:
      - zookeeper