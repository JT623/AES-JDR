from gurobipy import *
from EDGE_env import GetRandomStreams,GetLongTailStreams,GetPossionStreams,GetDIS,Getmu
from Algorithm import AlgAdjNvm,AlgAdjPvm
import random
import numpy as np
import sys
# ============部署解空间===============
# 二维矩阵 Nv^m = M*N,表示边缘节点i部署微服务j实例数量
#     0 1 2 ...
# 0   1 0 3
# 1   0 2 1
# 2   ...
# 3   ...
NUM_OF_STREAM = 50 # num of stream 50....250
NUM_OF_NODES = 10
NUM_OF_PODS = 20
CLASS_MICRESERVICE = 10
# 传播时延矩阵
DIS = GetDIS(NUM_OF_NODES)
# 边缘节点i对于微服务j的服务强度矩阵
mu = Getmu(NUM_OF_NODES,CLASS_MICRESERVICE)
# 到达率
max_lamda = 7
# Create a new model
def GurobiDeploy(reqs):
    
    model = Model("MICROSERVICE")
    # 定义部署解空间
    N_v = {} 
    for i in range(NUM_OF_NODES):
        for j in range(CLASS_MICRESERVICE):
            name = 'x_'+ str(i) + str(j)
            N_v[i,j] = model.addVar(0,10,vtype = GRB.CONTINUOUS,name=name)

    # 定义约束 : s.t.(1)
    for i in range(NUM_OF_NODES):
        POD_SUM = LinExpr(0) 
        for j in range(CLASS_MICRESERVICE):
            POD_SUM.addTerms(1,N_v[i,j])
        model.addConstr(POD_SUM<=NUM_OF_PODS)

    # 定义约束 : 微服务必须布置在其中一个节点上
    for ms in range(CLASS_MICRESERVICE):
        ms_sum = LinExpr(0)
        for node in range(NUM_OF_NODES):
            ms_sum.addTerms(1,N_v[node,ms])
        model.addConstr(ms_sum>=1)

    # 部署概率 微服务i部署在边缘节点上j的概率，由延迟和路由决定
    P_vm = {} 
    for i in range(CLASS_MICRESERVICE):
        for j in range(NUM_OF_NODES):
            name = 'p_' + str(i) + str(j)
            P_vm[i,j] = model.addVar(0,1,vtype = GRB.CONTINUOUS,name = name)

    # 定义约束 : s.t.(2)(3)
    for i in range(CLASS_MICRESERVICE):
        P_sum = LinExpr(0) 
        for j in range(NUM_OF_NODES):
            P_sum.addTerms(1,P_vm[i,j])
            model.addConstr(P_vm[i,j]<=N_v[j,i]/NUM_OF_PODS)
            model.addConstr(P_vm[i,j]>=0)
        model.addConstr(P_sum == 1)

    # 定义约束 : s.t.(4)(5)
    for i in range(NUM_OF_NODES):
        for j in range(CLASS_MICRESERVICE):
            model.addConstr(N_v[i,j]*mu[i][j]>=P_vm[j,i]*max_lamda, name = 'lamda_' + str(i) + str(j))
    # 计算时延Df
    Dealy = 0
    EDGE_NODES_LIST = [i for i in range(NUM_OF_NODES)]
    x={}
    random.seed(10)
    # _,len2lamda = GetRandomStreams(NUM_OF_STREAM,CLASS_MICRESERVICE)
    _,len2lamda = GetLongTailStreams(NUM_OF_STREAM,CLASS_MICRESERVICE)
    for req in reqs:
        lamda = len2lamda.get(len(req))
        for ms in req:
            edge_node = random.choice(EDGE_NODES_LIST)
            x[edge_node,ms] = model.addVar(0,500,vtype = GRB.CONTINUOUS) # 辅助变量 gurobi不支持除法
            ExeTimeOfDelay = (N_v[edge_node,ms]*mu[edge_node][ms]-P_vm[ms,edge_node]*lamda)
            model.addConstr(x[edge_node,ms]*ExeTimeOfDelay==1)
            Dealy += x[edge_node,ms]

    # Set objective
    model.setObjective(Dealy, GRB.MINIMIZE)
    model.Params.NonConvex = 2
    model.Params.MIPGap = 10**(-4) # 设置求解混合整数规划的 Gap
    model.Params.TimeLimit = 10 # 设置最长求解时间
    model.optimize()

    # print('Obj:', model.objVal)

    # 查看是否存在负值的情况
    for k in N_v.keys():
        if N_v[k].x<0:
            print(N_v[k].VarName + '=' ,N_v[k].x)
    for k in P_vm.keys():
        if P_vm[k].x<0:
            print(P_vm[k].VarName + '=' ,P_vm[k].x)

    N_vm = []
    for k in N_v.keys():
        N_vm.append(N_v[k].x)
    N_vm = np.array(N_vm).reshape(NUM_OF_NODES,CLASS_MICRESERVICE)
    print("====================部署解空间===================")
    print(N_vm)

    p_vm = []
    for k in P_vm.keys():
        p_vm.append(P_vm[k].x)
    p_vm = np.array(p_vm).reshape(CLASS_MICRESERVICE,NUM_OF_NODES)
    print("=====================概率空间========================")
    print(p_vm)

    print("====================调整解空间====================")
    DEPLOY = AlgAdjNvm(N_vm,NUM_OF_NODES,CLASS_MICRESERVICE)
    print(DEPLOY)

    # sum1 =[]
    # for i in range(len(DEPLOY)):
    #     sum1.append(sum(DEPLOY[i]))
    # print("部署资源和",sum1)

    print("开始调整概率......")
    PADJ = AlgAdjPvm(N_vm=DEPLOY,P_vm=p_vm,num_of_nodes=NUM_OF_NODES,num_of_ms=CLASS_MICRESERVICE)
    print("===================调整概率空间===================")
    print(PADJ)
    return DEPLOY,PADJ

def CalDealy(DEPLOY,PADJ,reqs):
    # _ , len2lamda = GetRandomStreams(NUM_OF_STREAM,CLASS_MICRESERVICE)
    _ , len2lamda = GetLongTailStreams(NUM_OF_STREAM,CLASS_MICRESERVICE)
    Dmax = 10 # 25,10
    # 执行时延
    random.seed(10)
    exetime = 0
    ExeTimeList = [0 for _ in range(len(reqs))]
    for idx,req in enumerate(reqs):
        per = 0
        lamda = len2lamda.get(len(req))
        for ms in req:
            EDGE_NODES_LIST = [i for i in range(NUM_OF_NODES)]
            edge_node = random.choice(EDGE_NODES_LIST)
            while DEPLOY[edge_node][ms] == 0:
                EDGE_NODES_LIST.remove(edge_node)
                edge_node = random.choice(EDGE_NODES_LIST)
            if DEPLOY[edge_node][ms]*mu[edge_node][ms]-PADJ[ms][edge_node]*lamda == 0:
                exetime += 10
                per += 10
            else:
                exetime += 1 / (DEPLOY[edge_node][ms]*mu[edge_node][ms]-PADJ[ms][edge_node]*lamda)
                per  += 1 / (DEPLOY[edge_node][ms]*mu[edge_node][ms]-PADJ[ms][edge_node]*lamda)
        ExeTimeList[idx] = per
    # print("执行时延:",exetime)
    # 路由时延
    NEWdelay = 0
    RouterTimeList =[0 for _ in range(len(reqs))]
    for idx,req in enumerate(reqs):
        minDelay = sys.float_info.max
        perRouter = 0
        EDGE_NODES_LIST = [i for i in range(NUM_OF_NODES)]
        node1 = random.choice(EDGE_NODES_LIST)
        for id,ms in enumerate(req):
            if DEPLOY[node1][ms] == 0 and id>0:
                for node2 in  EDGE_NODES_LIST:
                    if DEPLOY[node2][ms] == 0:
                        continue
                    else:
                        minDelay = min(minDelay,DIS[node1][node2])
                        # minDelay = min(minDelay,DIS[node1][node2]*(PADJ[ms][node2]*PADJ[req[idx-1]][node1])) # 乘路由转移概率
                NEWdelay += minDelay
                perRouter += minDelay
            elif id == 0 :
                node1 = random.choice(EDGE_NODES_LIST)
            else:
                continue
        RouterTimeList[idx] = perRouter
    # print("路由时延:",NEWdelay)
    NEW_AWT = exetime + NEWdelay
    # print("总时延为: ",NEW_AWT)
    print("执行时延集合",ExeTimeList)
    print("路由时延集合",RouterTimeList)
    count = 0 
    for i in range(len(reqs)):
        if ExeTimeList[i] + RouterTimeList[i] > Dmax:
            print("Time out of max Delay")
            count += 1
    # print("请求失败数:",count)
    return NEW_AWT,count

def main():
    # random distribution
    # reqs , _ = GetRandomStreams(NUM_OF_STREAM,CLASS_MICRESERVICE) 
    # long tail distribution
    reqs , _ = GetLongTailStreams(NUM_OF_STREAM,CLASS_MICRESERVICE)
    mscount = 0
    delay = 0
    Failcount = 0
    left = 0 
    for idx,req in enumerate(reqs):
        mscount += len(req)
        if mscount>NUM_OF_NODES*NUM_OF_PODS:
            streams = reqs[left:idx]
            N_vm,P_vm = GurobiDeploy(streams)
            delay += CalDealy(N_vm,P_vm,streams)[0]
            Failcount += CalDealy(N_vm,P_vm,streams)[1]
            mscount = len(req)
            left = idx
        else:
            continue
    streams = reqs[left:]
    N_vm, P_vm = GurobiDeploy(streams)
    delay += CalDealy(N_vm,P_vm,streams)[0]
    Failcount += CalDealy(N_vm,P_vm,streams)[1]
    SucessRate = (len(reqs) - Failcount) / len(reqs)
    print("总时延为:",delay)
    print("请求成功率:",SucessRate)

if __name__ == "__main__":
    main()