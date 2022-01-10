---HOW TO USE----

In the numbers.txt file, fill the first line of the file with numbers split by ",".
e.g : 3,5,4,6

The output of the script will be displayed in the console after some debug messages.
To run the script, run from cmd: 

mpiexec -n NR_P py odd-even-radu-v2.py

NR_P -> is the number of processors you want to program to run on. 
!!! The program will work only if the number of numbers introduced in the text file is divisible by NR_P !!!


Running example:
numbers.txt: "5,4,8,9,4,1,4,8,9,1,4,5,12,100,1000,4886,12,18,61,21,17" (21 numbers)
CMD: "mpiexec -n 7 py odd-even-radu-v2.py"
