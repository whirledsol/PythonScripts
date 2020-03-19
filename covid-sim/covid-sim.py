#!/usr/bin/env python3
"""
covid-sim.py
Created:
@author: Will Rhodes

"""
import argparse
import re,os,csv
import datetime
import numpy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import warnings
from scipy.optimize import OptimizeWarning

warnings.simplefilter("ignore", OptimizeWarning)
STATE_POPULATIONS = {"California":39512223,"Texas":28995881,"Florida":21477737,"New York":19453561,"Pennsylvania":12801989,"Illinois":12671821,"Ohio":11689100,"Georgia":10617423,"North Carolina":10488084,"Michigan":9986857,"New Jersey":8882190,"Virginia":8535519,"Washington":7614893,"Arizona":7278717,"Massachusetts":6949503,"Tennessee":6833174,"Indiana":6732219,"Missouri":6137428,"Maryland":6045680,"Wisconsin":5822434,"Colorado":5758736,"Minnesota":5639632,"South Carolina":5148714,"Alabama":4903185,"Louisiana":4648794,"Kentucky":4467673,"Oregon":4217737,"Oklahoma":3956971,"Connecticut":3565287,"Utah":3205958,"Puerto Rico":3193694,"Iowa":3155070,"Nevada":3080156,"Arkansas":3017825,"Mississippi":2976149,"Kansas":2913314,"New Mexico":2096829,"Nebraska":1934408,"West Virginia":1792065,"Idaho":1787147,"Hawaii":1415872,"New Hampshire":1359711,"Maine":1344212,"Montana":1068778,"Rhode Island":1059361,"Delaware":973764,"South Dakota":884659,"North Dakota":762062,"Alaska":731545,"District of Columbia":705749,"Vermont":623989,"Wyoming":578759}

def logistic(x,l,k,o):
    return l / (1 + numpy.exp(k*(o-x)))

def expo(x,a,b):
    return a*numpy.exp(b*x)

def cmap(value,mn,mx):
    value = numpy.abs(value)
    mn = numpy.abs(mn)
    mx = numpy.abs(mx)
    bg = 1-((value-mn)/(mx-mn)) #pow(scale,1-normalized)/scale
    return [1,bg,bg]

def start():
    PATH_BASE = '/home/will/Projects/COVID-19/csse_covid_19_data/csse_covid_19_time_series'
    OUTPUT_BASE = '/home/will/Projects/PythonUtilities/covid-sim/out/'
    PATH_TIME_CONFIRMED = os.path.join(PATH_BASE,'time_series_19-covid-Confirmed.csv')
    PATH_TIME_RECOVERY = os.path.join(PATH_BASE,'time_series_19-covid-Recovered.csv')
    custom_StatesPer(PATH_TIME_CONFIRMED)
    custom_UsaRecovery(PATH_TIME_CONFIRMED,PATH_TIME_RECOVERY)
    custom_CountriesZero(PATH_TIME_CONFIRMED)
    custom_StatesPerMap(PATH_TIME_CONFIRMED)
    custom_StatesFitMap(PATH_TIME_CONFIRMED,OUTPUT_BASE,check_states='Pennsylvania,New Jersey')

def custom_StatesPer(path,highlight='Pennsylvania'):
    '''
    Shows percent of state vs percent of US over time
    '''
    _, ax = plt.subplots()

    for state,population in STATE_POPULATIONS.items():
        x,y = parse_time(path,province=state)
        y = [i/population for i in y]
        linewidth = 3 if highlight == state else 1
        ax.plot(x,y,label=state,c=numpy.random.rand(3,),linewidth=linewidth)
    #ax.legend()
    plt.show()


def custom_UsaRecovery(path,recoverypath):
    '''
    Shows percent of state vs percent of US over time
    '''
    _, ax = plt.subplots()
    
    x,y = parse_time(path,country='US')
    rx,ry = parse_time(recoverypath,country='US')

    date_first = x[y.index([i for i in y if i>0][0])]
    ry = ry[rx.index(date_first):]
    y = [i for i in y if i>0]
    x = [i for i in x if i>=date_first]
    
    ax.set_title('US Cases and Recovery')
    ax.set_xlabel('Date')
    ax.set_ylabel('Incidents (Log Scale)')
    ax.plot(x,y,label='Cases',c=numpy.random.rand(3,),linewidth=2)
    ax.plot(x,ry,label='Recovery',c=numpy.random.rand(3,),linewidth=1)
    ax.legend()
    ax.set_yscale('log')
    plt.show()

def custom_StatesPerMap(path):
    '''
    Shows percent of state affected on map. Redder is bad.
    '''
    states = {}
    for state,population in STATE_POPULATIONS.items():
        _,y = parse_time(path,province=state)
        y = [i/population for i in y if i>0]
        states[state] = max(y) if len(y) > 0 else 0
    us_map(states,'Percentage of State Population Infected')

def custom_StatesFitMap(path,OUTPUT_BASE, func=expo,min_days=3,check_states=''):
    '''
    Fits data to curve, saves the best fit, displays base on map. Redder means high rate.
    '''
    states = {}
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    outpath = os.path.join(OUTPUT_BASE,'states_bestfit_{}.csv'.format(timestamp))

    with open(outpath,'w') as f:
        for state,_ in list(STATE_POPULATIONS.items()):
            _,y = parse_time(path,province=state)
            y = [i for i in y if i>0]
            if(len(y)>3): #we need >3 days worth of data
                print(state)
                x = range(len(y)) #create days
                try:
                    params,_ = curve_fit(func, x, y)
                    states[state] = params[1]

                    if(state in check_states.split(',')):
                        _, ax = plt.subplots()
                        ax.plot(x,y,c='red',linewidth=2)
                        ax.plot(x,func(x,*params),c='blue',linewidth=1)
                        ax.text(0, max(y), '$y={0:.3f}e^{{{1:.3f}x}}$'.format(*params)) 
                        ax.set_xlabel('Days with Cases')
                        ax.set_ylabel('Number of Confirmed Cases')
                        ax.set_title('{} Cases'.format(state))
                    f.write('{},{},{}\n'.format(state,*params))
                except:
                    raise ValueError('Could not find best fit for {}'.format(state))

    us_map(states,'Case Growth (Expotential Base)')



def custom_CountriesZero(path,min_cases=100):
    '''
    Shows cases over time starting the day at least min_cases were hit for each country
    '''
    _, ax = plt.subplots()
    countries = ['China','Italy','US','Iran','Spain']
    colors = ['red','green','blue','brown','yellow']
    
    ys = []
    for country in countries:
        _,y = parse_time(path,country=country)
        y = [i for i in y if i>min_cases]
        ys.append(y)
    
    for i,y in enumerate(ys):
        x = range(len(y))
        ax.plot(x, y, c=colors[i],label=countries[i])

    ax.set_xlabel('Days since at least {} cases in that country'.format(min_cases))
    ax.set_ylabel('Number of Confirmed Cases')
    ax.set_title('Cases Per Country from >{} Cases'.format(min_cases))
    ax.legend()
    plt.show()


def parse_time(path,country='',province=''):
    
    with open(path, 'r') as f:
        header = f.readline()
        date_start = header.split(',')[4]
        days = len(header.split(','))-4
        #print('parsing {} days worth of data'.format(days))

        x = get_date_range(date_start,len(header.split(','))-4)
        y = list(numpy.zeros(days))
        for line in f:
            row = line.replace('\n','').split(',')
            index_match = 0 if province != '' else 1
            location = province if province != '' else country
            if(row[index_match] == location):
                new = row[4:]
                y = [int(a) + int(b) for a,b in zip(y, new)]
        return x,y


def get_date_range(date_start,length):
    base = datetime.datetime.strptime(date_start,'%m/%d/%y')
    return [base + datetime.timedelta(days=x) for x in range(length)]

def us_map(states,title = ''):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())

    ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

    shapename = 'admin_1_states_provinces_lakes_shp'
    states_shp = shpreader.natural_earth(resolution='110m',category='cultural', name=shapename)

    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(False)
    ax.set_title(title)
    mn = min(states.values())
    mx = max(states.values())
    for state in shpreader.Reader(states_shp).records():

        edgecolor = 'black'

        try:
            value = states[state.attributes['name']]
        except:
            value = mn

        facecolor = cmap(value,mn,mx)
            

        # `astate.geometry` is the polygon to plot
        ax.add_geometries([state.geometry], ccrs.PlateCarree(),
                        facecolor=facecolor, edgecolor=edgecolor)

    plt.show()

if  __name__ =='__main__':start()