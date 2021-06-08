import sys
from random import randint
import json
d = 6
M = d*d
N = 140

f = open("Edge36Data.json",'r')
data = json.loads(f.read())

serv_capa = data["serv_capa"] #service_capacity of the edges
serv_occup = data["serv_occup"] # service that is currently occupied at the edges
mem_edge = data["mem_edge"] # Memory capacity of the edges
mem_occup = data["mem_occup"] # Memory occupied at the edges
bandwidth = data["bandwidth"] # bandwidth provided by the edges
bw_const = data["bw_const"] # bandwidth constant
l_cov = data["l_cov"] # The coverage area length of the edges
vel_free = data["vel_free"] # Free velocity of vehicles at the edges
density_jam = data["density_jam"] # density of vehicles during jam at edges
density = data["density"] # normal density of vehicles at edges
vel_at_edge = data["vel_at_edge"] # Velocity of vehicles at edges

serv_app = [] # Servcie requested by the vehicles(Number of VMs)
exec_time = [] # Execution time for the request sent by vehicle 
serv_send_data = [] # Data required to send the service request to the edge by the vehicle
serv_recv_data = [] # Data required to get the service result from the edge to the vehicle 
mem_app = [] # Memory applied by the vehicles

#Calculation of the vehicle data

for i in range(N):
	serv_app.append(randint(1,10))
	exec_time.append(randint(1,10))
	serv_send_data.append(randint(1,15))
	serv_recv_data.append(randint(1,15))
	mem_app.append(randint(60,80))

#Calculation of vehicle paths

x = []
for n in range(N):
	y = randint(0,2)
	edge_list = []
	edge_list.append(y)

	while(y<=d-2 and len(edge_list)<=d-1):
		z = randint(0,1)
		if(z==0):
			y = y+1
			edge_list.append(y)
		elif(z==1):
			edge_list.append(y)

	itr = 0
	flag =0
	a = []
	for k in range(d):
		for j in range(d):
			if(itr <= len(edge_list)-1 and edge_list[itr]==j ):
				a.append(1)
				itr = itr +1
			else:
				a.append(0)
	x.append(a)

#Generation of overlapping data set

min_velocity = min(vel_at_edge) #changed static value to value from list (20.35)
max_velocity = max(vel_at_edge) #changed static value to value from list (30.25)

earliest_arrival = [[0 for itr in range(M)] for y in range(N)]

latest_departure = [[0 for itr in range(M)] for y in range(N)]

#Calculation of Earliest Arrival time

l = 0
for i in x:
	sum_time = 0
	k = 0
	flag = 0
	for j in i:
		if j == 1 and flag == 0:
			sum_time += randint(6,9)/(float(max_velocity)*6)
			flag =1
			earliest_arrival[l][k] = float("{:.2f}".format(sum_time))
			sum_time += l_cov[k]/vel_at_edge[k]
		elif j == 1 and flag != 0:
			sum_time += randint(6,9)/(float(max_velocity)*6)
			earliest_arrival[l][k] = float("{:.2f}".format(sum_time))
			sum_time += l_cov[k]/vel_at_edge[k]
		k = k+1
	l = l+1

#Calculation of Latest departure time

l = 0
for i in x:
	sum_time = 0
	k = 0
	for j in i:
		if j == 1:
			sum_time += randint(6,9)/(float(min_velocity)*6)
			sum_time += l_cov[k]/vel_at_edge[k]
			latest_departure[l][k] = float("{:.2f}".format(sum_time))
		k = k+1
	l = l+1


vehicles_list_at_edge = [[] for i in range(M)]
earliest_arrivals_at_edge = [[] for i in range(M)]
latest_departure_at_edge = [[] for i in range(M)]

for j in range(N):
	for i in range(M):
		if earliest_arrival[j][i] != 0:
			vehicles_list_at_edge[i].append(j)
			earliest_arrivals_at_edge[i].append(earliest_arrival[j][i])
			latest_departure_at_edge[i].append(latest_departure[j][i])

#SOrting vehicles based on arrival time to determine overlapping sets


def bubblesort(i):
    for iter_num in range(len(earliest_arrivals_at_edge[i])-1,0,-1):
        for idx in range(iter_num):
            if earliest_arrivals_at_edge[i][idx]>earliest_arrivals_at_edge[i][idx+1]:
                temp = earliest_arrivals_at_edge[i][idx]
                earliest_arrivals_at_edge[i][idx] = earliest_arrivals_at_edge[i][idx+1]
                earliest_arrivals_at_edge[i][idx+1] = temp
                temp1 = vehicles_list_at_edge[i][idx]
                vehicles_list_at_edge[i][idx] = vehicles_list_at_edge[i][idx+1]
                vehicles_list_at_edge[i][idx+1] = temp1
                temp2 = latest_departure_at_edge[i][idx]
                latest_departure_at_edge[i][idx] = latest_departure_at_edge[i][idx+1]
                latest_departure_at_edge[i][idx+1] = temp2

for i in range(M):
	bubblesort(i)

#Assigning vehicles to make list of common vehicles

list_of_common_vehicles = [[] for i in range(M)]
for i in range(M):
	for j in range(len(latest_departure_at_edge[i])):
		common = []
		k = 0
		for l in earliest_arrivals_at_edge[i]:
			if l<latest_departure_at_edge[i][j] and l >= earliest_arrivals_at_edge[i][j]:
				common.append(vehicles_list_at_edge[i][k])
			k = k+1
		if common not in list_of_common_vehicles[i]:
			list_of_common_vehicles[i].append(common)

#Calculation of vehicle to edge travel time

v2e_trvtime = []
for j in range (N):
	a = []
	for i in range (M):
		a.append(str(earliest_arrival[j][i]))
	v2e_trvtime.append(a)	

#Calculation of overlapping sets

ov_sets = []
for i in range (M):
	for k in list_of_common_vehicles[i]:
		a = []
		for j in range(N):
			if j in k:
				a.append(1)
			else:
				a.append(0)
		ov_sets.append(a)			

#Length of overlapping sets (Given by differnce of two consecutive elements)

len_of_sets = []
SUM = 0
for i in range(M):
	len_of_sets.append(SUM)
	SUM = SUM + len(list_of_common_vehicles[i])
len_of_sets.append(SUM)

#Printing of all the data

print ("serv_capa = ", serv_capa)
print ("serv_occup = ", serv_occup)
print ("mem_edge = ", mem_edge)
print ("mem_occup = ", mem_occup)
print ("bandwidth = ", bandwidth)
print ("bw_const = ", bw_const)
print ("l_cov = ", l_cov)
print ("vel_free = ", vel_free)
print ("density_jam = ", density_jam)
print ("density = ", density)
print ("vel_at_edge = ", vel_at_edge)
print("\n")

print("serv_app = ",serv_app)
print("exec_time = ",exec_time)
print("serv_send_data = ",serv_send_data)
print("serv_recv_data = ",serv_recv_data)
print("mem_app = ",mem_app)
print("\n")

print("x = [")
for i in range(N):
	print(x[i])
print("] \n")

print("v2e_trvtime = [")
for i in range (N):
	print(v2e_trvtime[i])
print("] \n")

print("ov_sets = [")
for i in range(M):
	for k in range(len(list_of_common_vehicles[i])):
		print(ov_sets[i+k])
print("] \n")

print("len_of_sets = ",len_of_sets)


	

