from mpi4py import MPI
import numpy as np
import math
import random
import sys
import csv


comm = MPI.COMM_WORLD
my_id = comm.Get_rank()
p = comm.Get_size()



if my_id == 0: # READ THE VALUES TO BE SORTED BY PROCESSOR 0 


	#arr = sys.argv[1].split(',') #read from console
	
	text_file = open("numbers.txt", "r") # read from text file
	arr = text_file.read().split(',')
	data = np.array(arr) 
	data = data.astype(int) #convert them from char to int
	
	nrp = len(data)/p # this must be an int so data must be divisible with p
	data = np.array_split(data, p) # split them equally for each processor 
	

else:
	data = None

data = comm.scatter(data, root=0) #SCATTER THE VALUES TO ALL THE PROCESSES

#print("Processor ", my_id, " has data:", data)

left_neighbor = (my_id-1) % p
right_neighbor = (my_id+1) % p

l = len(data) 

for i in range(1,l*p):

	data = np.sort(data) # local sequential locally sort
	#print("Processor ", my_id, " has data (sorted locally):", data)

	#EVEN-ODD PHASE
	if(my_id%2 == 0 and my_id != p-1): #I AM EVEN and I AM NOT THE LAST (chain communication)
		comm.send(data, dest=right_neighbor)
		datar = comm.recv(source=right_neighbor)
		if(datar[0] < data[l-1]): #COMPARE VALUES AND EXCHANGE THE EXTREMITIES
			data[l-1] = datar[0]
			#print("Processor ", my_id, " has exchanged data:", datar[0], "from",right_neighbor)
			
	if(my_id%2 == 1 and my_id != 0):# I AM ODD and I AM NOT THE FIRST
		datar = comm.recv(source=left_neighbor)
		comm.send(data, dest=left_neighbor) 
		if(datar[l-1] > data[0]): #COMPARE VALUES AND EXCHANGE THE EXTREMITIES
			data[0] = datar[l-1];
			#print("Processor ", my_id, " has exchanged data:", datar[l-1], "from",left_neighbor)
		
	#print("Processor ", my_id, " has data:", data)
	#ODD-EVEN PHASE
	if(my_id%2 == 0 and my_id != 0): #I AM EVEN
		comm.send(data, dest=left_neighbor)
		datar = comm.recv(source=left_neighbor)
		if(datar[l-1] > data[0]): #COMPARE VALUES AND EXCHANGE THE EXTREMITIES
			data[0] = datar[l-1];
			#print("Processor ", my_id, " has exchanged data:", datar, "from",right_neighbor)

	if(my_id%2 == 1 and my_id != p-1): #I AM ODD and not the last
		comm.send(data, dest=right_neighbor)
		datar = comm.recv(source=right_neighbor)
		if(datar[0] < data[l-1]): #COMPARE VALUES AND EXCHANGE THE EXTREMITIES
			data[l-1] = datar[0];
			#print("Processor ", my_id, " has exchanged data:", datar, "from",left_neighbor)

	#print("Processor ", my_id, " has data:", data)

		
newData = comm.gather(data,root=0) # GATHER ALL THE DATA BACK

if my_id == 0: #output all the data
   print("FINAL RESULT OUTPUT:")
   a = ' '.join(map(str, newData))
   print(a)
