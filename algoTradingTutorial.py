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

timeStart = time.time()

date, bid, ask = np.loadtxt('data/GBPUSD1d.txt', unpack=True, delimiter=',', converters={0:bytespdate2num('%Y%m%d%H%M%S')})

patternSize = 30
patternAr    = []
performanceAr = []
patForRec = []
toWhat = 37000
allData = ((bid+ask)/2)
avgLine = allData[:toWhat]
accuracyAr = []
samps      = 0




def percentChange(startPoint, currentPoint):
    try:
        x = ((float(currentPoint)-startPoint)/abs(startPoint))*100.00
        if x == 0.0:
            return 0.0000000001
        else:
            return x
    except:
        return 0.0000000001

def patternStorage():
    patStartTime = time.time()
    global patternAr, performanceAr

    x = len(avgLine) - 60
    y = patternSize + 1

    while y < x:
        points = []
        for i in range(0,patternSize):
            points.append(percentChange(avgLine[y-patternSize], avgLine[y-(patternSize-1-i)]))

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
    # print(len(patternAr))
    # print(len(performanceAr))
    # print("Pattern storage took: " + str(patEndTime - patStartTime) + " seconds")


def currentPattern():
    global patForRec
    points = []
    for i in range(0, patternSize):
        points.append(percentChange(avgLine[-1-patternSize], avgLine[i-patternSize]))
    patForRec = points

def sum(arr):
    return reduce(lambda x, y: x+y, arr)

def average(arr):
    if len(arr) == 0:
        return 0
    return (sum(arr)/len(arr))

def printFoundPattern(pattern):
    patdex = patternAr.index(pattern)
    print("#########################")
    print("#########################")
    print(patForRec)
    print("#########################")
    print("#########################")
    print(pattern)
    print("#########################")
    print("#########################")
    print("predicted outcome:, ", performanceAr[patdex])
    print("#########################")
    print("#########################")

def patternRecognition():
    #print("Pattern for recognition:", patForRec)
    global similarAr

    patFound = False
    plotPatAr = []
    count = 0
    for pattern in patternAr:
        points = []
        for i in range (0, patternSize):
            similarity = 100.00 - abs(percentChange(pattern[i], patForRec[i]))
            points.append(similarity)
        howSimilar = (sum(points)/len(points))

        if howSimilar > 75:
            #printFoundPattern(pattern)
            patFound = True
            plotPatAr.append(pattern)
            count += 1

    if patFound:
        plotPatterns(plotPatAr)



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


def plotPatterns(patterns):
    global patForRec, patternAr, performanceAr, toWhat, allData
    predAr = []
    predictedOutcomesAr = []
    xaxis = range(1,patternSize+1)
    #fig   = plt.figure(figsize=(10, 6))
    for pattern in patterns:
        futurePoints = patternAr.index(pattern)

        if performanceAr[futurePoints] > patForRec[-1]:
            pcolor = '#24bc00'
            predAr.append(1.000)
        else:
            pcolor = '#d40000'
            predAr.append(-1.000)

        predictedOutcomesAr.append(performanceAr[futurePoints])
        #plt.plot(xaxis, pattern)
        #plt.scatter(patternSize + 5, performanceAr[futurePoints], c=pcolor, alpha=.3)


    realAvgOutcomeRange = allData[toWhat+20:toWhat+30]
    realAvgOutcome = sum(realAvgOutcomeRange)/len(realAvgOutcomeRange)
    realMovement = percentChange(allData[toWhat], realAvgOutcome)
    predictedAvgOutcome = sum(predictedOutcomesAr)/len(predictedOutcomesAr)
    print(predAr)
    predictionAverage = average(predAr)
    print(predictionAverage)
    if predictionAverage < 0:
        print('drop predicted')
        print(patForRec[patternSize - 1])
        print(realMovement)
        if realMovement < patForRec[patternSize-1]:
            accuracyAr.append(100)
        else:
            accuracyAr.append(0)

    if predictionAverage > 0:
        print('rise predicted')
        print(patForRec[patternSize - 1])
        print(realMovement)
        if realMovement > patForRec[patternSize-1]:
            accuracyAr.append(100)
        else:
            accuracyAr.append(0)
    #plt.scatter(patternSize + 10, realMovement, c='#54fff7', s=25)
    # plt.scatter(patternSize + 10, predictedAvgOutcome, c='b', s=25)
    #
    # plt.plot(xaxis, patForRec, '#54fff7', linewidth = 3)
    # plt.grid(True)
    # plt.title('Pattern Recognition')
    # plt.show()


def run():
    global allData, patternAr, performanceAr, patForRec, avgLine, samps, allData, toWhat, timeStart

    dataLength = int(bid.shape[0])
    print("data length is:", dataLength)

    while toWhat < dataLength:
        avgLine = allData[:toWhat]
        patternAr    = []
        performanceAr = []
        patForRec = []

        patternStorage()
        currentPattern()
        patternRecognition()

        elapsedTime = time.time() - timeStart

        accuracyAverage = average(accuracyAr)
        print('Backtested Accuracy is', str(accuracyAverage),"% after ", samps, " samples")
        samps  += 1
        toWhat += 1
    print("Entire processing time took: ", elapsedTime, " seconds\n")
if __name__ == '__main__':
    #graphRawFX()
    run()

    #plotSimilarPatterns()
