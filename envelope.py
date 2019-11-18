import os, sys, glob

mdir = "outputs/ST_IB_3/sim_"

#initiate min and max array of [x,y,z,0] tuples
baseFile = open(mdir + "0" + os.sep +"density_25.txt", "r")
outArrMin = []	#lower envelope
outArrMax = []	#upper envelope
for i in baseFile:
    x = float(i.split(",")[0])
    y = float(i.split(",")[1])
    z = float(i.split(",")[2])
    outArrMin.append([x,y,z,99999.0])	#array of dim(3242835,4)
    outArrMax.append([x,y,z,0.0])	#array of dim(3242835,4)

baseFile.close()

#for all perturbed datasets
i = 1
while i < 2:

    #for each voxel in perturbed dataset
    inFile = open(mdir + str(i) + os.sep + "density_25.txt", "r")
    for counter, value in enumerate(inFile):
        x = float(value.split(",")[0])
        y = float(value.split(",")[1])
        z = float(value.split(",")[2])
        d = float(value.split(",")[3])

        #if voxel coordinates match (outArrMin vs. current perturbed dataset) 
        if x == outArrMin[counter][0] and y == outArrMin[counter][1] and z == outArrMin[counter][2]:
            #if current perturbed density smaller than outArrMin density 
            if d < outArrMin[counter][3]:
                outArrMin[counter][3] = d
        else: 
            print("Coordinate mismatch Min", i, counter, x, y, z, outArrMin[counter][0], outArrMin[counter][1], outArrMin[counter][2])
            break 
        #if voxel coordinates match (outArrMax vs. current perturbed dataset)
        if x == outArrMax[counter][0] and y == outArrMax[counter][1] and z == outArrMax[counter][2]:
            #if current perturbed density greater than outArrMax density
            if d > outArrMax[counter][3]:
                outArrMax[counter][3] = d
        else: 
            print("Coordinate mismatch Max", i, counter, x, y, z, outArrMax[counter][0], outArrMax[counter][1], outArrMax[counter][2])
            break
    inFile.close() 
    i += 1   

# output folder
outDir = 'outputs/envelope'
if not os.path.exists(outDir):
    os.makedirs(outDir)

#write arrays to textfiles
outFileMin = open(outDir + os.sep + 'envelope_lower.txt', 'w')
outFileMax = open(outDir + os.sep + 'envelope_upper.txt', 'w')

for i,j in zip(outArrMin, outArrMax):
    outFileMin.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + "," + str(i[3]) + "\n")
    outFileMax.write(str(j[0]) + "," + str(j[1]) + "," + str(j[2]) + "," + str(j[3]) + "\n")
  
outFileMin.close()
outFileMax.close()
