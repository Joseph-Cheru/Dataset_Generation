import sys
from random import randint, uniform
import json

M = 36

serv_capa = []
serv_occup = []
mem_edge = []
mem_occup = []
bandwidth = []
bw_const = []
l_cov = []
vel_free = []
density_jam = []
density = []
vel_at_edge = []

for i in range(M):
	serv_capa.append(randint(24,40)) 
	serv_occup.append(randint(1,3))
	mem_edge.append(randint(400,500))
	mem_occup.append(randint(0,150))
	bandwidth.append(randint(8,15))
	bw_const.append(1)
	l_cov.append(int(uniform(0.6,1.6)*10)/10.0)
	vel_free.append(randint(50,70))
	density_jam.append(randint(50,65))
	density.append(35)
	vel_at_edge.append(int(vel_free[i]*(1 - float(density[i])/float(density_jam[i]))*100)/100.0)

# print ("serv_capa = ", serv_capa)
# print ("serv_occup = ", serv_occup)
# print ("mem_edge = ", mem_edge)
# print ("mem_occup = ", mem_occup)
# print ("bandwidth = ", bandwidth)
# print ("bw_const = ", bw_const)
# print ("l_cov = ", l_cov)
# print ("vel_free = ", vel_free)
# print ("density_jam = ", density_jam)
# print ("density = ", density)
# print ("vel_at_edge = ", vel_at_edge)


data = {"serv_capa": serv_capa,
	"serv_occup": serv_occup,
	"mem_edge": mem_edge,
	"mem_occup": mem_occup,
	"bandwidth": bandwidth,
	"bw_const": bw_const,
	"l_cov": l_cov,
	"vel_free": vel_free,
	"density_jam": density_jam,
	"density": density,
	"vel_at_edge": vel_at_edge }


with open('Edge36Data.json', 'w') as f:
    json.dump(data, f)	
