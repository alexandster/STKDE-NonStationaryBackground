#cluster_significance.py
#computes the significance of a cluster

import numpy as np
from scipy import spatial
import math, sys, os

#compute p value of observed odds ratio
percentile = 95       # percentile threshold parameter
neighThres = 40       # minsup: minimum number of ST neighbors threshold

#since we determined that the uncertainty that stems from population simulatino is negliglible, I picked simulation run 0 as the observed population.
#this allowed me to simulate the cases for significance testing.

#load index array: list of index numbers that denote voxles part of cluster in indatArr observed -- THIS IS THE OBSERVED CLUSTER (95 percentile)
indexArr = np.load('outputs/ST_IB_4/clustIndex_' + str(neighthres) + '_' + str(percentile) + ".npy")

#load observed odds ratio (at 95 percentile)
obsOddsRatio = np.loadtxt('outputs/ST_IB_4/odds_ratio_" + str(neighThres) + ".txt")[5][-1]

#open output file
outDir = 'outputs/cluster'
if not os.path.exists(outDir):
    os.makedirs(outDir)

outFile = open(outDir + 'cluster_significance_' + str(neighThres) + "_" + str(percentile) + ".txt", "w")

outFile.write('Observed odds ratio: ' + str(obsOddsRatio) + "\n")

#odds ratios from simulated clusters
simOddsRatio = 0
i = 0
while i <= 99:

    #load regular grid: 2d grid of tuples: (x, y, t, nCount, pCount, k) --- simulated density
    indatArr = np.loadtxt('outputs/ST_MC_3/sim_' + str(i) + os.sep + "density_" + str(neighThres) + ".txt", delimiter=",")

    #compute total number of cases and controls
    casTotal = sum(indatArr[:,3])	#cases
    conTotal = sum(indatArr[:,4])	#controls

    #compute number of cases and controls inside cluster
    casClust = sum(indatArr[indexArr,3][0])
    conClust = sum(indatArr[indexArr,4][0])

    #compute number of cases and controls outside cluster
    casNonClust = casTotal-casClust
    conNonClust = conTotal-conClust

    clustRatio = casClust/conClust
    nonClustRatio = casNonClust/conNonClust
    oddsRatio = clustRatio/nonClustRatio

    outFile.write('Odds ratio simulation ' + str(i)) + ' :' + str(oddsRatio) + "\n")

    i += 1

outFile.close()
