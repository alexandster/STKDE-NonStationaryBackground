#ST_IB_4.py, by Alexander Hohl
#This script creates an index file that delineates clusters based on risk threshold and computes odds ratios.

import numpy as np
from scipy import spatial
import math, sys, os

sim = sys.argv[1]
neighThres = sys.argv[2]       # minimum number of ST neighbors threshold

#percentile thresholds of disease risk
percThresList = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 99.9, 99.99] 

#------------------------------------------------
#points_obs spatiotemporal envelope (domain)
xmin, xmax, ymin, ymax, tmin, tmax = 322896.6389, 337268.7369, 368748.6975, 387824.4062, 3, 658

# spatial and temporal resolution of output grid
xyRes, tRes = 100, 1
xyResHalf = xyRes/2.0

#------------------------------------------------

#number of points in each dimension
xDim = int((xmax - xmin)/xyRes)  
yDim = int((ymax - ymin)/xyRes)  
tDim = int((tmax - tmin)/tRes)  

indir = 'outputs/ST_IB_3' + os.sep + 'sim_' + sim
outDir = 'outputs/ST_IB_4' + os.sep + 'sim_' + sim

#load regular grid: 2d grid of tuples: (x, y, t, nCount, pCount, k)
inArr = np.loadtxt(indir + os.sep + 'density_' + neighThres + '.txt',delimiter=',')

#compute total number of cases and controls
casTotal = sum(inArr[:,3])	#cases
conTotal = sum(inArr[:,4])	#controls

#discard zero density voxels
nonZeroIndex = np.where(inArr[:,5] > 0.0)

outFile = open(outDir + os.sep + "odds_ratio_" + neighThres + ".txt", "w")

for percThres in percThresList:
    print(percThres)

    #compute threshold (percentile)
    thres = np.percentile(inArr[nonZeroIndex][:,5], percThres)

    #select voxels with densities above threshold 
    aboveThresIndex = np.where(inArr[:,5] > thres)

    np.save(outDir + os.sep + "clustIndex_" + str(neighThres) + "_" + str(percThres), aboveThresIndex)

    #compute number of cases and controls inside cluster
    casClust = sum(inArr[aboveThresIndex][:,3])
    conClust = sum(inArr[aboveThresIndex][:,4])

    casNonClust = casTotal-casClust
    conNonClust = conTotal-conClust

    clustRatio = casClust/conClust
    nonClustRatio = casNonClust/conNonClust

    oddsRatio = clustRatio/nonClustRatio

    outFile.write(str(percThres) + "," + str(oddsRatio) + "\n") 

outFile.close()
