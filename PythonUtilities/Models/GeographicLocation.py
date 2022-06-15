# -*- coding: utf-8 -*-
"""
@author: Will Rhodes
"""

from .ClimateInfo import ClimateInfo
from Helpers.NumericalFxts import *

class GeographicLocation:

	#constuctor
    def __init__(self,data):
        self.datarows = data
        self.Id = data[0][0]
        self.Name = data[0][1]
        self.Latitude = data[0][3]
        self.Longitude = data[0][4]
        self.Elevation = data[0][2]
        self.Climate = ClimateInfo(data) 
            
    def IsValid(self):
        if is_number(self.Latitude) and is_number(self.Latitude) and self.Climate.IsValid():
            return True
        else:
            return False
    
    def toString(self):
        return '{0} @ ({1},{2})'.format(self.Name,self.Latitude,self.Longitude)
            
        