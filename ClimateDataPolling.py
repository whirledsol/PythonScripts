"""
ClimateDataPolling.py
Created:
@author: Will Rhodes
 
"""

from Helpers.GraphFxts import *
from Helpers.NumericalFxts import *
from Models.GeographicLocation import *
import csv
import numpy as np

def start():
    print("Starting Program")
    datafile = './Data/NOAA_Monthly_Climatological_Summary_2010.csv'
    datalist = GetGeographicDataList(datafile)
    print('2nd pass stores {0} items'.format(len(datalist)))
    datalist = narrowStationsByClimateBounds(datalist)
    print('3rd pass stores {0} items'.format(len(datalist)))
    #####################################################################
    #print([[x.Name,x.Climate.GetAvgDailyHighWinter()] for x in datalist])
    #####################################################################
    PlotGeographicDataList(datalist)
    #####################################################################
    if 0==1:
        testlocation = filterByName(datalist,'PHILADELPHIA')[0]
        print(testlocation.toString())
        print(testlocation.Climate.toString())
        ScatterPlot(list(range(1,13)),testlocation.Climate.MeanTempMonthly,errors=[x/2.0 for x in testlocation.Climate.MeanDiurnalRangeMonthly], title=testlocation.Name + ' Mean Temp with Diurnal Variance', xlabel='Month',ylabel='Degrees (F)')
        #ScatterPlot(list(range(1,13)),testlocation.Climate.MaxTempMonthly,errors=[x/2.0 for x in testlocation.Climate.MeanStdDevMonthly], title=testlocation.Name + ' Max Temp with Std Dev', xlabel='Month',ylabel='Degrees (F)')
    #####################################################################
    
    
def GetGeographicDataList(datafile):
    GeographicDataList = []    
    with open(datafile, newline='') as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.read(1024))
        csvfile.seek(0)  # rewind        
        csvReader = csv.reader(csvfile)    
        if has_header:
            next(csvReader)
        currentstation = ""
        stationdata = []
        for row in csvReader:
            if row[0] != currentstation:
                #we changed stations
                if len(stationdata) > 0: 
                    GeographicDataList.append(GeographicLocation(stationdata))
                stationdata = []
            currentstation = row[0]
            stationdata.append(row)
    print('First pass stores {0} items'.format(len(GeographicDataList)))
    return [x for x in GeographicDataList if x.IsValid()]
    
def PlotGeographicDataList(datalist):
    xs = []
    ys = []
    zs = []
    for item in datalist:
        xs.append(item.Longitude)
        ys.append(item.Latitude)  
        zs.append(item.Climate.MeanTempAvg)
        #print(zs)
    AmericaMapScatter(xs,ys,zs)

def narrowStationsByClimateBounds(datalist):
    idealThresholdMinT = 20
    idealThresholdMaxT = 90
    idealRangeSummerMeanT = (65,84)
    idealRangeWinterMeanT = (46,80)
    eaternOnly = 1==1#float(location.Longitude) > -95.0
    narrowedList = []
    for location in datalist:
        if eaternOnly and location.Climate.MinTemp >= idealThresholdMinT and location.Climate.MaxTemp <= idealThresholdMaxT and (idealRangeSummerMeanT[0] <= location.Climate.GetAvgDailyHighSummer() <= idealRangeSummerMeanT[1]) and (idealRangeWinterMeanT[0] <= location.Climate.GetAvgDailyHighWinter() <= idealRangeWinterMeanT[1]):
            narrowedList.append(location)
    return narrowedList

def filterByName(datalist, state):
    return [x for x in datalist if state in x.Name]
if  __name__ =='__main__':start()
