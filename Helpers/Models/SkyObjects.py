# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 17:07:19 2013

@author: Will
"""
from measurements import getProjectedDis,dzTodv
# SDSS SQL QUERY
# Select ra,dec,z,objID
#FROM SpecPhotoAll 
#where sourceType='GALAXY' and class='GALAXY'
#and mjd in (Select max(mjd) FROM SpecPhotoAll group by objID)
#order by ra


class skyObject:
    RA = 0.0
    DEC = 0.0
    z = 0.0
    flux = None
    def __init__(self,params):
        try:      
            self.RA = float(params[0])
            self.DEC = float(params[1])
            self.z = float(params[2])
            
            if self.DEC < 0:
                self.DEC = self.DEC + 360.0  
                
        except Exception as e:
            print(e)
            try:
                print("Problem importing item with RA=", self.RA)
            except:
                print("Problem importing item")
        try:
            if len(params) > 3:
                self.flux = float(params[3])
        except:
            print("Error importing flux to object")
    
    def __eq__(self, other):
        return self.getElements() == other.getElements()      
    
    def __hash__(self): return hash(id(self))
    
    def getElements(self):
        return [self.RA,self.DEC,self.z,self.flux]
    def toString(self):
        returning = str(self.RA)+","+str(self.DEC)+","+str(self.z)
        if self.flux is not None:
            returning+=",flux="+str(self.flux)
        
        return returning            
###############################################################################
class GalaxyCluster:
   
    def __init__(self,data):
        try:
            self.id = data[1]
            self.RA = float(data[2])
            if self.RA < 0:
                self.RA = self.RA + 360.0
            self.DEC = float(data[3])  
            if self.DEC < 0:
                self.DEC = self.DEC + 360.0            
            self.z = float(data[4])     
            self.MAG = data[6]
            
            self.clusterSize = float(data[9])
        except Exception as e:
            print(e)         
            exit()
            try:
                print("Problem importing cluster: " +  ", ".join(map(str, data)))
            except:
                print("Problem importing galaxy cluster: unknown")
 
       
        
        
    def toString(self,params=""):
        if params == "-v" or params == "v" or params == "verbose":
            return "ID: " + str(self.id)+ " | RA: " + str(self.RA) + " | DEC: " + str(self.DEC) + " | Z: " + str(self.z)
        else:
            return str(self.RA)+","+str(self.DEC)+","+str(self.z)
        
###############################################################################

class QSO:
 




   
    def __init__(self,data):
        
        if len(data) == 3:
            data = ["","","",data[0],data[1],data[2],"",""]
        try:
            self.id = data[0]
            self.surveyName = data[1].strip(' \t\n\r')
            self.MJD = data[2].strip(' \t\n\r') 
            self.RA = data[3].strip(' \t\n\r')
            if self.RA < 0:
                self.RA = self.RA + 360
            self.DEC = data[4].strip(' \t\n\r')  
            if self.DEC < 0:
                self.DEC = self.DEC + 360                    
            self.z = float(data[5].strip(' \t\n\r'))     
            self.MAG = data[6].strip(' \t\n\r')
            self.type = data[7].strip(' \t\n\r')
            self.hasNeighbor = False
        except:
            try:
                print("Problem importing QSO: " + str(data[0]))
            except:
                print("Problem importing QSO: unknown")

        
    def sethasNeighbor(self,boolean):
        self.hasNeighbor = boolean
        
        
    def toString(self,params=""):
        if params == "-v" or params == "v" or params == "verbose":
            return "ID: " + str(self.id)+ " | RA: " + str(self.RA) + " | DEC: " + str(self.DEC) + " | Z: " + str(self.z)
        else:
            return str(self.RA)+","+str(self.DEC)+","+str(self.z)

class qsoCluster:

    qsoClusterList = []
    angles = []
    projDisList = []
    dvList = []
    size = 0


    #CONSTRUCTER
    def __init__(self,qso1,qso2,angle):
        self.qsoClusterList = []
        self.angles = []     
        self.projDisList = []
        self.dvList = []
        self.size = 2
        
        self.qsoClusterList.append(qso1)
        self.qsoClusterList.append(qso2)
        self.angles.append(angle)
        
        projDis = getProjectedDis(angle,qso1.z,qso2.z)
        dv = dzTodv(qso1.z,qso2.z)        
        
        
        self.projDisList.append(projDis)
        self.dvList.append(dv)
        
    def appendQSO(self,qsoExisting,qsoNew,angle):
        
               
        self.qsoClusterList.append(qsoExisting)
        self.angles.append(-1)
        self.projDisList.append(-1)
        self.dvList.append(-1)
                
        self.qsoClusterList.append(qsoNew)
        self.angles.append(angle)
        projDis = getProjectedDis(angle,qsoExisting.z,qsoNew.z)
        dv = dzTodv(qsoExisting.z,qsoNew.z)             
        self.projDisList.append(projDis)
        self.dvList.append(dv)
        
        self.check()
        
        self.size = self.size+1
    
    def hasQSO(self,qso):
        if qso in self.qsoClusterList:
            return True
        else:
            return False
    
    #checks to see if the two arrays are in sync, if not - we have a problem
    def check(self):
        if (len(self.angles) == len(self.projDisList)) and (len(self.projDisList) == len(self.dvList)) and (len(self.angles) == len(self.qsoClusterList)-1):
            return True
        else:
            print("LENGTHS: "+str(len(self.dvList))+" "+str(len(self.angles)) + " " + str(len(self.projDisList))+ " " + str(len(self.qsoClusterList)))
            return False
            
    def getSize(self):
        return self.size

    def getUniqueQSOs(self):
        return list(set(self.qsoClusterList))
        
    def toString(self):
        fString = ""
        for i in range(0,len(self.qsoClusterList)):
            
            fString = fString + self.qsoClusterList[i].toString()
            
        
            if i<len(self.qsoClusterList)-1:
                if self.angles[i] == -1:
                    fString = fString+"\n\n"
                else:
                    fString = fString + " || ANGLE: "+ str(self.angles[i]) + " degrees || projDIS: " + str(self.projDisList[i])+ " Mpc || dv: " + str(self.dvList[i])+" km/s \n"
            else:
                fString = fString + "\n"
        return fString        
        
###############################################################################
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False