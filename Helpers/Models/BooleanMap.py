# -*- coding: utf-8 -*-
"""
Created on Sun Jul 07 16:31:26 2013

@author: Will Rhodes
"""
import numpy as np
import math

#creates the boolean map from a list of skyObjects (data) with a specified 
class BooleanMap:
    resolution = 360
    dSize = 360./resolution
    countMap = np.zeros([resolution,resolution])
    
	#constuctor
    def __init__(self,data,bins=360):
        self.resolution = bins
        self.dSize = 360./self.resolution
        self.countMap = np.zeros([self.resolution,self.resolution])
        
        for point in data:
            if hasattr(point,'RA'): #if it has RA assume it has DEC
                raPos = int(math.floor(point.RA / self.dSize))
                decPos = int(math.floor(point.DEC / self.dSize))
                #row x col or dec x ra
                self.countMap[raPos,decPos] = self.countMap[raPos,decPos] +1
            else:
                print "can't parse data into the map"
                
    
    def inSurvey(self,ra,dec):
        raPos = int(math.floor(ra / self.dSize))
        decPos = int(math.floor(dec / self.dSize))
        cell = self.countMap[raPos,decPos]
        if cell == 0:
            return False
        else:
            return True
    
    def toString(self):
        return np.array_str(self.countMap)
            
        