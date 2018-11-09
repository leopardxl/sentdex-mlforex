import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time
from functools import reduce
import math


def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter



date, bid, ask = np.loadtxt('data/GBPUSD1d.txt', unpack=True, delimiter=',', converters={0:bytespdate2num('%Y%m%d%H%M%S')})

patternAr    = []
performanceAr = []

def percentChange(startPoint, currentPoint):
    return ((currentPoint-startPoint)/abs(startPoint))*100.00

def patternStorage():
    patStartTime = time.time()

    avgLine = ((bid + ask)/2.0)
    x = len(avgLine) - 30
    y = 11

    while y < x:
        points = []
        for i in range(0,10):
            points.append(percentChange(avgLine[y-10], avgLine[y-(9-i)]))

        outcomeRange = avgLine[y+20:y+30]
        currentPoint = avgLine[y]
        try:
            avgOutcome = reduce(lambda x, y: x+y, outcomeRange) / len(outcomeRange)
        except Exception as e:
             print(str(e))
             avgOutcome = 0

        futureOutcome = percentChange(currentPoint, avgOutcome)

        patternAr.append(points)
        performanceAr.append(futureOutcome)

        # print(currentPoint)
        # print("---------")
        # print(points)


        y += 1

    patEndTime = time.time()
    print(len(patternAr))
    print(len(performanceAr))
    print("Pattern storage took: " + str(patEndTime - patStartTime) + " seconds")
    
def graphRawFX():
    fig = plt.figure(figsize=(10,7))
    ax1 = plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)

    ax1.plot(date, bid)
    ax1.plot(date, ask)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax1_2 = ax1.twinx()
    ax1_2.fill_between(date,0, (ask-bid), facecolor='g', alpha=.3)


    plt.subplots_adjust(bottom=.23)

    plt.grid(True)
    plt.show()



if __name__ == '__main__':
    #graphRawFX()
    patternStorage()
