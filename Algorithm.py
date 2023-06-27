import math
import random

random.seed(10)
def AlgAdjNvm(N_vm,num_of_nodes,num_of_ms):
    for i in range(num_of_nodes):
        flag = 0
        for j in range(num_of_ms):
            # if (math.ceil(N_vm[i][j])-N_vm[i][j]) == 0.5:
            #     p = random.uniform(0,1)
            #     if p>0.5:
            #         N_vm[i][j] = math.ceil(N_vm[i][j])
            #         flag += math.ceil(N_vm[i][j])-N_vm[i][j]
            #     else:
            #         N_vm[i][j] = math.floor(N_vm[i][j])
            #         flag -= N_vm[i][j]-math.floor(N_vm[i][j])
            # else:
            label = round(N_vm[i][j])
            if label-N_vm[i][j]>=0:
                flag += label-N_vm[i][j]
            else:
                flag -= N_vm[i][j]-label
            if flag>=0.99:
                flag -= 2*(label-N_vm[i][j])
                N_vm[i][j] = math.floor(N_vm[i][j])
            else:
                N_vm[i][j] = round(N_vm[i][j])

    return N_vm

def AlgAdjPvm(N_vm,P_vm,num_of_nodes,num_of_ms):
    for node in range(num_of_nodes):
        for ms in range(num_of_ms):
            if N_vm[node][ms] == 0:
                P_vm[ms][node] = 0
            else:
                continue
    for ms in range(num_of_ms):
        for node in range(num_of_nodes):
            if P_vm[ms][node] != 0:
                P_vm[ms][node] = P_vm[ms][node] / sum(P_vm[ms])
            else:
                continue
    return P_vm