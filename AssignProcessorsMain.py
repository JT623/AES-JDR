from EDGE_env import GetRandomStreams,GetLongTailStreams,GetPossionStreams,GetDIS,Getmu
from Algorithm import AlgAdjPvm
import random
import numpy as np
import sys
import math

NUM_OF_STREAM = 50 # 50..250
NUM_OF_NODES = 10
NUM_OF_PODS = 20
CLASS_OF_MICROSERVICE = 10

# 传播时延矩阵
DIS = GetDIS(NUM_OF_NODES)
# 边缘节点i对于微服务j的服务强度矩阵
mu = Getmu(NUM_OF_NODES,CLASS_OF_MICROSERVICE)
# 到达率
# Avg_lamda = 3
def AssignProcessors(reqs):
    random.seed(100)
    reqs = sorted(reqs,key=lambda x:len(x),reverse=False)
    EDGE_RESOURCE = [NUM_OF_PODS for _ in range(NUM_OF_NODES)]
    N_vm = [[] for _ in range(NUM_OF_NODES)]
    _,len2lamda = GetRandomStreams(NUM_OF_STREAM,CLASS_OF_MICROSERVICE)
    # 初始化initial
    for i in range(NUM_OF_NODES):
        for _ in range(CLASS_OF_MICROSERVICE):
            N_vm[i].append(0)   
    for req in reqs:
        lamda = len2lamda.get(len(req))
        EDGE_NODE_LIST = [i for i in range(NUM_OF_NODES)]
        node = random.choice(EDGE_NODE_LIST)
        for ms in req:
            mu = Getmu(NUM_OF_NODES,CLASS_OF_MICROSERVICE)
            if EDGE_RESOURCE[node]>=1:
                N_vm[node][ms] += math.ceil(lamda/mu[node][ms])
                EDGE_RESOURCE[node] -= math.ceil(lamda/mu[node][ms])
            else:
                while EDGE_RESOURCE[node]<1:
                    EDGE_NODE_LIST.remove(node)
                    if EDGE_NODE_LIST == []:
                        print("pods不足,等待pods释放")
                    else: 
                        m = -1
                        for idx in EDGE_NODE_LIST:
                            if mu[idx][ms]>m:
                                node = idx
                                m = mu[node][ms]
                N_vm[node][ms] += 1
                EDGE_RESOURCE[node] -= math.ceil(lamda/mu[node][ms])

    N_vm = np.array(N_vm).reshape(NUM_OF_NODES,CLASS_OF_MICROSERVICE)
    return N_vm

def CalDealy(N_vm,P_vm,reqs):
    # _ , len2lamda = GetRandomStreams(NUM_OF_STREAM,CLASS_OF_MICROSERVICE)
    _ , len2lamda = GetLongTailStreams(NUM_OF_STREAM,CLASS_OF_MICROSERVICE)
    # _ ,len2lamda = GetPossionStreams(NUM_OF_STREAM,CLASS_OF_MICROSERVICE)
    Dmax = 10 #25,10
    # 执行时延
    random.seed(100)
    exetime = 0
    exeTimeList = [0 for _ in range(len(reqs))]
    for idx,req in enumerate(reqs):
        lamda = len2lamda.get(len(req))
        per = 0
        for ms in req:
            EDGE_NODES_LIST = [i for i in range(NUM_OF_NODES)]
            edge_node = random.choice(EDGE_NODES_LIST)
            while N_vm[edge_node][ms] == 0:
                EDGE_NODES_LIST.remove(edge_node)
                edge_node = random.choice(EDGE_NODES_LIST)
            if N_vm[edge_node][ms]*mu[edge_node][ms]-P_vm[ms][edge_node]*lamda == 0:
                exetime += 10 # 处理不可行解
                per += 10
            else:
                exetime += 1 / (N_vm[edge_node][ms]*mu[edge_node][ms]-P_vm[ms][edge_node]*lamda)
                per += 1 / (N_vm[edge_node][ms]*mu[edge_node][ms]-P_vm[ms][edge_node]*lamda)
            # exetime += 1 / N_vm[edge_node][ms]*mu[edge_node][ms]
        exeTimeList[idx] = per
    # print("执行时延:",exetime)
    # 路由时延
    # minDelay = sys.float_info.max
    NEWdelay = 0
    routerTimeList = [0 for _ in range(len(reqs))]
    for idx,req in enumerate(reqs):
        perRouter = 0
        EDGE_NODES_LIST = [i for i in range(NUM_OF_NODES)]
        node1 = random.choice(EDGE_NODES_LIST)
        for id,ms in enumerate(req):
            if N_vm[node1][ms] == 0 and id>0:
                node2 = random.choice(EDGE_NODES_LIST)
                while N_vm[node2][ms] == 0:
                    # EDGE_NODES_LIST.remove(node2)
                    node2 = random.choice(EDGE_NODES_LIST)
                minDelay = DIS[node1][node2]
                # for node2 in  EDGE_NODES_LIST:
                #     if N_vm[node2][ms] == 0:
                #         EDGE_NODES_LIST.remove(node2)
                #     else:
                #         minDelay = min(minDelay,DIS[node1][node2])
                        # minDelay = min(minDelay,DIS[node1][node2]*(P_vm[ms][node2]*P_vm[req[idx-1]][node1])) # 乘路由转移概率
                NEWdelay += minDelay
                perRouter += minDelay
            elif id == 0 :
                node1 = random.choice(EDGE_NODES_LIST)
            else:
                continue
        routerTimeList[idx] = perRouter
    # print("执行时延",exetime)
    # print("路由时延",NEWdelay)
    print("执行时延集合",exeTimeList)
    print("路由时延集合",routerTimeList)
    count = 0 
    for i in range(len(reqs)):
        if exeTimeList[i] + routerTimeList[i] > Dmax:
            print("Time out of max Delay")
            count += 1
    # print("请求失败数:",count)
    AWT = exetime + NEWdelay
    return AWT,count

def main():
    # random distribution
    # reqs , _ = GetRandomStreams(NUM_OF_STREAM,CLASS_OF_MICROSERVICE) 
    # long tail distribution
    reqs , _ = GetLongTailStreams(NUM_OF_STREAM,CLASS_OF_MICROSERVICE)
    # possion distribution
    # reqs , _ = GetPossionStreams(NUM_OF_STREAM,CLASS_OF_MICROSERVICE

    np.random.seed(100)
    P_vm = np.random.dirichlet(np.ones(NUM_OF_NODES),size=CLASS_OF_MICROSERVICE)
    mscount = 0
    delay = 0
    Failcount = 0
    left = 0
    for idx,req in enumerate(reqs):
        mscount += len(req)
        if mscount>NUM_OF_NODES*NUM_OF_PODS:
            streams= reqs[left:idx]
            N_vm = AssignProcessors(streams)
            P_vm = AlgAdjPvm(N_vm,P_vm,NUM_OF_NODES,CLASS_OF_MICROSERVICE)
            delay += CalDealy(N_vm,P_vm,streams)[0]
            Failcount += CalDealy(N_vm,P_vm,streams)[1]
            # reqs = np.delete(reqs,[i for i in range(idx-1)],0)
            # reqs = reqs[idx:]
            mscount = len(req)
            left =  idx
        else:
            continue
    streams = reqs[left:]
    N_vm = AssignProcessors(streams)
    P_vm = AlgAdjPvm(N_vm,P_vm,NUM_OF_NODES,CLASS_OF_MICROSERVICE)
    delay += CalDealy(N_vm,P_vm,streams)[0]
    Failcount += CalDealy(N_vm,P_vm,streams)[1]
    SucessRate = (len(reqs) - Failcount) / len(reqs)
    print("总时延为:",delay)
    print("请求成功率:",SucessRate)
            
if __name__ == "__main__":
    main()