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

def start():
    PATH_BASE = '/home/will/Projects/COVID-19/csse_covid_19_data/csse_covid_19_time_series'
    PATH_TIME_CONFIRMED = 'time_series_19-covid-Confirmed.csv'

    #custom_StatevsUSPer(os.path.join(PATH_BASE,PATH_TIME_CONFIRMED))
    custom_CountriesPer(os.path.join(PATH_BASE,PATH_TIME_CONFIRMED))


def custom_StatevsUSPer(path,state='Pennsylvania'):
    '''
    Shows percent of state vs percent of US over time
    '''
    fig, ax = plt.subplots()

    x1,y1 = parse_time(path,province=state)
    y1 = [i/12801989 for i in y1]

    x2,y2 = parse_time(path,country='US')
    y2 = [i/328239523 for i in y2]
    
    graph_time(ax,x1,y1,'PA','tab:purple')
    graph_time(ax,x2,y2,'US','tab:blue')
    ax.legend()
    #ax.set_yscale('log')
    plt.show()

def custom_Countries(path):
    '''
    Shows simple cases in country over time
    '''
    fig, ax = plt.subplots()

    x1,y1 = parse_time(path,country='Italy')
    x2,y2 = parse_time(path,country='US')

    graph_time(ax,x1,y1,'Italy','tab:green')
    graph_time(ax,x2,y2,'US','tab:blue')
    ax.legend()
    plt.show()


def custom_CountriesPer(path):
    '''
    Shows percent of country population affected over time
    '''
    fig, ax = plt.subplots()

    x0,y0 = parse_time(path,country='China')
    y0 = [i/1427647786. for i in y0]

    x1,y1 = parse_time(path,country='Italy')
    y1 = [i/60317546. for i in y1]

    x2,y2 = parse_time(path,country='US')
    y2 = [i/328239523 for i in y2]

    x3,y3 = parse_time(path,province='Hubei')
    y3 = [i/58500000. for i in y3]

    graph_time(ax,x0,y0,'China','red')
    graph_time(ax,x1,y1,'Italy','green')
    graph_time(ax,x2,y2,'US','blue')
    graph_time(ax,x3,y3,'Hubei','yellow')

    ax.set_xlabel('Date')
    ax.set_ylabel('Percent of Population Infected')
    ax.set_title('Percent Infected Per Country')
    ax.legend()
    plt.show()


def custom_CountriesZero(path,min_cases=100):
    '''
    Shows cases over time starting the day at least min_cases were hit for each country
    '''
    _, ax = plt.subplots()
    countries = ['China','Italy','US','Iran']
    colors = ['red','green','blue','yellow']
    
    ys = []
    for country in countries:
        _,y = parse_time(path,country=country)
        y = [i for i in y if i>min_cases]
        ys.append(y)
    
    for i,y in enumerate(ys):
        x = range(len(y))
        ax.plot(x, y, c=colors[i],label=countries[i])

    ax.set_xlabel('Days since at least {} cases'.format(min_cases))
    ax.set_ylabel('Number of Confirmed Cases')
    ax.set_title('Cases Per Country')
    ax.legend()
    plt.show()


def parse_time(path,country='',province=''):
    
    with open(path, 'r') as f:
        header = f.readline()
        date_start = header.split(',')[4]
        days = len(header.split(','))-4
        print('parsing {} days worth of data'.format(days))

        x = get_date_range(date_start,len(header.split(','))-4)
        y = list(numpy.zeros(days))
        for line in f:
            row = line.replace('\n','').split(',')
            index_match = 0 if province != '' else 1
            location = province if province != '' else country
            if(row[index_match] == location):
                new = row[4:]
                y = [int(a) + int(b) for a,b in zip(y, new)]
        #print(y)
        return x,y


def get_date_range(date_start,length):
    base = datetime.datetime.strptime(date_start,'%m/%d/%y')
    return [base + datetime.timedelta(days=x) for x in range(length)]

def graph_time(ax,x,y,label,color):
    ax.plot(x, y, c=color,label=label,alpha=0.7)



if  __name__ =='__main__':start()