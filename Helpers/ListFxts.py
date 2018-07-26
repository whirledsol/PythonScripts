# -*- coding: utf-8 -*-
'''
List Functions
Created on Sun Jul 07 14:23:47 2013
@author: Will Rhodes
'''

import math,operator
from collections import OrderedDict
import itertools

def convertAllToFloat(lst):
    '''
    utility method that can convert all in list to float without throwing exceptions
    '''
    fltLst = []
    if type(lst) == list:
        for each in lst:
            each.strip('\n\t\s')
            try:
                fltLst.append(float(each))
            except:
                print("problem with ",each)
        return fltLst
    else:
        print(lst,' is not a list')
        return lst
      
def chunks(l, n):
    '''
    splits a list, l, into a list of lists with each sublist of size n  
    '''
    newList = []
    
    for i in range(0, len(l), n):
        newList.append(l[i:i+n])
    return newList
        
def getNumPerRange(tempList,sampleSize = 50,dSize = None,upTo=False,returnList=False):
    '''
    gets the number of items in a list within the range 0-> limit in dSize chunks
    returns: dictionary with x labels and y count
    '''
    if dSize is None:
        limit = max(tempList) 
        dSize = limit/sampleSize
    else:
        limit = sampleSize*dSize
        
    upperBound = dSize 
    lowerBound = upperBound - dSize
    returning = OrderedDict()
    while upperBound <= limit:
        tag = upperBound#+"-"+str(upperBound-0.001)+"..."
        if upTo:
            returning[tag] = sum(1 for item in tempList if (item<upperBound))
        else:
            returning[tag] = sum(1 for item in tempList if ((item<upperBound) and (item>= lowerBound)))
        upperBound = upperBound+dSize
        lowerBound = lowerBound+dSize
    if returnList:
        return list(returning.values())
    return returning

def partitionByAttributeSize(mylist,attribute,dSize,maxVal=None):
    '''
    sorts a list by dynamic attribute name and parttions into dSize chunks
    '''
    try:    
        getattr(mylist[0], attribute)
    except:
        print("Object does not have attribute, try again")
        return None
    dSize = float(dSize)
    # sort first
    mylist.sort(key=operator.attrgetter(attribute), reverse=False)
    
    returning = []
    
    if maxVal is None:
        maxVal = float(max([getattr(each, attribute) for each in mylist]))
        
    maxIndex = int(math.ceil(maxVal/dSize))
    print(maxIndex)    
    for count in range(maxIndex):
        returning.append([])

    for each in mylist:
        indexPlacement = int(math.ceil((float(getattr(each, attribute))/maxVal)*float(maxIndex)))-1
        returning[indexPlacement].append(each)
    return returning  
         
def getNumPerRange_v2(keys,tempList,upTo=False,returnList=True):
    '''
    gets the number of items in a list within the range 0-> limit in dSize chunks
    returns: dictionary with x labels and y count
    '''
    returning = OrderedDict()
    for i in range(1,len(keys)):
        temp = []
        for each in tempList:
            if upTo:
                if each <=keys[i]:
                    temp.append(each)
            else:
                if each >= keys[i-1] and each < keys[i]:
                    temp.append(each)
        
        returning[keys[i]] = len(temp)            
        
    if returnList:
        return list(returning.values())
    else:
        return returning
       
def averageCorroIndices(listoflists):
    '''
    Average Corropsonding Indices
    Get the averages across multiple lists where they have the same index
    e.g.: [[3,4],[5,6]] yields [4,5]
    assumption: each sublist is of the same size 
    '''
    if type(listoflists[0]) != list:
        print("Not a list of lists")
        return None
    size = len(listoflists)
    subListSize = len(listoflists[0])
    returning = []
    
    
    for j in range(subListSize):
        temp = 0
        for each in listoflists:
            temp+=each[j]
        returning.append(temp)
    
    returning = [x/size for x in returning]
    return returning
        
def flatten(lst):
    '''
    takes a list of lists and makes it one list
    '''
    #print lst
    return list(itertools.chain.from_iterable(lst))      

def subtractLists(major,minor):
    '''
    subtracts elements from the minor list
    from the major list and returns the listed result
    '''
    subtracted = []
    if len(minor)==0:
        return major
    if len(major) == 0:
        return None
        
    if type(minor[0]) == list:
        minor = list(itertools.chain.from_iterable(minor)) #FLATTEN THE LIST
        
    for each in major:
        if getIndex(minor,each) <0: #each major is NOT in minor
            subtracted.append(each)
    return subtracted
        
def first(iterable, default=None):
    '''
    returns the first item in a list or itterable
    '''
    for item in iterable:
        return item
    return default

def getIndex(mylist,obj):
    '''
    similar to list.index(item) but without the error, just returns -1
    '''
    try:
        idx = mylist.index(obj)
        return idx
    except Exception as e:
        #print e
        return -1

def is_sorted(lst):
    '''
    tests to see if the list is sorted numerically
    '''
    it = iter(lst)
    try:
        prev = next(it)
    except StopIteration:
        return True
    for x in it:
        if prev > x:
            return False
        prev = x
    return True 

def normalizeList(myList):
    '''
    normalizes a list of numbers
    '''
    try:
        maxval = max(myList)
        return [float(x)/float(maxval) for x in myList]
    except:
        print("Can't normalize this list")
        return []

def distinct(l):
    '''
    returns a list of distinct items
    '''
    return list(set(l))