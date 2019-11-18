import numpy as np
from scipy import spatial
import sys, os

sim = sys.argv[1]				#simulation 0-99
neighThres = sys.argv[2]       # minimum number of ST neighbors threshold

#------------------------------------------------
#spatiotemporal domain and resolution
xmin, xmax, ymin, ymax = 323000, 337300, 369100, 387700
xyRes = 100
xyResHalf = xyRes/2.0

#number of points in each dimension
xDim = int((xmax - xmin)/xyRes)  
yDim = int((ymax - ymin)/xyRes)    

print xDim, yDim

# function to convert coordinates to index for inArr
#--------------------------------------------------------------------------------------
def coordToIndex(x,y):

    xIndex1 = int((x-xmin) / xyRes)
    if x%xyRes < xyResHalf:
        xIndex2 = xIndex1
    else:
        xIndex2 = xIndex1 + 1

    yIndex1 = int((y-ymin) / xyRes)
    if y%xyRes < xyResHalf:
        yIndex2 = yIndex1
    else:
        yIndex2 = yIndex1 + 1

    return [xIndex2, yIndex2]

#------------------------------------------------
#initialize regular grid: 3d grid of tuples: (x, y, nCount, pCount, ds) |nCount: how many disease cases within pixel, pCount: how much population within pixel
fullGridArr = np.zeros((xDim, yDim, 5))

#populate the grid
xG = xmin
while xG < xmax:
    yG = ymin
    while yG < ymax:
        
        #create index
        gIndex = coordToIndex(xG, yG)
        xIndex, yIndex = gIndex[0], gIndex[1]

        #assign coordinates
        fullGridArr[xIndex][yIndex][0] = xG
        fullGridArr[xIndex][yIndex][1] = yG
        
        yG += xyRes
    xG += xyRes

#------------------------------------------------
#read population files, add them to one array [x, y, flag]	|flag: for avoiding double count (how many population  within voxel?)

i = 0
popList = []
while i <  334:
    popFile = open('outputs/pop_model/sim_' + sim + os.sep + 'barrio_' + str(i) + '.txt', 'r')
    for record in popFile:
        x = record.split(',')[0]
        y = record.split(',')[1]
        popList.append([float(x),float(y), 0])
    popFile.close()
    i += 1

popArr = np.array(popList)

#------------------------------------------------
## read file containing case coordinates and bandwidths [ID, x, y, hs]
disFile = open('outputs/S_IB_1/bandwidths_' + neighThres + '.txt', 'r')
disList = []
for record in disFile:
    #print record
    line = record.split(',')
    disList.append([float(line[0]),float(line[1]),float(line[2]),float(line[3])])
disFile.close()
numPts = len(disList)

#------------------------------------------------

outDir = 'outputs/S_IB_2' + os.sep + 'sim_' + sim
# make output directory
if not os.path.exists(outDir):
    os.makedirs(outDir)

# open output File
outFile = open(outDir + os.sep + 'peopleTime_' + neighThres + '.txt','w')

#------------------------------------------------

#build kd tree
sTree = spatial.cKDTree(popArr[:,:2])

count = 0
#for each disease case, compute populaiton inside kernel
for i in disList:

    sCoord = i[1:3]

    # query the tree: return all population points within bandwidth
    sNeigh = sTree.query_ball_point(sCoord, i[3])

    p = 0      #how many population inside kernel? population adjustment.
    # for each population neighbor, calculate length of stay within kernel
    for j in sNeigh:
        p += 1

        #add pop within voxel
        gIndex = coordToIndex(popArr[j,0],popArr[j,1])      
        xIndex, yIndex = gIndex[0], gIndex[1]

        if xIndex >= 0 and xIndex < xDim and yIndex >= 0 and yIndex < yDim and popArr[j,2]==0:
            fullGridArr[xIndex,yIndex,3] += 1
            popArr[j,2] = 1 

    #[ID, x, y, hs, p] |p: population
    outFile.write(str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + ',' + str(i[3]) + ',' + str(p) + '\n')

    count += 1

outFile.close()

np.save(outDir + os.sep + 'fullGrid_' + neighThres,fullGridArr)
