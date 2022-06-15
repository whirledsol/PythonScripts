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
import pandas as pd
import re
def start():
    print("Starting Program")
    datafile = './Data/PPD_Crime_Incidents_2006-Present.csv'
    Data = DataMapper(datafile)
    #print('Data Length: {0}'.format(len(Data)))
    print(Data.dtypes)
    Data = Data[(Data.Lat.isnull() == False) & (Data.Lon.isnull()== False)]
    for i in range(5):
        print(str(Data.iloc[i].Lat) + '  ' + str(Data.iloc[i].Lon ))
    #####################################################################
    ShowCrimeMap(Data)
    
def DataMapper(datafile):
    Data = pd.read_csv(datafile)
    
    """ Sort by date
    Dat = pd.to_datetime(Data.Dispatch_Date_Time)
    Data.Dispatch_Date_Time = Dat
    Data.sort_values(by='Dispatch_Date_Time', inplace=True)
    Data.index = np.array(range(Data.shape[0]))
    Dat = pd.to_datetime(Data.Dispatch_Date_Time)
    Data['all_hour'] = abs(Dat - Dat[0]).dt.total_seconds() / 3600.0
    """
    return Data
    
def ShowCrimeMap(Data):
    m = Basemap(projection='mill', llcrnrlat=Data.Lat.min(), urcrnrlat=Data.Lat.max(), llcrnrlon=Data.Lon.min(), urcrnrlon=Data.Lon.max(), resolution='c', epsg=4269)
    x, y = m(tuple(float(Data.Lon)), tuple(float(Data.Lat)))
    
    plt.figure(figsize=(20,10))
    m.arcgisimage(service="NatGeo_World_Map", xpixels=3000, verbose=True)
    m.plot(x,y,'ro',markersize=3, alpha=0.6 )

def filterByName(datalist, state):
    return [x for x in datalist if state in x.Name]
if  __name__ =='__main__':start()
