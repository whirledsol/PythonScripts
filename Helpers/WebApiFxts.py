'''
WebFxts
@author Will Rhodes
'''
import 



def authorize(h,s,v):
    '''
    converts hsv to rgb hex
    '''
    rgb = colorsys.hsv_to_rgb(h/360.,s/100.,v/100.)
    rgb = [round(x*255.) for x in rgb]
    return getColorCodeRGB(*rgb)

