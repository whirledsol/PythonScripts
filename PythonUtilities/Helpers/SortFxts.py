# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 17:37:29 2013

@author: Will
"""
import Helpers.Models.SkyObjects


def sort_RA(list):
    try: import operator
    except ImportError:
        #print("using lambda")
        RAsorter= lambda x: (x.RA, x.DEC) # use a lambda if no operator module
    else:
        #print("using attrgetter")
        RAsorter= operator.attrgetter("RA") # use operator since it's faster than lambda
        
    list.sort(key=RAsorter, reverse=False)
    return list     

def sort_DEC(list):
    try: import operator
    except ImportError:
        #print("using lambda")
        RAsorter= lambda x: (x.DEC) # use a lambda if no operator module
    else:
        #print("using attrgetter")
        RAsorter= operator.attrgetter("DEC") # use operator since it's faster than lambda
        
    list.sort(key=RAsorter, reverse=False)
    return list 

def sort_Z(list):
    try: import operator
    except ImportError:
        #print("using lambda")
        RAsorter= lambda x: (x.z) # use a lambda if no operator module
    else:
        #print("using attrgetter")
        RAsorter= operator.attrgetter("z","RA") # use operator since it's faster than lambda
        
    list.sort(key=RAsorter, reverse=False)
    return list 