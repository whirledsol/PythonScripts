#!/usr/bin/env python3
"""
covid-sim.py
Created:
@author: Will Rhodes

"""
import argparse,re,os,csv,datetime,numpy,warnings,matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from scipy.optimize import OptimizeWarning,fsolve
import matplotlib.dates as mdates

warnings.simplefilter("ignore", OptimizeWarning)
COUNTRY_POPULATIONS = {"China":1433783686, "US":329064917, "Japan":126860301, "United Kingdom":67530172, "Italy":60550075, "Canada":37411047}
COUNTRY_COLORS =  {'China':'orange','US':'blue','Japan':'yellow','United Kingdom':'purple', 'Italy':'green', 'Canada':'red'}
STATE_POPULATIONS = {"California":39512223,"Texas":28995881,"Florida":21477737,"New York":19453561,"Pennsylvania":12801989,"Illinois":12671821,"Ohio":11689100,"Georgia":10617423,"North Carolina":10488084,"Michigan":9986857,"New Jersey":8882190,"Virginia":8535519,"Washington":7614893,"Arizona":7278717,"Massachusetts":6949503,"Tennessee":6833174,"Indiana":6732219,"Missouri":6137428,"Maryland":6045680,"Wisconsin":5822434,"Colorado":5758736,"Minnesota":5639632,"South Carolina":5148714,"Alabama":4903185,"Louisiana":4648794,"Kentucky":4467673,"Oregon":4217737,"Oklahoma":3956971,"Connecticut":3565287,"Utah":3205958,"Puerto Rico":3193694,"Iowa":3155070,"Nevada":3080156,"Arkansas":3017825,"Mississippi":2976149,"Kansas":2913314,"New Mexico":2096829,"Nebraska":1934408,"West Virginia":1792065,"Idaho":1787147,"Hawaii":1415872,"New Hampshire":1359711,"Maine":1344212,"Montana":1068778,"Rhode Island":1059361,"Delaware":973764,"South Dakota":884659,"North Dakota":762062,"Alaska":731545,"District of Columbia":705749,"Vermont":623989,"Wyoming":578759}

logistic = lambda x,l,k,o: l / (1 + numpy.exp(k*(o-x)))

expo = lambda x,a,b: a* numpy.exp(b*x)

FORMULAE = {
    logistic:'$y=\\frac{{{0:.3f}}}{{1+e^{{{1:.3f}({2:.3f}-x)}}}}$',
    expo:'$y={0:.3f}e^{{{1:.3f}x}}$'
}

plot_months = mdates.MonthLocator()   # every year
plot_days = mdates.DayLocator()  

def start():
    PATH_BASE = '/home/will/Projects/COVID-19/csse_covid_19_data/csse_covid_19_time_series'
    OUTPUT_BASE = '/home/will/Projects/PythonUtilities/covid-sim/out/'
    PATH_TIME_CONFIRMED = os.path.join(PATH_BASE,'time_series_19-covid-Confirmed.csv')

    duration = 90
    important_states = ['New York','New Jersey','Pennsylvania']
    func = logistic
    bounds=([0.03,-1,5], [0.90,1,duration])

    custom_StatesNew(PATH_TIME_CONFIRMED,important_states)
    custom_StatesPerMap(PATH_TIME_CONFIRMED)
    custom_CountriesPerZero(PATH_TIME_CONFIRMED)

    custom_StatesFitMap(PATH_TIME_CONFIRMED,OUTPUT_BASE, important_states,expo)

    custom_StatesExtrapolate(PATH_TIME_CONFIRMED,important_states,duration,func,bounds)
    

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

def custom_StatesNew(path,check_states=[],min_cases=0):
    '''
    Shows the increase in cases since previous day for various states over time
    '''
    _, ax = plt.subplots()
    for state in check_states:
        _,y = parse_time(path,province=state)
        y = [v-y[i-1] for i, v in enumerate(y) if v>min_cases and i>min_cases]
        x = range(len(y))
        ax.plot(x,y,c=numpy.random.rand(3,),label=state)
    
    ax.set_xlabel('Days since at least {} cases in that state'.format(min_cases))
    ax.set_ylabel('New Cases since Previous Day')
    ax.set_title('New Cases Per Day for Various States')
    ax.legend()
    plt.show()       

def custom_StatesPerMap(path):
    '''
    Shows percent of state affected on map. Redder is bad.
    '''
    states = {}
    for state,population in STATE_POPULATIONS.items():
        _,y = parse_time(path,province=state)
        y = [i/population*100. for i in y if i>0]
        states[state] = max(y) if len(y) > 0 else 0
    us_map(states,'Percentage of State Population Infected',formatter='{0:.3f}%')

def custom_StatesFitMap(path,OUTPUT_BASE,check_states=[],func=expo,min_days=3):
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
                #print(state)
                x = range(len(y)) #create days
                try:
                    params,_ = curve_fit(func, x, y)
                    states[state] = params[1]

                    if(state in check_states):
                        graph_fit(x,y,func,'{} Case Growth'.format(state))
                    f.write('{},{},{}\n'.format(state,*params))
                except:
                    raise ValueError('Could not find best fit for {}'.format(state))

    us_map(states,'Case Growth')


def custom_CountriesPerZero(path,func=expo,min_cases=100):
    '''
    Shows cases over time starting the day at least min_cases were hit for each country
    '''
    _, ax = plt.subplots()
    
    for country,population in COUNTRY_POPULATIONS.items():
        _,y = parse_time(path,country=country)
        y = [i/population*100. for i in y if i>min_cases]
        x = range(len(y))
        _,formula = best_fit(x,y,func,label=country)
        label = '{}  {}'.format(country,formula)
        ax.plot(x, y, c=COUNTRY_COLORS[country],label=label)

    ax.set_xlabel('Days since at least {} cases in that country'.format(min_cases))
    ax.set_ylabel('% Population Infected')
    ax.set_title('Percent of Country Infected After {} Cases'.format(min_cases))
    ax.legend()
    plt.show()


def custom_StatesExtrapolate(path,important_states,duration = 90,func=logistic, bounds=None):
    '''
    Extrapolates the current data to fit func
    '''
    _, ax = plt.subplots()
    for i,state in enumerate(important_states):
        x,y = parse_time(path,province=state)
        y = [i/STATE_POPULATIONS[state]*100. for i in y if i>0]
        xd = x[-len(y):]
        x = range(len(y))
        ax.plot(xd,y,c=numpy.random.rand(3,),label=state,linewidth=3)

        params,formula = best_fit(x,y,func,bounds,state)
        
        xd = get_date_range(xd[0],duration)
        x = range(duration)
        y = func(x,*params)
        
        y = [i for i in y if i<=100]
        x = x[0:len(y)]
        xd = xd[0:len(y)]

        ax.plot(xd,y,c=numpy.random.rand(3,),label=formula,dashes=[6, 2],linewidth=1)

        ax.legend()
        
        ax.set_xlabel('Date')
        plt.xticks(rotation=30)
        ax.xaxis.set_major_locator(plot_months)
        ax.xaxis.set_minor_locator(plot_days)
        
        ax.set_ylabel('% of Population Infected')
        ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:.3f}'))
        
        ax.set_title('Extrapolation of Cases in Various States')
    plt.show()
















def parse_time(path,country='',province=''):
    '''
    parse a time series file from the COVID-19 repo
    '''
    with open(path, 'r') as f:
        index_first_date = 2
        header = f.readline()
        date_start = header.split(',')[index_first_date]
        days = len(header.split(','))-index_first_date
        #print('parsing {} days worth of data'.format(days))

        x = get_date_range(date_start,len(header.split(','))-4)
        y = list(numpy.zeros(days))

        reader = csv.reader(f, delimiter=",")
        for _, row in enumerate(reader):
            index_match = 0 if province != '' else 1
            location = province if province != '' else country
            if(row[index_match] == location):
                new = row[index_first_date:]
                try:
                    y = [int(a or '0') + int(b or '0') for a,b in zip(y, new)]
                except:
                    print(new)
                    raise ValueError('Could not parse values')
        return x,y


def get_date_range(date_start,length):
    '''
    creates an array of dates
    '''
    base = date_start if isinstance(date_start, datetime.date) else datetime.datetime.strptime(date_start,'%m/%d/%Y')
    return [base + datetime.timedelta(days=x) for x in range(length)]


def best_fit(x,y,func=expo,bounds=None,label='dat data'):
    '''
    attempt to find the best fit params and formula
    '''
    try:
        params,_ = curve_fit(func, x, y, maxfev=5000, bounds = bounds)
        formula = FORMULAE[func].format(*params)
        return params,formula
    except:
        print('Could not find a curve for {}'.format(label))
        return [],''

def graph_fit(x,y,func,title=''):
    '''
    Show the data and best fit curve (using func) and formula too!
    '''
    
    params,formula = best_fit(x,y,func,label=title)
    if(len(params) == 0): return

    _, ax = plt.subplots()
    ax.plot(x,y,c='red',linewidth=2)
    ax.plot(x,func(x,*params),c='blue',linewidth=1)
    formula = FORMULAE[func].format(*params)
    ax.text(0, max(y), formula) 

    ax.set_xlabel('Days with Cases')
    ax.set_ylabel('Number of Confirmed Cases')
    ax.set_title(title)
    plt.show()

def us_map(states,title = '',text_top=5,formatter = '{0:.3f}'):
    '''
    show a us map with state color highlighting
    '''
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

    #find the min value that we will display text values for
    text_top = min(text_top,len(states.values()))
    text_threshold = list(states.values())
    text_threshold.sort()
    text_threshold = min(text_threshold[-text_top:])

    for state in shpreader.Reader(states_shp).records():

        edgecolor = 'black'

        try:
            value = states[state.attributes['name']]
        except:
            value = mn

        facecolor = cmap(value,mn,mx)
            

        # `state.geometry` is the polygon to plot
        ax.add_geometries([state.geometry], ccrs.PlateCarree(),
                        facecolor=facecolor, edgecolor=edgecolor)

        #add text if value is over threshold
        if value >= text_threshold:
            x = state.geometry.centroid.x        
            y = state.geometry.centroid.y
            ax.text(x, y, formatter.format(value),size=7, color='blue', ha='center', va='center', transform=ccrs.PlateCarree())   
            
    plt.show()


def cmap(value,mn,mx):
    value = numpy.abs(value)
    mn = numpy.abs(mn)
    mx = numpy.abs(mx)
    bg = 1-((value-mn)/(mx-mn)) #pow(scale,1-normalized)/scale
    return [1,bg,bg]



if  __name__ =='__main__':start()