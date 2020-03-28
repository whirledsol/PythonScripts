#!/usr/bin/env python3


'''

'''

import datetime, os,csv,re 

def runETL(datum='Confirmed'):
    '''
    Takes day files and adds them to the legacy files
    '''

    OUTPUT_PATH = '../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-{}.csv'.format(datum)
    DAILY_DIR = '../../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
    
    lastDate = getLatestFileDate(DAILY_DIR)
    
    seriesData = {}

    length = 0
    for i in range(0,365):
        date = lastDate - datetime.timedelta(days=i)
        dayData = parseDayData(DAILY_DIR,date,datum)
        length = i
        if dayData is None: 
            print('Stopped at the day prior to {} because this file did not exist.'.format(date.strftime('%m-%d-%Y')))
            break
        if seriesData == {}:
            seriesData = dayData
        else:
            for key in seriesData.keys():
                next_value = dayData[key] if key in dayData else [0]
                seriesData[key] = seriesData[key] + next_value
        
    daterange = [d.strftime('%m/%d/%Y') for d in get_date_range(lastDate,length,-1)]
    writeSeriesData(OUTPUT_PATH,daterange,seriesData)

def getLatestFileDate(DAILY_DIR):
    files = os.listdir(DAILY_DIR)
    regex = re.compile(r'\d{2}-\d{2}-\d{4}\.csv')
    datefiles = list(filter(regex.search, files))
    dates = [datetime.datetime.strptime(d[:-4],'%m-%d-%Y') for d in datefiles]
    return max(dates)

def getPath(DAILY_DIR,date):
    return os.path.join(DAILY_DIR,date.strftime('%m-%d-%Y')+'.csv')

def parseDayData(DAILY_DIR,date,datum):
    '''
    parses a day file into a dictionary of
    {'State|Country':0}
    '''

    path = getPath(DAILY_DIR,date)
    if not os.path.isfile(path):
        return None

    data = {}
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=",")
        for i, row in enumerate(reader):
            if i==0: continue
            index_map = {'State':2,'Country':3,'Confirmed':7,'Deaths':8,'Recovered':9}
            if len(row) <= 8:
                index_map = {'State':0,'Country':1,'Confirmed':3,'Deaths':4,'Recovered':5}

            key = '{}|{}'.format(row[index_map['State']],row[index_map['Country']])
            try:
                value = int(row[index_map[datum]] or '0')
                data[key] = [value + data[key][0] if key in data else value]
            except:
                print(row)
                raise Exception('bad data')

        #print(list(data.items())[0:40])
        return data


def writeSeriesData(OUTPUT_PATH,dates,seriesData):
    '''
    Writes the series data to OUTPUT_PATH
    '''
    with open(OUTPUT_PATH, 'w') as f:
        writer = csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        dates = list(reversed(dates))
        writer.writerow(['State','Country'] + dates)
        for key,values in seriesData.items():
            state = key.split('|')[0]
            country = key.split('|')[1]
            values = list(reversed([str(v) for v in values]))
            writer.writerow([state,country] + values)

def days_between(d1, d2):
    '''
    gets the diff between two days
    '''
    #print('{} {}'.format(type(d2),type(d1)))
    return abs((d2 - d1).days)

def get_date_range(date_start,length,direction=1):
    '''
    creates an array of dates
    '''
    base = date_start if isinstance(date_start, datetime.date) else datetime.datetime.strptime(date_start,'%m/%d/%y')
    return [base + datetime.timedelta(days=x*direction) for x in range(length)]

if  __name__ =='__main__':runETL()