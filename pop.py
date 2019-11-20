#pop.py
#This script creates the population columns, additing the temporal components to the x, y coordinates of the random points created by random_points.r

#--------------------------------------------------------------
#workflow:
#for each fc in GDB:
#   create initial population
#   for each timestep:
#       determine pop change
#       if pop increase:
#           add pop increase (floor, probability decimal part)
#       else:
#           remove pop (floor , probability decimal part)
#--------------------------------------------------------------

import sys, os, random, numpy as np

#simulation number
sim = sys.argv[1]

# create output directory
outDir = "outputs/pop_model/sim_" + sim
if not os.path.exists(outDir):
    os.makedirs(outDir)

i = 0
#iterate through barrios, create initial population, compute rate of pop change for each year, break down to days,
#add or remove pop for each day 

#for each barrio
while i < 334:
    
    #read file of random points
    pointFile = open("outputs/barrios_rand/sim_" + sim + os.sep + "barrio_" + str(i) + ".txt", 'r')
    pointFile.readline()
    pointArr = []
    for j in pointFile:
        line = j.split(" ")
        pointArr.append([float(line[1]),float(line[2]), 0, 730])

    #read population count file
    popFile = open("outputs/barrios_rand/sim_" + sim + os.sep + "barrio_ypop_" + str(i) + ".txt", 'r')
    popFile.readline()
    popArr = []
    for k in popFile:
        line = k.split(" ")
        popArr.append(float(line[1].strip()))
    
    #initial population 2010: create random points within polygon
    initIndex = int(round(popArr[0]))
    initialTable = pointArr[:initIndex]

    #compute daily rate of pop change for each year
    popChange1011 = (popArr[2]-popArr[1])/365
    popChange1112 = (popArr[3]-popArr[2])/365

    #open output file
    outFile = open(outDir + os.sep + "barrio_" + str(i) + ".txt", "w")

    #for each year   
    for j1, j2 in enumerate([popChange1011,popChange1112]):
                
        #separate integer part from decimal part 
        intPart, decPart = divmod(j2, 1)

        fr = j1 * 365
        to = fr + 365

        #if population increase
        if j2 > 0:
            k = fr

            #for each day
            while k < to:

                #pick random row of remaining records               
                #add pop increase (floor, probability decimal part)
                if intPart != 0:
                    x = 0
                    while x < int(intPart):

                        #random row
                        randIndex = random.randint(initIndex, len(pointArr)-1)
                        addRow = pointArr[randIndex]
                        initialTable.append([addRow[0],addRow[1],k,730])
                        x += 1

                if decPart > random.random():
                        randIndex = random.randint(initIndex, len(pointArr)-1)
                        addRow = pointArr[randIndex]
                        initialTable.append([addRow[0],addRow[1],k,730])

                k += 1
        #if population decrease
        else:

            n = fr

            #for each day
            while n < to:

                #remove pop decrease (floor, probability decimal part)
                if intPart != 0:
                    o = 0
                    while o < abs(intPart):
                        initialTable[random.randint(0,len(initialTable)-1)][-1] = n + 1
                        o += 1
                if decPart > random.random():
                    initialTable[random.randint(0,len(initialTable)-1)][-1] = n + 1
                n += 1
                
                
    for m in initialTable:
        outFile.write(str(m[0]) + "," + str(m[1]) + "," + str(m[2]) + "," + str(m[3]) + "\n") 
    outFile.close()    
            
    i += 1    
