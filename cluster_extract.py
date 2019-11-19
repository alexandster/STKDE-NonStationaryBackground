#cluster_extract.py
#This script uses the index file (from ST_IB_4.py) to extract clusters from regular grid file.

import numpy as np
import math, sys, os

#extract a cluster: x, y, t tuples that denote cluster voxels.

sim = 0              #simulation number. here, the simulation number refers to population simulation. As the uncertainty from population simulation is negliglible, we can just pick one dataset
neighThres = 45       # minimum number of ST neighbors threshold
percentile = 95			#percentile threshold for delineating cluster

#load regular grid: 2d grid of tuples: (x, y, t, nCount, pCount, k) --- observed density
indatArr = np.loadtxt('outputs/ST_IB_3/sim_' + str(sim) + os.sep + 'density_' + str(neighThres) + '.txt',delimiter=',')

#load index array: list of index numbers that denote voxles part of cluster in indatArr observed -- THIS IS THE OBERSVED CLUSTER
inDir = 'outputs/ST_IB_4' + os.sep + 'sim_' + str(sim)
indexArr = np.load(inDir + os.sep + 'clustIndex_' + str(neighThres) + '_' + str(percentile) + '.npy')

#create array that denotes cluster
outArr = indatArr[indexArr]

# output folder
outDir = 'outputs/cluster'
if not os.path.exists(outDir):
    os.makedirs(outDir)

np.savetxt(outDir + os.sep + 'clust_' + str(neighThres)+ '_' + str(percentile) + '.txt', outArr[0][:,0:3])
