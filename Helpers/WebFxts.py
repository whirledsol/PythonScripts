'''
WebFxts
@author Will Rhodes
'''
import colorsys
import math



def getColorCodeHSV(h,s,v):
    '''
    converts hsv to rgb hex
    '''
    rgb = colorsys.hsv_to_rgb(h/360.,s/100.,v/100.)
    rgb = [round(x*255.) for x in rgb]
    return getColorCodeRGB(*rgb)

def getColorCodeRGB(r,g,b):
    '''
    converts rgb to hex
    '''
    r = int(round(r))
    g = int(round(g))
    b = int(round(b))
    
    return "#{:02x}{:02x}{:02x}".format(r,g,b)
