#odds_ratio_surface.py
# computes differences in odds ratios between ST_IB and S_IB. calculates differences within minsup threshold and precentile threshold parameter space.

import numpy as np
import math, sys, os

#input directories
inDir3D = 'outputs/ST_IB_4/sim_0/odds_ratio_'
inDir2D = 'outputs/S_IB_4/sim_0/odds_ratio_'

#parameter space
thresList = [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 99.9, 99.99]
popSupList = [5, 10, 15, 20, 25, 30, 35, 40, 45]

#initialize array
curArr = np.zeros((len(popSupList)*len(thresList), 3), dtype=float)

#for each minsup threshold value
count = 0
for i,j in enumerate(popSupList):
    print(j)
    inArr3D = np.loadtxt(inDir3D + str(j) + ".txt", delimiter=',', usecols=-1)
    inArr2D = np.loadtxt(inDir2D + str(j) + ".txt", delimiter=',', usecols=-1)
    inArrStack = np.stack((inArr3D,inArr2D))
    #for each percentile threshold value
    for k,l in enumerate(zip(list(inArr3D),list(inArr2D))):
        curArr[count][0] = i
        curArr[count][1] = k
        curArr[count][2] = l[0]-l[1]        #difference between odds ratios
        count += 1

# output folder
outDir = 'outputs/odds_ratios'
if not os.path.exists(outDir):
    os.makedirs(outDir)

np.savetxt(outDir + os.sep + 'odds_ratio_diff_surface.txt', curArr,delimiter=",")
