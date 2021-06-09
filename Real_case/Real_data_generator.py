import sys
import csv  
import xml.etree.ElementTree as ET 
from random import randint
import json

#To get list of vehicles that stisfy the minimum edge criteria (vehicle passes through atleast M/10 edges)
list_of_vehicles = []
edge_list = ['-32336','--30528#27','--32468#4','--31476','--31818#22','--31794#2','--32266','--30528#25','-32582','-32798','-32860','-31954','-30706#0','--31262#0','--31228','--32638#5','--32280#2','--31648#3','-31496#1','--31860#1','--30694#6','-31910#6','--30620','--31818#16','-32456','--32004','-30668#5','-31834#1','-30668#7','--32468#7','-31614','-31622#8','-30994#2','--31818#17','-31004#1','-30668#8','-30706#2','-31622#3','-32764#2','-31622#9','-30772#3','-31876#1','-31622#7','-31680#1','--32910','-31052','-31578#1','--30528#33','-32770#7','--31818#14','--30528#34','-31622#5','--31792','--31744#4','-30384#3','-30962#2','-32400#2','--30890#3','-31952#9','-31910#3','-31622#10','--31952#8','--30684#2','-32004','-31876#3','--32644#2','--32184','--32224#1','-31628','-31910#7']
#Pre defined list of road segments assumed to have an edge server placed in them. This list of edge segments was manually chosen form the real data set
M = 70 #Number of edges 
N = 280 #Number of Vehicles
print("M = ",M)
print("N = ",N)
print("\n")

#Calculation of the total list of vehcles that pass through the edges chosen from edge list

for j in range(M):
    i = edge_list[j]
    tree = ET.parse('local.actuated.0.rou.xml')
    root = tree.getroot()
    edges_set = set()
    for vehicle in root:
	    for route in vehicle:
		    for str in route.get('edges').split():
			    if str == i:
				    list_of_vehicles.append(vehicle.get('id'))     

vehicle_set = set() #List converted to set to remove duplicates
for vehicle in list_of_vehicles:
	vehicle_set.add(vehicle)

for i in range(int(M/10)): #Remove instances of vehicles from the list so as to make sure there will only exist vehicles that satisfy passing through M/10 criteria
    for vehicle in vehicle_set:
	    if vehicle in list_of_vehicles:
		    list_of_vehicles.remove(vehicle)

fine_set = set() #Final set of vehicles
for vehicle in list_of_vehicles:
	fine_set.add(vehicle)

#To calculate length of road segments

tree1 = ET.parse('lust.net.xml')
root1 = tree1.getroot()

Leng = {}
for edge in root1:
	Leng[edge.get('id')] = float(edge.find('lane').get('length'))

#Calculate distance Matrix
#First create a dictionary with vehicle id as key and route of road segments as value
tree2 = ET.parse('local.actuated.0.rou.xml')
root2 = tree2.getroot()

Dict = {}
for vehicle in root2:
	for id1 in fine_set:
		if id1 == vehicle.get('id'):
			Dict[id1] = vehicle.find('route').get('edges')

# Distance matrix generation

h = len(fine_set)
distance_mat = [[float(-1) for x in range(M)] for y in range(h)]

k=0
for ide in fine_set:
	for strng in Dict[ide].split():
		for j in range(M):
			if strng==edge_list[j]:
				l =0
				for s in Dict[ide].split():
					if s!=strng:
						l = l + Leng[s]
					else:
						break
				distance_mat[k][j] = float("{:.2f}".format(l))
	k = k+1		

#Vehicle Path matrix calculation

x = [[0 for z in range(M)] for y in range(N)]
k=0
for n in range(N):
	i = distance_mat[n]
	l=0
	for j in i:
		if j!=-1.0:
			x[k][l] = 1
		l=l+1
	k=k+1

#Loading of Edge data

f = open("Edge70Data.json",'r')
data = json.loads(f.read())
f.close()


l_cov = data["l_cov"]
vel_at_edge = data["vel_at_edge"] 

min_velocity = min(vel_at_edge) #changed static value to value from list (20.35)
max_velocity = max(vel_at_edge) #changed static value to value from list (30.25)


earliest_arrival = [[0 for itr in range(M)] for y in range(N)]

latest_departure = [[0 for itr in range(M)] for y in range(N)]

l = 0

#Calculation of earliest arrival and latest departure

for i in x:
	sum_time = 0
	k = 0
	for j in i:
		if j == 1:
			sum_time = (distance_mat[l][k]*3600)/float(max_velocity*1.60934*1000)
			earliest_arrival[l][k] = float("{:.2f}".format(sum_time))
		k = k+1
	l = l+1

l = 0

for i in x:
	sum_time = 0
	k = 0
	for j in i:
		if j == 1:
			sum_time = (distance_mat[l][k]*3600)/(float(min_velocity)*1.60934*1000)
			sum_time += l_cov[k]*1.6*3600/(float(16.5))
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

#Sorting vehicles based on the arrival time at an edge

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

#Finding lists of common vehicles  

list_of_common_vehicles = [[] for i in range(M)]
for i in range(M):
	for j in range(len(latest_departure_at_edge[i])):
		common = []
		k = 0
		for l in earliest_arrivals_at_edge[i]:
			if l<latest_departure_at_edge[i][j] and l >= earliest_arrivals_at_edge[i][j]:
				common.append(vehicles_list_at_edge[i][k])
			k = k+1
		list_of_common_vehicles[i].append(common)

serv_app = []
exec_time = []
serv_send_data = []
serv_recv_data = []
mem_app = []

for i in range(N):
	serv_app.append(randint(1,10))
	exec_time.append(randint(1,10))
	serv_send_data.append(randint(1,15))
	serv_recv_data.append(randint(1,15))
	mem_app.append(randint(40,60))


v2e_trvtime = []
for j in range (N):
	a = []
	for i in range (M):
		a.append(earliest_arrival[j][i])
	v2e_trvtime.append(a)	

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

len_of_sets = []
SUM = 0
for i in range(M):
	len_of_sets.append(SUM)
	SUM = SUM + len(list_of_common_vehicles[i])
len_of_sets.append(SUM)

print ("l_cov = ", l_cov)
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

