#!/usr/bin/env python3
#Michael Pare 861061582
import sys
import math
import time

sys.setrecursionlimit(1000000) # 10000 is an example, try with different values
#point class
class point:
    #init function to create object
    def __init__(self, x, y):
        self.x = x
        self.y = y
    #allows uses of the print function
    def __str__(self):
        return "(%s,%s)\n"%(self.x, self.y) 

#helper functions ====================================================================
#function to calculate distance between two points using given formula
def calc_distance(p1, p2):
    '''Calculates distance between 2 points'''
    return math.sqrt(((p1.x - p2.x)**2) + ((p1.y - p2.y)**2))


def brute_force(neighbors):
    if len(neighbors) == 1:
        return sys.maxsize
    min = calc_distance(neighbors[0], neighbors[1])
    for i in range(len(neighbors)):
        for j in range(1, len(neighbors)):
            temp = calc_distance(neighbors[i], neighbors[j])
            if temp < min and temp != 0:
                min = temp   
    return min

def find_mid(a, b):
    if a > b:
        return b + (a - b)/2
    elif a == b:
        return a
    else:
        return a + (b - a)/2

def rec_calc(arr):
    if len(arr) <= 3:
        return brute_force(arr)
    else:
        return min( rec_calc(arr[1:]), rec_calc(arr[0:2]) )
#=====================================================================================
#load inputs from file into point objects    

print('{0:=^50s}'.format('='))


try:
    file = open(sys.argv[1],"r")
    print("input file succesfully opened!")
except IOError:
    print("Could not open file!")
    print('{0:=^50s}'.format('='))
    exit()

neighbors = list()

while True:
    temp = file.readline()
    if(temp == ''):
        break
    else:
        tempx, tempy = temp.split()
        tempx = float(tempx)
        tempy = float(tempy)
        new_neighbor = point(tempx, tempy)
        neighbors.append(new_neighbor)
        

file.close()


#Divide and Conquer method=======================================================================================

print("Divide and Conquer Method:")
start2 = time.time() #used to record how long it takes to find nearest neighbors using brute force algorithm

#sort list of points in ascending order by x value
neighbors_dc = sorted(neighbors, key=lambda neighbor: neighbor.x)
mid_list = int(len(neighbors)/2)

left_list = neighbors_dc[mid_list:]
right_list = neighbors_dc[:mid_list]

left_min = rec_calc(left_list)
right_min = rec_calc(right_list)


if left_min == 0:
    d = right_min
elif right_min == 0:
    d = left_min
else:
    d = min(left_min, right_min)

left_bound = neighbors_dc[mid_list-1].x - d
right_bound = neighbors_dc[mid_list-1].x + d

cnt_lower = 0
cnt_upper = 0
for  x in range (len(neighbors_dc)):
    if neighbors_dc[x].x < left_bound:
        cnt_lower += 1

for  x in range (len(neighbors_dc)):
    if neighbors[x].x > right_bound:
        cnt_upper += 1

if cnt_upper > 0:
    ycheck = neighbors_dc[cnt_lower:-cnt_upper]
else: 
    ycheck = neighbors_dc[cnt_lower:]


#sort by y here
ycheck = sorted(ycheck, key=lambda neighbor: neighbor.y)

min_bounded = rec_calc(ycheck)

if left_min < right_min and left_min < min_bounded:
    final_min = left_min
elif right_min < left_min and right_min < min_bounded:
    final_min =right_min
else:
    final_min = min_bounded
    
if left_min == 0 and right_min == 0:
    final_min = min_bounded
    
print(("nearest neighbors distance: %f")%(final_min))
print(("Time taken: %f")%(time.time() - start2))



#Brute Force method ===============================================================================================
print('{0:=^50s}'.format('='))
print("Brute Force Method:")
start1 = time.time() #used to record how long it takes to find nearest neighbors using brute force algorithm

nearest = brute_force(neighbors)

    
print(("nearest neighbors distance: %f")%(nearest))
print(("Time taken: %f")%(time.time() - start1))
print('{0:=^50s}'.format('='))
print("Done!\nWriting results to text file...")
output = open("input_distance.txt" ,'w')
output.write(str(final_min))
output.write('\n')

print('{0:=^50s}'.format('='))



 
