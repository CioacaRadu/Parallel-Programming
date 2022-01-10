from mpi4py import MPI
import numpy as np
import math
import random
import sys
import csv


comm = MPI.COMM_WORLD
my_id = comm.Get_rank()
p = comm.Get_size()

d = round(math.log2(p))

if my_id == 0: # READ THE VALUES TO BE SORTED BY PROCESSOR 0 

	text_file = open("numbers.txt", "r") # read from text file
	arr = text_file.read().split(',')
	data = np.array(arr) 
	data = data.astype(int) #convert them from char to int
	
	nrp = len(data)/p # this must be an int so data must be divisible with p
	data = np.array_split(data, p) # split them equally for each processor 
	

else:
	data = None

data = comm.scatter(data, root=0) #SCATTER THE VALUES TO ALL THE PROCESSES

#print("Processor ", my_id, " has data(initial):", data)

LOW_data = np.array([]) #each half of the array init
HIGH_data = np.array([]) 
rpivot = -1


mask = 0;

for k in range(d,0,-1): #hypercube step decrement

	HIGH_data = []
	LOW_data = []
	HIGH_data_r = []
	LOW_data_r = []
	
	
	#print("Processor ", my_id, " mask at step", k, " is ", bin(mask))

	n = len(data)
	
	#THE ROOT NODE BROADCASTS THE PIVOT TO ALL THE MEMBERS OF ITS HYPERCUBE
	
	if( my_id & ~mask == 0 and n > 0): #I AM ROOT NODE IN MY HYPERCUBE and I STILL HAVE ELEMENTS
		rpivot = data[int(n/2)] #I CHOOSE THE PIVOT
		message = rpivot
		#print("Processor ", my_id, " chose pivot:", rpivot , "in step", k)
	else:
		message = 1 #DUMMY MESSAGE AND PIVOT
		rpivot = 1
	
	ell = -1 
	id = my_id & ~mask # I SET TO 0 ALL THE BITS THAT DON T MATTER IN THE CURRENT HYPERCUBE
	
	while id != 0: #get the level in the current hypercube
	  id = id // 2
	  ell += 1

	#print("Processor ", my_id, " ell= ", ell, sep='')
	
	if ell != -1: #I AM NOT A ROOT NODE IN MY HYPERCUBE so I HAVE TO RECIEVE
	  neighbor = my_id ^ pow(2,ell)
	  message = comm.recv(source=neighbor)
	  rpivot = message
	  #print("Processor ", my_id, ": received ", message, " from ", neighbor, "at step" , k)

	for i in range(ell+1,d): # SEND TO ALL MY NEIGHBOURS IN CURRENT HYPERCUBE
	  neighbor = my_id ^ pow(2,i)
	  comm.send(message, dest=neighbor)
	
	#BROADCAST OVER
	
	#DIVIDE w.r.t to the pivot that I know
	for i in range(0,n):
		if(data[i] <= rpivot):
			LOW_data = np.append(LOW_data,data[i])
		if(data[i] > rpivot):
			HIGH_data = np.append(HIGH_data,data[i])
	
	#print("Processor ", my_id, " has divided its list in", LOW_data, '--and--', HIGH_data)	
	
	
	if( my_id & pow(2,k-1) != 0 ): # I AM ON THE UPPER LEVEL in the current HYPERCUBE
	
		low_neighbour = my_id ^ pow(2,k-1) #my lower neighbour
		data = HIGH_data #keep only the the numbers higher than the pivot
		comm.send(LOW_data, dest=low_neighbour) #send down the smaller ones
		HIGH_data_r = comm.recv(source=low_neighbour) #get data from the lower value 
		data = np.append(data,HIGH_data_r) #append recieved data
		#print("Processor ", my_id, " exchanges data with", low_neighbour , "in step" , k)	
		
	if( my_id & pow(2,k-1) == 0 ): # I AM ON THE LOWER LEVEL in the current HYPERCUBE
		top_neighbor = my_id ^ pow(2,k-1);
		data = LOW_data
		comm.send(HIGH_data, dest=top_neighbor)
		LOW_data_r = comm.recv(source=top_neighbor)
		data = np.append(data,LOW_data_r)
		#print("Processor ", my_id, " exchanges data with (to top)", top_neighbor, "in step" , k)		
	
	#print("Processor ", my_id, " has data:", data, "at step" , k)
	
	
	mask = mask | pow(2,k-1) #update the mask. The mask shall mask all the top bits that must be ignored at each iteration in the HyperCube e.g for p = 8 => mask = 000 100 110

data = np.sort(data) #sequential sort each node just at the end
  
newData = comm.gather(data,root=0) # GATHER ALL THE DATA BACK

if my_id == 0: #output all the data
   print("FINAL RESULT OUTPUT:")
   a = ' '.join(map(str, newData))
   print(a)
