---HOW TO USE----

In the numbers.txt file, fill the first line of the file with numbers split by ",".
e.g : 3,5,4,6

The output of the script will be displayed in the console after some debug messages.
To run the script, run from cmd: 

mpiexec -n NR_P py hyperquick-radu.py

NR_P -> is the number of processors you want to program to run on. 
*The program will work only if the number of numbers introduced in the text file is divisible by NR_P !!!
*NR_P must be a power of 2, otherwise it will not work !


Running example:
numbers.txt: "5,4,1,2,3,7,8,4,110,1000,1534,123,78,14,15,18" (16 numbers)

CMD: "mpiexec -n 8 py hyperquick-radu.py"
CMD: "mpiexec -n 2 py hyperquick-radu.py"
CMD: "mpiexec -n 4 py hyperquick-radu.py"