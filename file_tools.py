import os, errno

def writeMessageToFile(partition, topic, data):
    path = './consumed_topics/'+str(topic)+'/'

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    with open(path+str(partition)+'.txt', "a") as f:
        f.write(str(data)+'\n')
    