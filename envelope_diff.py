import os, sys, glob
import numpy as np

wDir = 'outputs/envelope'
#open envelope files
envLo = np.loadtxt(wDir + os.sep + 'envelope_lower.txt', delimiter=",")
envUp = np.loadtxt(wDir + os.sep + 'envelope_upper.txt', delimiter=",")

envDiff = envUp[:,3] - envLo[:,3]

finalArr = np.column_stack((envLo[:,:3],envDiff))

np.savetxt(wDir + os.sep + 'envelope_diff.txt', finalArr, delimiter=',')
