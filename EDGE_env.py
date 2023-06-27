import random
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

# random generate request flow
def GetRandomStreams(NUM_OF_STREAM,CLASS_MICROSERVICES):
    len2lamda = {}
    lamda = [1,2,3,5,7]
    user_streams = [[] for _ in range(NUM_OF_STREAM)]
    random.seed(100)
    for i in range(NUM_OF_STREAM):
        ms_len = random.randint(2,6)
        len2lamda[ms_len] = random.choice(lamda)
        ms_set = [i for i in range(CLASS_MICROSERVICES)]
        for _ in range(ms_len):
            ms = random.choice(ms_set)
            user_streams[i].append(ms)
            ms_set.remove(ms)
    print("======================Random Distributed Streams:===========================" + "\n",user_streams)
    return user_streams,len2lamda

def GetLongTailStreams(num_of_streams,class_microservices):
    ms_len = np.arange(2,7,1)
    lamda = [1,2,3,5,7]
    pdf = stats.lognorm.pdf(ms_len,2/3,1,np.exp(1))
    pdf = np.array(pdf)
    count = []
    for p in pdf:
        count.append(round(num_of_streams*(p/sum(pdf))))
    # 误差拉伸
    if sum(count)<num_of_streams:
        count[count.index(max(count))] += num_of_streams-sum(count)
    elif sum(count)>num_of_streams:
        count[count.index(max(count))] -= sum(count) - num_of_streams
    count = np.array(count)
    len2num = {}
    for idx in range(len(count)):
        len2num[ms_len[idx]] = count[idx]
    sort = sorted(len2num.items(),key=lambda x:x[1])
    len2lamda = {}
    for idx in range(len(count)):
        len2lamda[sort[idx][0]] = lamda[idx]
    # plot
    # plt.subplots_adjust(hspace=0.5)
    # plt.subplot(211)
    # plt.plot(ms_len,pdf,linestyle='None',marker='o')
    # plt.vlines(ms_len,0,pdf)
    # plt.xlabel('Length of Request Chain')
    # plt.ylabel('Probability')
    # plt.title("Streams by Long Tail Distribution")
    # plt.subplot(212)
    # plt.bar(ms_len,count)
    # plt.xlabel('Length of Request Chain')
    # plt.ylabel('Number of Request Chain')
    # plt.show()

    # generate streams
    random.seed(1037)
    user_streams = []
    for item in len2num.items():
        ms_len = item[0]
        num = item[1]
        for _ in range(num):
            stream = []
            ms_set = [i for i in range(class_microservices)]
            for _ in range(ms_len):
                ms = random.choice(ms_set)
                stream.append(ms)
                ms_set.remove(ms)
            user_streams.append(stream)
    random.shuffle(user_streams)
    print(len(user_streams))
    print("======================Long Tail Distributed Streams:===========================" + "\n",user_streams)

    return user_streams,len2lamda

def GetPossionStreams(num_of_streams,class_microseverces):
    # streamsLen = np.random.normal(4,2/3,num_of_streams) # 3-sigma rule
    # for i in range(len(streamsLen)):
    #     streamsLen[i] = round(streamsLen[i])
    # print(streamsLen)
    # plt.hist(streamsLen,5)
    # plt.show()
    # plt.figure()
    # streams = np.random.poisson(4,100)
    # plt.hist(streams,50)
    # plt.show()
    # print(streams)
    AVG = 4
    lamda = [1,2,3,5,7]
    ms_len = np.arange(2,7,1)
    pList = stats.poisson.pmf(ms_len,AVG)
    count = []
    for p in pList:
        count.append(round(num_of_streams*(p/sum(pList))))

    if sum(count) < num_of_streams:
        count[count.index(max(count))] += num_of_streams-sum(count)
    elif sum(count) > num_of_streams:
        count[count.index(max(count))] -= sum(count) - num_of_streams
    
    len2num = {}
    for idx in range(len(count)):
        len2num[ms_len[idx]] = count[idx]
    
    len2lamda = {}
    sort = sorted(len2num.items(),key=lambda x:x[1])
    for idx in range(len(sort)):
        len2lamda[sort[idx][0]] = lamda[idx]
    
    # plot
    # plt.subplots_adjust(hspace=0.5)
    # plt.subplot(211)
    # plt.plot(ms_len,pList,linestyle='None',marker='o')
    # plt.vlines(ms_len,0,pList)
    # plt.xlabel('Length of Request Chain')
    # plt.ylabel('Probability')
    # plt.title('Possion Distribute: Average Length of Chain lamda=%i'%AVG)
    # plt.subplot(212)
    # plt.bar(ms_len,count)
    # plt.xlabel('Length of Request Chain')
    # plt.ylabel('Number of Request Chain')
    # plt.show()

    # generate streams
    user_streams = []
    # random.seed(1037)
    for item in len2num.items():
        ms_num = item[1]
        ms_len = item[0]
        for _ in range(ms_num):
            ms_set = [i for i in range(class_microseverces)]
            stream = []
            for _ in range(ms_len):
                ms = random.choice(ms_set)
                stream.append(ms)
                ms_set.remove(ms)
            user_streams.append(stream)
    random.shuffle(user_streams)
    print(len(user_streams))
    print("==========================Possion Distribution Sreams====================================" + "\n",user_streams)

def GetDIS(NUM_OF_NODES):
    random.seed(1037)
    # 传播时延矩阵
    C = 100 # light speed 
    DIS = [[] for _ in range(NUM_OF_NODES)]
    for i in range(NUM_OF_NODES):
        for j in range(NUM_OF_NODES):
            if i==j:
                DIS[i].append(0)
            else:
                DIS[i].append(random.randint(1000,3000) / C)
    
    print("+++++++++++++时延传播矩阵++++++++++++" + "\n",DIS)
    return DIS

def Getmu(NUM_OF_NODES,CLASS_MICROSERVICES):
    random.seed(1037)
    mu = [[] for _ in range(NUM_OF_NODES)] # 边缘节点i对于微服务j的服务强度矩阵
    for i in range(NUM_OF_NODES):
        for _ in range(CLASS_MICROSERVICES):
            mu[i].append(random.randint(8,10))
    print("++++++++++++服务速率矩阵+++++++++++++" + "\n",mu)
    return mu

#############test#################
if __name__ == "__main__":
    # GetRandomStreams(100,10)
    # GetPossionStreams(100,10)
    GetLongTailStreams(50,10)