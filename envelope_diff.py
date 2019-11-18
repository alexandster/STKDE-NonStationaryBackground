import os, sys, glob
import numpy as np

wDir = 'outputs/envelope'
#open envelope files
envLo = np.loadtxt(wDir + os.sep + 'envelope_lower.txt', delimiter=",")
envUp = np.loadtxt(wDir + os.sep + 'envelope_upper.txt', delimiter=",")

print("Arrays read")

envDiff = envUp[:,3] - envLo[:,3]

print("Difference calculated")

finalArr = np.column_stack((envLo[:,:3],envDiff))

print("Arrays stacked")

np.savetxt(wDir + os.sep + 'envelope_diff.txt', finalArr, delimiter=',')

print("done")
