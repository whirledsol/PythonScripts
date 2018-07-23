'''
WebFxts
@author Will Rhodes
'''
import colorsys

def getColorCodeHSV(h,s,v):
    '''
    converts hsv to rgb hex
    '''
    rgb = colorsys.hsv_to_rgb(359,100,100)
    return getColorCodeRGB(*rgb)

def getColorCodeRGB(r,g,b):
    '''
    converts rgb to hex
    '''
    return '#%02x%02x%02x' % (r,g,b)