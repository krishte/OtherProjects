import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from sklearn.linear_model import LinearRegression


xlist = [0.100,0.200,0.300,0.400,0.500,0.600,0.700,0.800,0.900,1.000]
ylist = [1650,1980,2330,2690,3030,3380,3700,4180,4420,4740]
xerrors = [0.005 for i in range(10)]
yerrors = [100.0 for i in range(10)]

minslopee = (ylist[-1]-yerrors[-1]-(ylist[0]+yerrors[0]))/(xlist[-1]+xerrors[-1]-(xlist[0]-xerrors[0]))
maxslopee = (ylist[-1]+yerrors[-1]-(ylist[0]-yerrors[0]))/(xlist[-1]-xerrors[-1]-(xlist[0]+xerrors[0]))
xlist2 = np.array(xlist).reshape((-1, 1))
model = LinearRegression().fit(xlist2, ylist)

modelintercept = model.intercept_


def f(minslope, maxslope, typee):
    count = 0
    adjustedintercept = 0
    savedyintercept = 0
    while (count < 15):
        tryslope = (minslope+maxslope)/2
        overallpossible = False
        for i in range(100000):
            possible = True
            adjustedintercept = modelintercept + (float(i)-50000.0)/100.0
            for j in range(len(xlist)):
                minyval = tryslope*(xlist[j]-xerrors[j])+adjustedintercept
                maxyval = tryslope*(xlist[j]+xerrors[j])+adjustedintercept
                minpossibleyval = ylist[j]-yerrors[j]
                maxpossibleyval = ylist[j]+yerrors[j]
                if (minyval > maxpossibleyval or maxyval < minpossibleyval):
                    possible = False
                    break
            if possible:
                overallpossible = True
                savedyintercept = adjustedintercept
                break
        if (typee == 1):
            if (overallpossible):
                minslope = tryslope
            else:
                maxslope = tryslope
        else:
            if (overallpossible):
                maxslope = tryslope
            else:
                minslope = tryslope
        count += 1
    return (minslope, savedyintercept)
   # print(model.coef_[0], minslope)
            
print(minslopee, maxslopee)
print(model.coef_[0], f(minslopee, maxslopee, 0), f(minslopee, maxslopee, 1))

    

