# -*- coding: utf-8 -*-
"""
Graphing

Created on Wed Jun 26 22:22:00 2013

@author: Will
"""
import numpy,scipy
from collections import OrderedDict
import matplotlib as matplotlib
import matplotlib.pyplot as plt
from NumericalFxts import *
from ListFxts import *
from AstroFxts import *
from Tkinter import Tk
from tkFileDialog import askopenfilename
try:
    from CorrelationFinder import getNumPerRange
except ImportError:
    print 'could not import getNumPerRange'



#parses 
def parsePoints(filepath = None,returnValues=True):
    if filepath is None:
        #get the file
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filepath = askopenfilename(initialdir="C:\Users\Will\Dropbox\_MMA Research\Quasar Project\qsoProgram\\results\CSVSurveys") # show an "Open" dialog box and return the path to the selected file
        #print(filepath)
        
        #get the data file
        file = open(filepath,"r")
        lines = file.readlines()
        file.close
        
        pXs = []
        pYs = []
        pErrors = []
        
        iXs = []
        iYs = []
        iErrors = []
       
            
        #assume structure: X, Y, Error for each line
        for i in range(len(lines)):
            row = convertAllToFloat(lines[i].split(','))
            pXs.append(row[0])
            pYs.append(row[1])
            try:
                pErrors.append(row[2])
                iXs.append(row[3])
                iYs.append(row[4])
                iErrors.append(row[5])
            except Exception as e:
                print e


        
        if not returnValues:
            MultiScatterPlot([pXs,pYs,iXs,iYs],title="",xLabel="Distance from Quasar",yLabel="Number of Galaxies inside",titles=["Paired Quasars","Isolated Quasars"],errorBars=[pErrors,iErrors])
        else:
            return pXs,pYs,pErrors,iXs,iYs,iErrors




###############################################################################
##          GRAPHS
###############################################################################
def dualPolarPlot(Angles1,Angles2,title1="Real",title2="Random",inDegrees=True):
    Angles1Rad = []
    Angles2Rad = []
    if inDegrees:        
        for i in range(len(Angles1)):
            Angles1Rad.append(toRad(Angles1[i]))
        for j in range(len(Angles2)):
            Angles2Rad.append(toRad(Angles2[j]))
    else:
        Angles1Rad = Angles1
        Angles2Rad = Angles2
            
    fig = plt.figure()
    plot1 = fig.add_subplot(121,projection='polar')
    plot1.scatter(Angles1Rad,numpy.ones(len(Angles1Rad)),color='r',s=15,lw=0)
    plot1.set_title(title1)
    
    plot2 = fig.add_subplot(122,projection='polar')
    plot2.scatter(Angles2Rad,numpy.ones(len(Angles2Rad)),color='b',s=15,lw=0)
    plot2.set_title(title2)
    
    
    plt.show()
    
def dualScatterPlot(X1,Y1,X2,Y2,title1="Pairs",title2="Isolated",xLabel= "Proj. Dis (Mpc)",yLabel= "dv (km/s)",sameGraph=False,saveAs=None):
    
    
    #print len(X1),len(Y1),len(X2),len(Y2)
    #create bar graphs   
    fig = plt.figure()
    
    
    if sameGraph: #plot on one graph
        plot1 = fig.add_subplot(111)
        pairs = plot1.scatter(X1,Y1,color='r',s=5)
        isolated = plot1.scatter(X2,Y2,color='b',s=2)
        lnd =  plot1.legend([pairs,isolated],[title1,title2])
        lnd.draggable(True)
        plot1.set_ylabel(yLabel)
        plot1.set_xlabel(xLabel)
        
    
    else:
        plot1 = fig.add_subplot(211)
        plot1.scatter(X1,Y1,color='r',s=5)
        plot1.set_ylabel(yLabel)
        plot1.set_xlabel(xLabel)
          
        
        plot2 = fig.add_subplot(212)
        plot2.scatter(X2,Y2,color='b',s=5)
        plot2.set_ylabel(yLabel)
        plot2.set_xlabel(xLabel)
    
    if saveAs is not None:
        saveGraph(fig,saveAs)
        
    plt.show()
    

#points are lists in lists of [x1,y1,x2,y2,x3,y3,...]
def MultiScatterPlot(points,titles=[],xLabel= "x",yLabel= "y",title="",errorBars=[],saveAs=None):
        
    fig = plt.figure()
    plot1 = fig.add_subplot(111)
    plot1.set_title(title)
    markers='oHv^<>8sp*hDdoHv^<>8sp*hDd'
    colors='rbcmykcmykbgrcmykcmykbgbgr'
    graphs = []
    for i in xrange(0,len(points),2):
        m = markers[i:i+1]
        c = colors[i:i+1]
        try:
            errors = errorBars[i/2]
            #print errors
            graph = plot1.errorbar(points[i],points[i+1],yerr=errors,color=c,fmt='o')
        except Exception as e:
            print e
            graph = plot1.scatter(points[i],points[i+1],marker=m,color=c,s=30/(i+1))
        graphs.append(graph)
   
    lnd = plot1.legend(graphs,titles)
    lnd.draggable(True)
    plot1.set_ylabel(yLabel)
    plot1.set_xlabel(xLabel)

    
    if saveAs is not None:
        saveGraph(fig,saveAs)
    else:   
        plt.show()

    
    
def dualBestFit(X1,Y1,X2,Y2,order=2,res = 100,sameGraph=True,title1="Pairs",title2="Isolated",xLabel= "Proj. Dis (Mpc)",yLabel= "Count"):
    #x1 = numpy.linspace(0, len(pairsNumDisCorr), len(pairsNumDisCorr))
    #x2 = numpy.linspace(0, len(isoNumDisCorr), len(isoNumDisCorr))
    
    bestFitEq1 = numpy.polyfit(X1, Y1, order)
    bestFitEq2 = numpy.polyfit(X2, Y2, order)
    print bestFitEq1
    print bestFitEq2
    
    
    func1 = numpy.poly1d(bestFitEq1)    
    func2 = numpy.poly1d(bestFitEq2)
    
    x1 = numpy.linspace(0, max(X1), res)
    x2 = numpy.linspace(0, max(X2), res)
    
    y1 = func1(x1)
    y2 = func2(x2)
    
    fig = plt.figure()
    
    if sameGraph:
        plot1 = fig.add_subplot(111)
        plot1.scatter(X1, Y1)        
        plot1.scatter(X2, Y2)
        pairs, = plot1.plot(x1, y1, color='r')
        isolated, = plot1.plot(x2, y2, color='b')
        plot1.legend([pairs,isolated],[title1,title2])
        plot1.set_ylabel(yLabel)
        plot1.set_xlabel(xLabel)
    else:
        plot1 = fig.add_subplot(211)
        plot2 = fig.add_subplot(212)
        
        plot1.plot(x1, y1, color='r')
        plot2.plot(x2, y2, color='b')
        plot2.set_ylabel(yLabel)
        plot2.set_xlabel(xLabel)
    plt.show()        
        
    
def dualHistogram2D(X1,Y1,X2,Y2,res=16,title1='Pairs',title2='Isolated',xLabel= "Proj. Dis (Mpc) binned",yLabel= "dv (km/s) binned"):
    
    hist1,xedges1, yedges1= numpy.histogram2d(X1,Y1,bins=res)
    hist2,xedges2, yedges2= numpy.histogram2d(X2,Y2,bins=res)
    #print xedges1," ",yedges1
    #create bar graphs   
    fig = plt.figure()
    
    #set ranges
    #extent1 = [yedges1[0], yedges1[-1], xedges1[-1], xedges1[0]]
    plot1 = fig.add_subplot(121)
    im1 = plot1.imshow(hist1,interpolation='nearest')
    plot1.set_ylabel(yLabel)
    plot1.set_xlabel(xLabel)
    plot1.set_title(title1)
    fig.colorbar(im1) 
    
    #set ranges
    extent2 = [yedges2[0], yedges2[-1], xedges2[-1], xedges2[0]]
    plot2 = fig.add_subplot(122)
    im2 =  plot2.imshow(hist2,interpolation='nearest')
    plot2.set_ylabel(yLabel)
    plot2.set_xlabel(xLabel)
    plot2.set_title(title2)
    fig.colorbar(im2)
    
    
    plt.show()
    
    
def dualContourPlot(Z1,Z2=[],title1="Pairs",title2="Isolated",xLabel= "Proj. Dis (Mpc) - binned",yLabel= "dv (km/s) - binned"):
    
    #create bar graphs   
    fig = plt.figure()
    
    plot1 = fig.add_subplot(121)
    plot1.contour(Z1,N=5)
    plot1.set_ylabel(yLabel)
    plot1.set_xlabel(xLabel)
    plot1.set_title(title1)  
    
    plot2 = fig.add_subplot(122)
    plot2.contour(Z2,N=5)
    plot2.set_ylabel(yLabel)
    plot2.set_xlabel(xLabel)
    plot2.set_title(title2)

        
    plt.show()


# creates two histograms from the matplotlib library funct
def dualHistogram(pairDistances,isolatedDistances,sameGraph=False,normalize = False,title1="Pairs",title2="Isolated",xLabel= "Distance",yLabel="Number",bins=15):
    
    #create bar graphs   
    fig = plt.figure()
    
    if sameGraph:
        plot1 = fig.add_subplot(111)
        pHisto = getNumPerRange(pairDistances,sampleSize=bins,upTo=True)
        iHisto = getNumPerRange(isolatedDistances,sampleSize=bins,upTo=True)
        if normalize:            
            p = plot1.scatter(pHisto.keys(),normalizeList(pHisto.values()),c='r',s=5,lw=0)
            i = plot1.scatter(iHisto.keys(),normalizeList(iHisto.values()),c='b',s=5,lw=0)
        else:
            p = plot1.scatter(pHisto.keys(),pHisto.values(),c='r',s=4,lw=0)
            i = plot1.scatter(iHisto.keys(),iHisto.values(),c='b',s=4,lw=0)
        plot1.legend([p,i],[title1,title2])
        plot1.set_ylabel(yLabel)
        plot1.set_xlabel(xLabel)
    else:
        plot1 = fig.add_subplot(211)
        plot1.set_xlim([0,max(pairDistances)])    
        plot1.hist(pairDistances, bins=bins, normed=normalize, facecolor='r')
        #plot1.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(steps=2))
        plot1.set_ylabel('Number')
        plot1.set_xlabel(xLabel)
        plot1.set_title(title1)
        
          
        
        plot2 = fig.add_subplot(212)
        plot2.set_xlim([0,max(pairDistances)])    
        plot2.hist(isolatedDistances, bins=bins, normed=normalize, facecolor='b')
        plot2.set_ylabel('Number')
        plot2.set_xlabel(xLabel)
        plot2.set_title(title2)
    
    
        
    plt.show()



#Creates two graphs that show the correlation between seperation distances and number of occurances
#needs to be called via command line because it occurs right after a long calculation 
def correlationGraphs(pairDistances,isolatedDistances,title1="Pairs",title2="Isolated",xLabel= "Distance"):
    
    #remove all bogus info from the read in lists
    pairDistances = filter(None,pairDistances)
    isolatedDistances = filter(None,isolatedDistances)
    #convert to floats
    pairDistances = list(map(float, pairDistances))
    isolatedDistances = list(map(float, isolatedDistances))
    
    #get the ordered dictionaries
    pairsNumDisCorr = getNumPerRange(pairDistances)
    isoNumDisCorr = getNumPerRange(isolatedDistances)
 
    #create bar graphs   
    fig = plt.figure()
    
    plot1 = fig.add_subplot(211)
    ind = numpy.arange(len(pairsNumDisCorr.values()))
    width=1.0
    plot1.bar(ind, pairsNumDisCorr.values(), width, color='r')
    #plot1.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(steps=2))
    plot1.set_ylabel('Number')
    plot1.set_xlabel(xLabel)
    plot1.set_title(title1)
  
      
    
    plot2 = fig.add_subplot(212)
    ind = numpy.arange(len(isoNumDisCorr.values()))
    width=1.0
    plot2.bar(ind, isoNumDisCorr.values(), width, color='b')
    plot2.set_ylabel('Number')
    plot2.set_xlabel(xLabel)
    plot2.set_title(title2)
    

        
    plt.show()

def boxWisker(pairedList,isoList,title1="Paired",title2="Isolated"):
    
    #plot both equally scaled so NORMALIZE BOTH
    pairedList= normalizeList(pairedList)
    isoList = normalizeList(isoList)
    
    fig = plt.figure()    
    
    plot1 = fig.add_subplot(211)
    plot1.boxplot(pairedList,sym='r+',vert=False)   
    plot1.set_title(title1)
    plot1.set_xlim([0,max(pairedList)])
   
    plot2 = fig.add_subplot(212)
    plot2.boxplot(isoList,sym='b+',vert=False)       
    plot2.set_title(title2)     
    plot2.set_xlim([0,max(pairedList)])
    
    
    plt.show()
    
def correlationGraphs_Line(pairDistances,isolatedDistances,title1="Counts per Distance Range",xLabel= "Distance"):
     #dynamically get the graph range params
    limit = max(pairDistances)
    totalPoints = 200    
    dSize = limit/totalPoints 
    
    #remove all bogus info from the read in lists
    pairDistances = filter(None,pairDistances)
    isolatedDistances = filter(None,isolatedDistances)
    #convert to floats
    pairDistances = list(map(float, pairDistances))
    isolatedDistances = list(map(float, isolatedDistances))
    
    #get the ordered dictionaries
    pairsNumDisCorr = getNumPerRange(pairDistances)
    isoNumDisCorr = getNumPerRange(isolatedDistances)
 
    #plot both on one graph so NORMALIZE BOTH
    pairsNumDisCorr = normalizeList(pairsNumDisCorr.values())
    isoNumDisCorr = normalizeList(isoNumDisCorr.values())    
    
    
    
    #create bar graphs   
    fig = plt.figure()
    
    plot1 = fig.add_subplot(111)
    ind = numpy.arange(len(pairsNumDisCorr))
    width=1.0
    plot1.plot(pairsNumDisCorr, color='r')
    plot1.plot(isoNumDisCorr, color='b')
    plot1.set_ylabel('Number')
    plot1.set_xlabel(xLabel)
    plot1.set_title(title1)
    plot1.set_xticks(ind+width)
    plot1.set_xticklabels([])    
    #plot1.set_xticklabels( pairsNumDisCorr.keys() )

    
    plt.show()
    
    
def plotBestFit(pairDistances,isolatedDistances,order=2,bins=30):
    
    #remove all bogus info from the read in lists
    pairDistances = filter(None,pairDistances)
    isolatedDistances = filter(None,isolatedDistances)
    #convert to floats
    pairDistances = list(map(float, pairDistances))
    isolatedDistances = list(map(float, isolatedDistances))
    
    #get the ordered dictionaries
    pairsNumDisCorr = getNumPerRange(pairDistances,sampleSize=bins,upTo=True)
    isoNumDisCorr = getNumPerRange(isolatedDistances,sampleSize=bins,upTo=True)
    
    
    fig = plt.figure()
    
    plot1 = fig.add_subplot(211)
    plot2 = fig.add_subplot(212)
    
    x1 = numpy.linspace(0, len(pairsNumDisCorr), len(pairsNumDisCorr))
    x2 = numpy.linspace(0, len(isoNumDisCorr), len(isoNumDisCorr))
    
    bestFitEq1 = numpy.polyfit(x1, pairsNumDisCorr.values(), order)
    bestFitEq2 = numpy.polyfit(x2, isoNumDisCorr.values(), order)
    
    func1 = numpy.poly1d(bestFitEq1)    
    func2 = numpy.poly1d(bestFitEq2)
    
    
        
    y1 = func1(x1)
    y2 = func2(x2)
    
    
    #plot vertical line where the graph is maximum
    maxpos1 = y1.argmax()
    maxpos1 = x1[maxpos1]
    #print maxpos1
    plot1 = verticalLine(plot1,maxpos1,linecolor='r')    
    
    maxpos2 = y2.argmax()
    maxpos2 = x2[maxpos2]    
    plot2 = verticalLine(plot2,maxpos2,linecolor='b')    
    
    
    
    plot1.plot(x1, y1, color='r')
    plot2.plot(x2, y2, color='b')
    
    plt.show()

def ProjectionPlot(list1=None,list2 = True,list3=False,title='Map'):
    
    if list1 is None:
        list1 = SurveyParserCSV.parse()
        
    if type(list2) == bool:
        if list2:
            list2 = SurveyParserCSV.parse()
        #else do nothing
    #else use it
    if type(list3) == bool:
        if list3:
            list3 = SurveyParserCSV.parse()
   
    RAs = []
    DECs = [] 
    RAs2 = []
    DECs2 = []
    RAs3 = []
    DECs3 = []
    
    
    for each in list1:
        RA = float(each.RA)
        DEC = float(each.DEC)
        
        if DEC >180.0:
            DEC = DEC-360.0
            
        #RA = toRad(RA)
        #DEC = toRad(DEC)
        
        RAs.append(RA)
        DECs.append(DEC)
    
    if type(list2) is not bool:
        
       
        for each in list2:
            RA = float(each.RA)
            DEC = float(each.DEC)
            
            if DEC >180.0:
                DEC = DEC-360.0
                
            #RA = toRad(RA)
            #DEC = toRad(DEC)
            
            RAs2.append(RA)
            DECs2.append(DEC)    

    if type(list3) is not bool:
        
        for each in list3:
            RA = float(each.RA)
            DEC = float(each.DEC)
            
            if DEC >180.0:
                DEC = DEC-360.0
                
            #RA = toRad(RA)
            #DEC = toRad(DEC)
            
            RAs3.append(RA)
            DECs3.append(DEC)    
    
    fig = plt.figure()
    plot1 = fig.add_subplot(111,projection=None)
    pairs = plot1.scatter(RAs,DECs,color='r',s=10)
    #plot1.set_ylim(-0.4,1.4)
    plot1.set_ylabel("DEC")
    plot1.set_xlabel("RA")
    if len(RAs2) > 0: #then we have secondary points
        isolated = plot1.scatter(RAs2,DECs2,color='b',s=1)
    if len(RAs3) > 0: #then we have third points
        clusters = plot1.scatter(RAs3,DECs3,color='g',s=0.5)
        lnd =  plot1.legend([pairs,isolated,clusters],['Pairs','Isolated','Clusters'])
        lnd.draggable(True)
        
    saveGraph(fig,'results/survey.png')
    plt.show()

    
    
def verticalLine(myplot,x,linecolor='r'):
    #print myplot.get_ylim
    line = matplotlib.lines.Line2D([x,x],[myplot.get_ylim()[0],myplot.get_ylim()[1]],color=linecolor)
    myplot.add_line(line)
    return myplot
    
def saveGraph(figure,name,l=30,w=20):
    try:
        if name.rindex(".") < len(name)-4:
            raise Exception
    except:
        name=name+".png"
    #print "Saving as:  "+name
    figure.set_size_inches(l, w)
    try:
        figure.savefig(name)
    except Exception as e:
        print e
        print "Could not save image but moving on"
        
        
        
        
#if  __name__ =='__main__':parsePoints(returnValues=False)