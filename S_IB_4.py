import numpy as np
from scipy import spatial
import math, sys, os

sim = sys.argv[1]
neighThres = sys.argv[2]       # minimum number of ST neighbors threshold

#spatiotemporal domain
xmin, xmax, ymin, ymax = 323000, 337300, 369100, 387700

#spatiotemporal resolution
xyRes = 100
xyResHalf = xyRes/2.0

#number of points in each dimension
xDim = int((xmax - xmin)/xyRes)  
yDim = int((ymax - ymin)/xyRes)    

indir = 'outputs/S_IB_3' + os.sep + 'sim_' + sim
outDir = 'outputs/S_IB_4' + os.sep + 'sim_' + sim

# output folder
if not os.path.exists(outDir):
    os.makedirs(outDir)

#load regular grid: 2d grid of tuples: (x, y, nCount, pCount, d)
inArr = np.loadtxt(indir + os.sep + 'density_' + neighThres + '.txt',delimiter=',')

#compute total number of cases and controls
casTotal = sum(inArr[:,2])	#cases
conTotal = sum(inArr[:,3])	#controls

#discard zero density voxels
nonZeroIndex = np.where(inArr[:,4] > 0.0)

outFile = open(outDir + os.sep + 'odds_ratio_' + neighThres + '.txt', 'w')

#percentile thresholds of disease risk
percThresList = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 99.9, 99.99] 

for percThres in percThresList:

    #compute threshold (percentile)
    thres = np.percentile(inArr[nonZeroIndex][:,4], percThres)

    #select voxels with densities above threshold 
    aboveThresIndex = np.where(inArr[:,4] > thres)

    #compute number of cases and controls inside cluster
    casClust = sum(inArr[aboveThresIndex][:,2])
    conClust = sum(inArr[aboveThresIndex][:,3])

    casNonClust = casTotal-casClust
    conNonClust = conTotal-conClust

    clustRatio = casClust/conClust
    nonClustRatio = casNonClust/conNonClust

    oddsRatio = clustRatio/nonClustRatio

    outFile.write(str(oddsRatio) + '\n') 

outFile.close()

