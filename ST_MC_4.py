#ST_IB_MC_4.py, by Alexander Hohl
#This script

import numpy as np
from scipy import spatial
import math, sys, os

sim = sys.argv[1]
neighThres = sys.argv[2]       # minimum number of ST neighbors threshold

#spatiotemporal domain
xmin, xmax, ymin, ymax, tmin, tmax = 323000, 337300, 369100, 387700, 14, 730

#spatiotemporal resolution
xyRes, tRes = 100, 1
xyResHalf = xyRes/2.0

#number of points in each dimension
xDim = int((xmax - xmin)/xyRes)  
yDim = int((ymax - ymin)/xyRes)  
tDim = int((tmax - tmin)/tRes)  

indir = "outputs/ST_IB_MC_3" + os.sep + "sim_" + sim
outDir = "outputs/ST_IB_MC_4" + os.sep + "sim_" + sim

#load regular grid: 2d grid of tuples: (x, y, t, nCount, pCount, k)
inArr = np.loadtxt(indir + os.sep + "density_" + neighThres + ".txt",delimiter=",")

#compute total number of cases and controls
casTotal = sum(inArr[:,3])	#cases
conTotal = sum(inArr[:,4])	#controls

#discard zero density voxels
nonZeroIndex = np.where(inArr[:,5] > 0.0)

outFile = open(outDir + os.sep + "odds_ratio_" + neighThres + ".txt", "w")

#percentile thresholds of disease risk
percThresList = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 99.9, 99.99] 

for percThres in percThresList:

    #compute threshold (percentile)
    thres = np.percentile(inArr[nonZeroIndex][:,5], percThres)

    #select voxels with densities above threshold 
    aboveThresIndex = np.where(inArr[:,5] > thres)

    #compute number of cases and controls inside cluster
    casClust = sum(inArr[aboveThresIndex][:,3])
    conClust = sum(inArr[aboveThresIndex][:,4])

    casNonClust = casTotal-casClust
    conNonClust = conTotal-conClust

    clustRatio = casClust/conClust
    nonClustRatio = casNonClust/conNonClust

    oddsRatio = clustRatio/nonClustRatio

    outFile.write(str(oddsRatio) + "\n") 



outFile.close()



