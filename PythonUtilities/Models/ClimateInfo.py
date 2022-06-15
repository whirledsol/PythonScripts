# -*- coding: utf-8 -*-
"""
@author: Will Rhodes
"""
from Helpers.NumericalFxts import *
from Helpers.ListFxts import *
import numpy as np

class ClimateInfo:

	#constuctor
    def __init__(self,data):
        self.datarows = data
        self.TotalPrecipMonthly = []
        self.MaxTempMonthly = []
        self.MinTempMonthly = []
        self.MaxTempMonthly = []
        self.MeanTempMonthly = []
        self.MeanDiurnalRangeMonthly = []
        self.MeanStdDevMonthly = []
        for row in data:
            self.TotalPrecipMonthly.append(TryConvertFloat(row[6]))
            self.MeanTempMonthly.append(TryConvertFloat(row[7]))
            self.MeanDiurnalRangeMonthly.append(TryConvertFloat(row[8]))
            self.MaxTempMonthly.append(TryConvertFloat(row[9]))
            self.MinTempMonthly.append(TryConvertFloat(row[10]))
            self.MeanStdDevMonthly.append(TryConvertFloat(row[11]))
        
        self.MaxTemp = max(self.MaxTempMonthly)
        self.MinTemp = min(self.MinTempMonthly)
        self.MeanTempAvg = Mean(self.MeanTempMonthly)
        self.TotalPrecipAvg = Mean(self.TotalPrecipMonthly)
        self.MeanDiurnalRangeAvg = Mean(self.MeanDiurnalRangeMonthly)
        self.MeanStdDevAvg = Mean(self.MeanStdDevMonthly)
        
    def IsValid(self):
        if -9999.0 in self.TotalPrecipMonthly or  -9999.0 in self.MeanTempMonthly or -9999.0 in self.MeanDiurnalRangeMonthly or -9999.0 in self.MaxTempMonthly or -9999.0 in self.MinTempMonthly or -9999.0 in self.MeanStdDevMonthly:
            return False
        else:
            return True
            
    def GetAvgDailyHighSummer(self):
        if not self.IsValid():
            return None
        greatest,indices = Greatest(self.MeanTempMonthly,3,True)
        summermean = Mean(greatest)
        halfdiurnal = Mean([x for i,x in enumerate(self.MeanDiurnalRangeMonthly) if i in indices]) / 2.0
        return summermean + halfdiurnal
        
    def GetAvgDailyHighWinter(self):
        if not self.IsValid():
            return None
        least,indices = Least(self.MeanTempMonthly,3,True)
        wintermean = Mean(least)
        halfdiurnal = Mean([x for i,x in enumerate(self.MeanDiurnalRangeMonthly) if i in indices]) / 2.0
        return wintermean + halfdiurnal

    def GetAvgLengthofSpringFall(self):
        return 0.0
        
    def toString(self):
        return "|| MaxTemp: {0} | MinTemp: {1} | GetAvgDailyHighSummer: {2} | GetAvgDailyHighWinter: {3} ||".format(self.MaxTemp, self.MinTemp, self.GetAvgDailyHighSummer(), self.GetAvgDailyHighWinter() )
            
        