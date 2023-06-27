import matplotlib.pyplot as plt
import numpy as np
# Lontail distribution figures 
# figure 1 
# seed 2
# Time of Total Delay by Num of Requests
num_of_streams = [50,100,150,200,250]
Delay_random = [514.2560200551181,546.4267344959477,914.5244939259353,2064.5645188325543,1917.7460380140724]
Delay_assign = [535.9525360233542,561.2018277910462,876.9824598943446,1453.092931130401,1772.3523846246635]
Delay_greedy = [373.50211888432364,664.0493821285818, 835.68442293444,1182.775438708456,1617.7704731075646]
Delay_gurobi = [197.85287768725675,418.9875753004037, 661.9089302530922,688.7727580357507,1406.4914639437236]
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

Rate_random = [0.76,0.93,0.9066666666666666,0.84,0.88]
Rate_assign = [0.8,0.92,0.9,0.89,0.9]
Rate_greedy = [0.88,0.91,0.9,0.93,0.912]
Rate_gurobi = [1.0,1.0,0.96,0.99,0.956]

plt.figure()
plt.bar(xticks,Rate_random,width=width,label="Random",color = "orange")
plt.bar(xticks+width,Rate_assign,width=width,label="AssignProcessors",color = "lightgreen")
plt.bar(xticks+2*width,Rate_greedy,width = width,label="AssignProcessors*",color="peachpuff")
plt.bar(xticks+3*width,Rate_gurobi,width = width,label="Ours",color="deepskyblue")
plt.legend(loc = "lower right")
plt.xticks(x,num_of_streams)
plt.xlabel("Num of Requests")
plt.ylabel("Success Rate")
plt.title("Success Rate by Num of Requests")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()

# figure 3
# change num of pods, num of stream is 50
num_of_pods = [10,12,14,16,18,20]
Delay_random = [927.678890618323,839.6317477542661,983.7234842197042,695.1781932338619,599.8731103747008,514.2560200551181]
Delay_assign = [942.7402228921039,590.2530169879365,622.9645930100157,496.8900938375326,384.54755377351682,535.9525360233542]
Delay_greedy = [665.4138161831538, 533.9464340287545,609.7044560540998,472.6980678696237,313.19879353730204,373.50211888432364]
Delay_gurobi = [643.2735773820698,440.15182705766415,508.9621626243305, 397.9817872809621,211.2951401814128,197.85287768725675]
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

# figure 4
num_of_pods = [10,12,14,16,18,20]
x = np.arange(len(num_of_pods))
total_width, n = 0.8,4
width = total_width / n
xticks = x - (total_width-width) / 2
Rate_random = [0.62,0.72,0.68,0.84,0.74,0.76]
Rate_assign= [0.74,0.8,0.8,0.88,0.98,0.8]
Rate_greedy = [0.74,0.86,0.78,0.86,0.96,0.88]
Rate_gurobi = [0.8,0.94,0.92,0.96,1.0,1.0]

plt.figure()
plt.bar(xticks,Rate_random,width=width,label="Random",color = "orange")
plt.bar(xticks+width,Rate_assign,width=width,label="AssignProcessors",color = "lightgreen")
plt.bar(xticks+2*width,Rate_greedy,width = width,label="AssignProcessors*",color="peachpuff")
plt.bar(xticks+3*width,Rate_gurobi,width = width,label="Ours",color="deepskyblue")
plt.legend(loc = "lower right")
plt.xticks(x,num_of_pods)
plt.xlabel("Num of Pods")
plt.ylabel("Success Rate")
plt.title("Success Rate by Length of Num of Pods")
plt.grid(True,linestyle="--",color="gray",linewidth="0.5",axis="both")
plt.show()

# # figure 5 
# seed 1037
# change trans speed, num of srtreams is 50
C = [100,125,150,175,200]
Delay_random = [355.6176865596216,286.5396865596216,240.48768655962164,207.5934008453359,182.92268655962158]
Delay_assign = [313.58663827309323,253.4746382730932, 213.39997160642656,184.77520970166466,163.30663827309323]
Delay_greedy = [191.97474489739432,156.36874489739435, 132.631411564061,115.67617346882291,102.95974489739432]
Delay_gurobi = [140.68227805291832,114.49027805291831,97.02894471958497,84.55656376720403,75.2022780529183]

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

# figure 6
# change trans speed, num of srtreams is 50,Dmax = 10
C = [100,125,150,175,200]
x = np.arange(len(C))
total_width, n = 0.8,4
width = total_width / n
xticks = x - (total_width-width) / 2

Rate_random = [0.72,0.74,0.78,0.8,0.84]
Rate_assign= [0.76,0.76,0.78,0.78,0.84]
Rate_greedy = [0.84,0.84,0.86,0.9,0.9]
Rate_gurobi = [0.8,0.86,1.0,1.0,1.0]
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