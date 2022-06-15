"""
measurements.py
Includes all the mathematical functions used in the qso project from MMA Summer 2013

"""
import math,numpy,NumericalFxts

try:
    import Models.SkyObjects
except:
    print "could not import skyObject"



H_0 = 72.0
SpeedOfLight = 2.997e5 #km/s
#FLRW = LambdaCDM(H_0,0.27,0.73)          
# gets angular distance based on the real transverse distance
# param: orbitDis: the distance between the two objects, z1: the redshift of object1, z2: the redshift of object2
def getAngularThreshold(orbitDis,z):

    angle = orbitDis*(H_0*(1+z)**2)/(2.0*SpeedOfLight*(1+z-math.sqrt(1+z)))

    #print toDegree(angle)
    return toDegree(angle)
# given the angle of seperation and the two redshifts, calculate the projected seperation
# params: angular seperation (degrees) and their two redshifts
# returns distance from formula given in Mpc
def getProjectedDis(angle,z1,z2):
    #    #use average redshift
    z = (float(z1)+float(z2))/2
#    R = 1/(1+z)
#    comovingTransverse = FLRW.comoving_transverse_distance(z)*toRad(angle)*R
#
#    # THIS IS WHAT'S HAPPENING ABOVE    
#    #    func = lambda z: (0.27*((1+z)**3)+1-0.27)**(-0.5)
#    #    try:
#    #        integrationResult = integrate.quad(func,0,z)
#    #        integrationResult = integrationResult[0]
#    #    except:
#    #        print "Error integrating"
    
    
    
    D = (2.0*toRad(angle)*SpeedOfLight*(1+z-math.sqrt(1+z)))/(H_0*(1+z)**2)
    #print "2D Projection"
    #print "Using Comoving transverse: ",comovingTransverse,"  and using the original way:", D    
    
    return D


# given the RA and DEC of two objects, get their angular seperation 
# returns angle in degrees    
def getAngularSep(a1,d1,a2,d2):
    #convert all inputs to floats
    a1 = float(a1)
    d1 = float(d1)
    a2 = float(a2)
    d2 = float(d2)
    
    if (a1==a2) and (d1==d2): #if equal, they have no angular seperation
        return 0.0
    
    try:
        angularSep = math.acos(math.sin(toRad(d1))*math.sin(toRad(d2))  +  math.cos(toRad(d1)) * math.cos(toRad(d2))*math.cos(toRad(a1)-toRad(a2)))
        angularSep = toDegree(angularSep) #convert from radians, back to degrees
    except:
        print "\n"+str(a1)+" "+str(d1)+" "+str(a2)+" "+str(d2)
        angularSep = 9000 #high number so that it won't be factored in
   
    return angularSep    

#converts param: dz with z1 and z2 to the rest frame velocity between objects
# returns rest frame velocity in km/s
def dzTodv(z1,z2):  
    z = (z1+z2)/2
 
    v1_here = (SpeedOfLight*((1+z1)**2) - SpeedOfLight)/(1+((1+z1)**2))
    v2_here = (SpeedOfLight*((1+z2)**2) - SpeedOfLight)/(1+((1+z2)**2))
    
    dv_here = abs(v1_here - v2_here)
    #print dv_here
    dv_there = dv_here/(1+z)
    return dv_there
    
    
    
#converts an items RA,DEC,Z to x,y,z for plotting
#params: r=RA, d=DEC, z=REDSHIFT
#returns: out = list of x,y,z    
def RDZtoXYZ(r,d,rs):


    #convert inputs to floats
    rs = float(rs)    
    d = float(d)
    r = float(r)


    #constants
    H_0 = 67.80;
    SpeedOfLight = 2.997e5 #km/s
    
    #calculations
    v_here = (SpeedOfLight*((1+rs)**2 - 1))/(1+(1+rs)**2)
    dis = (v_here)/(H_0)    #TODO: take into account cosmological redshift
                            #TODO: take into account FRW Metric

    #coordinate transformation
    x = dis*math.sin(toRad(d))*math.cos(toRad(r))
    y = dis*math.sin(toRad(d))*math.sin(toRad(r))
    z = dis*math.cos(toRad(d))
    return [x,y,z]
    


#takes into account the actual distance between two extragalactic objects
def get3Ddistance(qso,eachCluster):
    disProj = getProjectedDis(getAngularSep(qso.RA,qso.DEC,eachCluster.RA,eachCluster.DEC),qso.z,eachCluster.z)
    z = abs(qso.z - eachCluster.z)/2
    H_there = H_0*math.sqrt(0.27*((1+z)**3) + 0.73)  
    
    #get recessional velocity of the two objects
    v2 = (SpeedOfLight*((1+eachCluster.z)**2) - SpeedOfLight)/(1+((1+eachCluster.z)**2))
    v1 = (SpeedOfLight*((1+qso.z)**2) - SpeedOfLight)/(1+((1+qso.z)**2))
    
    #get the proper distance using Hubble's Law    
    r2 = v2/H_0
    r1 = v1/H_0
    
    
    R = 1/(1+z)
    disRad = R*abs(r2-r1)
    
    #now assuming the universe is flat there
    dis = math.sqrt(disRad**2 + disProj**2)
    #print dis
    return dis

#takes into account the actual distance between two extragalactic objects
def get3Ddistance_v2(qso,eachCluster):
    print "abandoned method"
    return None
#    z = abs(qso.z+eachCluster.z)/2
#    R=1
#    
#    x1 = R* FLRW.comoving_distance(qso.z)*math.sin(toRad(qso.DEC))*math.cos(toRad(qso.RA))
#    y1 = R* FLRW.comoving_distance(qso.z)*math.sin(toRad(qso.DEC))*math.sin(toRad(qso.RA))
#    z1 = R* FLRW.comoving_distance(qso.z)*math.cos(toRad(qso.DEC))
#    
#    x2 = R* FLRW.comoving_distance(eachCluster.z)*math.sin(toRad(eachCluster.DEC))*math.cos(toRad(eachCluster.RA))
#    y2 = R* FLRW.comoving_distance(eachCluster.z)*math.sin(toRad(eachCluster.DEC))*math.sin(toRad(eachCluster.RA))
#    z2 = R* FLRW.comoving_distance(eachCluster.z)*math.cos(toRad(eachCluster.DEC))    
#    
#    dis = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
#    return dis


def compare(obj1,obj2):
    print "abandoned method"
    return None
#    z = abs(obj1.z - obj2.z)/2
#    
#    angularDiaDis = toRad(getAngularSep(obj1.RA,obj1.DEC,obj2.RA,obj2.DEC))*FLRW.angular_diameter_distance(obj1.z,obj2.z)
#    print "angular diameter distance z1z2: ",angularDiaDis
#    print "vs...",getProjectedDis(getAngularSep(obj1.RA,obj1.DEC,obj2.RA,obj2.DEC),obj1.z,obj2.z)
    #disProj = FLRW.comoving_distance(z)
    #print "comoving radial dis in Mpc: ",disProj
    
    
###############################################################################


#utility function that can be used to get max values for normalization - FAILED
def getMaxValues(galaxyClusters,pairedQSOs,isolatedQSOs,limiter):
    maximumProj = -1
    maximumdV = -1
    allQSOs = pairedQSOs + isolatedQSOs
    for eachQSO in allQSOs:
        for eachGal in galaxyClusters:
            if (math.fabs(float(eachGal.RA) - float(eachQSO.RA)) < limiter) and (math.fabs(float(eachGal.DEC) - float(eachQSO.DEC)) < limiter) and (math.fabs(float(eachGal.z) - float(eachQSO.z)) < limiter):
                tempProj = getProjectedDis(getAngularSep(eachQSO.RA,eachQSO.DEC,eachGal.RA,eachGal.DEC),eachQSO.z,eachGal.z)
                tempdV = dzTodv(eachQSO.z,eachGal.z)
                
                if tempProj > maximumProj:
                    maximumProj = tempProj
                if tempdV > maximumdV:
                    maximumdV = tempdV
    output = open("results\maxValues_WenBoss.txt","w")
    output.write("Max Proj Distance: " + str(maximumProj)+ " and Max dv: "+str(maximumdV))
    return maximumProj,maximumdV
    
##############################################################################
def getPosAngle(ra1,dec1,ra2,dec2):
    ra1 = toRad(float(ra1))
    ra2 = toRad(float(ra2))
    dec1 = toRad(float(dec1))    
    dec2 = toRad(float(dec2))    
    
    radiff  = ra2-ra1
    angle  = math.atan2(math.sin(radiff),math.cos(dec1)*math.tan(dec2)-math.sin(dec1)*math.cos(radiff))
    angle = toDegree(angle)    
    #print angle
    if angle < 0:
        angle = angle+360
    return angle


#gets an object with the angle RA,DEC,and Z
def midpoint(item1,item2 = None):
    if type(item1) == list:
        item2 = item1[1]
        item1 = item1[0]
    
    #print item1.RA,item2.RA,item1.DEC,item2.DEC
    
    midRa = avg_angle(item1.RA,item2.RA)
    midDec = avg_angle(item1.DEC,item2.DEC)
#    
#    if midDec<0:
#        midDec = midDec+360.
#    if midRa <0:
#        midRa = midRa+360.
    
    midZ = (item1.z+item2.z)/2
    
    #print "MIDPOINT: ",midRa,midDec
    return SkyObjects.skyObject([midRa,midDec,midZ])

def avg_angle(ra1,ra2):
    ra1 = float(ra1)
    ra2 = float(ra2)
    
    maxAng = max([ra1,ra2])
    minAng = min([ra1,ra2])
  
    if maxAng>270. and minAng<90.:
        #woah now, we're dealing with some circle stuff
        maxAng = (maxAng-360)
    
    returning = (maxAng+minAng)/2
    if returning <0:
        returning +=360
    
    return returning     

#    midRa = 0   
#    minAngle = min([ra1,ra2])
#    if minAngle > 90 and minAngle <270:
#        midRa = 180
#    if minAngle>270 and minAngle<360:
#        midRa = 360
#    ra1i = math.cos(toRad(ra1))
#    ra1j = math.sin(toRad(ra1))
#    ra2i = math.cos(toRad(ra2))
#    ra2j = math.sin(toRad(ra2))
#    midRa += toDegree(math.atan((ra1j+ra2j)/(ra1i+ra2i)))   
#    return midRa   
    
def angleDiff(a1,a2):
    a1 = float(a1)
    a2 = float(a2)
    maxAng = max([a1,a2])
    minAng = min([a1,a2])
  
    if maxAng>270. and minAng<90.:
        #woah now, we're dealing with some circle stuff
        maxAng = (maxAng-360.)
    
    returning = maxAng-minAng
    
    if abs(returning)>90.:
        returning = 180 - abs(returning)
    
    return returning   

#standard deviation of mean or standard error
def SDOM(data):
    sd = stdDev(data)
    return sd/math.sqrt(len(data))

#standard deviation      
def stdDev(data):
    mean = numpy.mean(data)
    sumterm = 0
    for each in data:
        sumterm +=(each-mean)**2
    returning = math.sqrt((1/(float(len(data))))*sumterm)
    
    return returning
  
