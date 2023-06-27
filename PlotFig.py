import matplotlib.pyplot as plt
plt.rc('font',family='Times New Roman')
import numpy as np
# random distribution figures

# figure 1 
# seed 100
# Time of Total Delay by Num of Requests
num_of_streams = [50,100,150,200,250]
Delay_random = [405.2814395903947,1210.9104314725012,1439.9758285718476,1708.8797446899457,2043.5509874358263]
Delay_greedy = [329.6279820192158,772.9039563157978,993.7593262452936,1272.795037054864,1289.4996170695817]
Delay_assign = [312.7982841619922,900.5174151023755,1146.2232493626652,1379.4627125273387,1576.4958975622596]
Delay_gurobi = [241.7237425560793,756.6804510814877,800.2489202753384,992.4818721918732,1227.8883070384131]
plt.figure()
plt.plot(num_of_streams,Delay_random,label = "Random",color = "b",marker = "o",linestyle = "-",linewidth = 1.5)
plt.plot(num_of_streams,Delay_assign,label = "AssignProcessors",color = "c",marker = "x",linestyle = "-",linewidth = 1.5)
plt.plot(num_of_streams,Delay_greedy,label = "AssignProcessors*",color = "g",marker = "s",linestyle = "-",linewidth = 1.5)
plt.plot(num_of_streams,Delay_gurobi,label = "Ours",color = "r",marker = "*",linestyle = "-",linewidth = 1.5)
plt.legend(loc = "upper left")
plt.xticks(num_of_streams)
plt.xlabel("Num of Requests")
plt.ylabel("Time of Total Delay")
plt.title("Time of Total Delay by Num of Requests")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()

# figure 2
# Success Rate by Num of Request
num_of_streams = [50,100,150,200,250]
x = np.arange(len(num_of_streams))
total_width, n = 0.8,4
width = total_width / n
xticks = x - (total_width-width) / 2

Rate_random = [0.84,0.77,0.8333333333333334,0.865, 0.868]
Rate_greedy = [0.88,0.85, 0.8866666666666667,0.895,0.92]
Rate_assign =[0.92,0.86, 0.9066666666666666,0.9,0.932]
Rate_gurobi = [0.96,0.94,0.9333333333333333,0.98,0.948]

plt.figure()
plt.bar(xticks,Rate_random,width=width,label="Random",color = "orange")
plt.bar(xticks+width,Rate_assign,width=width,label="AssignProcessors",color = "lightgreen")
plt.bar(xticks+2*width,Rate_greedy,width = width,label="AssignProcessors*",color="peachpuff")
plt.bar(xticks+3*width,Rate_gurobi,width = width,label="Ours",color="deepskyblue")
# plt.plot(num_of_streams,Rate_random,label = "Random",color = "b",marker = "o",linestyle = "-",linewidth = 1.5)
# plt.plot(num_of_streams,Rate_greedy,label = "Greedy",color = "g",marker = "s",linestyle = "-",linewidth = 1.5)
# plt.plot(num_of_streams,Rate_assign,label = "AssignProcessors",color = "c",marker = "x",linestyle = "-",linewidth = 1.5)
# plt.plot(num_of_streams,Rate_gurobi,label = "Ours",color = "r",marker = "*",linestyle = "-",linewidth = 1.5)
plt.legend(loc = "lower right")
plt.xticks(x,num_of_streams)
plt.xlabel("Num of Requests")
plt.ylabel("Success Rate")
plt.title("Success Rate by Num of Requests")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()

# # figure 3
# # change length of chain, num of stream is 200
length = [2,3,4,5,6]
Delay_random = [653.8685011814057,989.8680860159052,1216.342847326784,2103.133618699523,2492.330892631715]
Delay_assign = [405.262141521007,780.4014007790431,1083.7516165585132,1736.411067415465,1908.5061102428012]
Delay_greedy = [378.7904337763991,733.6048138745015,997.2812487238152,1490.80667551648,1825.2982050427938]
Delay_gurobi = [254.27339351200345,708.015368825438, 888.6508049261208,1426.1717298994893,1527.414804097478]

plt.figure()
plt.plot(length,Delay_random,label = "Random",color = "b",marker = "o",linestyle = "-",linewidth = 1.5)
plt.plot(length,Delay_assign,label = "AssignProcessors",color = "c",marker = "x",linestyle = "-",linewidth = 1.5)
plt.plot(length,Delay_greedy,label = "AssignProcessors*",color = "g",marker = "s",linestyle = "-",linewidth = 1.5)
plt.plot(length,Delay_gurobi,label = "Ours",color = "r",marker = "*",linestyle = "-",linewidth = 1.5)
plt.legend(loc = "upper left")
plt.xticks(length)
plt.xlabel("Length of Request Chain")
plt.ylabel("Time of Total Delay")
plt.title("Time of Total Delay by Length of Request Chain")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()

# figure 4
length = [2,3,4,5,6]
x = np.arange(len(length))
total_width, n = 0.8,4
width = total_width / n
xticks = x - (total_width-width) / 2
# xstick = ["2~3","3~4","3~4","5~6","6~7"]
Rate_random = [0.955,0.93,0.93,0.83,0.8]
Rate_assign = [0.96,0.945,0.935,0.925,0.88]
Rate_greedy = [0.97,0.965,0.94,0.935,0.89]
Rate_gurobi = [1,0.98,0.99,0.965,0.945]
plt.figure()
plt.bar(xticks,Rate_random,width=width,label="Random",color = "orange")
plt.bar(xticks+width,Rate_assign,width=width,label="AssignProcessors",color = "lightgreen")
plt.bar(xticks+2*width,Rate_greedy,width = width,label="AssignProcessors*",color="peachpuff")
plt.bar(xticks+3*width,Rate_gurobi,width = width,label="Ours",color="deepskyblue")
# plt.plot(length,Rate_random,label = "Random",color = "b",marker = "o",linestyle = "-",linewidth = 1.5)
# plt.plot(length,Rate_greedy,label = "Greedy",color = "g",marker = "s",linestyle = "-",linewidth = 1.5)
# plt.plot(length,Rate_assign,label = "AssignProcessors",color = "c",marker = "x",linestyle = "-",linewidth = 1.5)
# plt.plot(length,Rate_gurobi,label = "Ours",color = "r",marker = "*",linestyle = "-",linewidth = 1.5)
plt.legend(loc = "lower right")
plt.xticks(x,length)
plt.xlabel("Length of Request Chain")
plt.ylabel("Success Rate")
plt.title("Success Rate by Length of Request Chain")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()

# figure 5
# change num of pods, num of stream is 50
num_of_pods = [10,12,14,16,18,20]
Delay_random = [1125.207151245989,1038.5291029636287,921.2036824148493,787.4787110537084,674.3690694053282,405.2814395903947]
Delay_assign = [1019.9220940869197,879.0172122814722,845.2442176785653,763.2880106201837,604.7960104225904,379.64010073219316]
Delay_greedy = [880.4632878127953,795.0127481845398,753.9734511691366,709.862784287835,586.96597011261673,329.6279820192158]
Delay_gurobi = [809.6709505841322,566.6345683282539,523.2683675725502,453.1168116355325,438.628590153048,241.7237425560793]
plt.figure()
plt.plot(num_of_pods,Delay_random,label = "Random",color = "b",marker = "o",linestyle = "-",linewidth = 1.5)
plt.plot(num_of_pods,Delay_assign,label = "AssignProcessors",color = "c",marker = "x",linestyle = "-",linewidth = 1.5)
plt.plot(num_of_pods,Delay_greedy,label = "AssignProcessors*",color = "g",marker = "s",linestyle = "-",linewidth = 1.5)
plt.plot(num_of_pods,Delay_gurobi,label = "Ours",color = "r",marker = "*",linestyle = "-",linewidth = 1.5)
plt.legend(loc = "upper right")
plt.xticks(num_of_pods)
plt.xlabel("Num of Pods")
plt.ylabel("Time of Total Delay")
plt.title("Time of Total Delay by Num of Pods")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()

# figure 6
num_of_pods = [10,12,14,16,18,20]
x = np.arange(len(num_of_pods))
total_width, n = 0.8,4
width = total_width / n
xticks = x - (total_width-width) / 2
Rate_random = [0.6,0.62,0.64,0.74,0.74,0.84]
Rate_assign= [0.62, 0.7, 0.72, 0.76, 0.8, 0.92]
Rate_greedy = [0.76,0.76,0.78,0.82,0.84,0.88]
Rate_gurobi = [0.8,0.84,0.86,0.92,0.96,0.96]
plt.figure()
plt.bar(xticks,Rate_random,width=width,label="Random",color = "orange")
plt.bar(xticks+width,Rate_assign,width=width,label="AssignProcessors",color = "lightgreen")
plt.bar(xticks+2*width,Rate_greedy,width = width,label="AssignProcessors*",color="peachpuff")
plt.bar(xticks+3*width,Rate_gurobi,width = width,label="Ours",color="deepskyblue")
# plt.plot(num_of_pods,Rate_random,label = "Random",color = "b",marker = "o",linestyle = "-",linewidth = 1.5)
# plt.plot(num_of_pods,Rate_assign,label = "AssignProcessors",color = "c",marker = "x",linestyle = "-",linewidth = 1.5)
# plt.plot(num_of_pods,Rate_greedy,label = "Greedy",color = "g",marker = "s",linestyle = "-",linewidth = 1.5)
# plt.plot(num_of_pods,Rate_gurobi,label = "Ours",color = "r",marker = "*",linestyle = "-",linewidth = 1.5)
plt.legend(loc = "lower right")
plt.xticks(x,num_of_pods)
plt.xlabel("Num of Pods")
plt.ylabel("Success Rate")
plt.title("Success Rate by Length of Num of Pods")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()

# # figure 7
# change trans speed, num of srtreams is 50
C = [100,125,150,175,200]

Delay_random = [405.2814395903947,327.44343959039475,275.55143959039475,238.48572530468044,210.68643959039474]
Delay_assign = [379.64010073219316,307.0001007321932,258.5734340655265,223.98295787505032,198.0401007321932]
Delay_greedy = [329.6279820192158,267.1299820192158,225.46464868588245,195.70369630493008,173.38298201921577]
Delay_gurobi = [241.7237425560793,195.9977425560793,165.5137425560793,143.7394568417936,127.4087425560793]

plt.figure()
plt.plot(C,Delay_random,label = "Random",color = "b",marker = "o",linestyle = "-",linewidth = 1.5)
plt.plot(C,Delay_assign,label = "AssignProcessors",color = "c",marker = "x",linestyle = "-",linewidth = 1.5)
plt.plot(C,Delay_greedy,label = "AssignProcessors*",color = "g",marker = "s",linestyle = "-",linewidth = 1.5)
plt.plot(C,Delay_gurobi,label = "Ours",color = "r",marker = "*",linestyle = "-",linewidth = 1.5)
plt.legend(loc = "upper right")
plt.xticks(C)
plt.xlabel("Propagation Velocity")
plt.ylabel("Time of Total Delay")
plt.title("Time of Total Delay by Propagation Velocity")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()

# figure 8
# change trans speed, num of srtreams is 50,Dmax = 10
C = [100,125,150,175,200]
x = np.arange(len(C))
total_width, n = 0.8,4
width = total_width / n
xticks = x - (total_width-width) / 2

Rate_random = [0.72,0.74,0.76,0.8,0.82]
Rate_assign= [0.66, 0.72,0.78, 0.82,0.84]
Rate_greedy = [0.7,0.72,0.8,0.82,0.82]
Rate_gurobi = [0.76,0.8,0.94,0.94,0.94]
plt.bar(xticks,Rate_random,width=width,label="Random",color = "orange")
plt.bar(xticks+width,Rate_assign,width=width,label="AssignProcessors",color = "lightgreen")
plt.bar(xticks+2*width,Rate_greedy,width = width,label="AssignProcessors*",color="peachpuff")
plt.bar(xticks+3*width,Rate_gurobi,width = width,label="Ours",color="deepskyblue")
plt.legend(loc = "lower right")
plt.xticks(x,C)
plt.xlabel("Propagation Velocity")
plt.ylabel("Success Rate")
plt.title("Success Rate by Propagation Velocity")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()