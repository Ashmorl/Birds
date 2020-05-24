# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:18:39 2020

@author: Tove
"""

from  numpy import *
from  matplotlib.pyplot import *
import pandas as pd
import matplotlib.dates as dates


##############################
# A Mock Dataset for Testing
##############################

# Create a mock dataset 
# use a pandas dataframe for this 

data_test = pd.DataFrame([['2015-05-16 14:28:05.258913', 3, 'night', 'No'],
                    ['2015-05-17 14:28:05.258913', 1, 'night', 'No'],
                    ['2015-05-27 14:26:04.477710', 5, 'night', 'No'],
                    ['2015-06-03 14:28:05.258913', 3, 'night', 'No'],
                    ['2015-06-12 14:28:05.258913', 1, 'night', 'No'],
                    ['2015-06-15 14:28:05.258913', 3, 'night', 'No'],
                    ['2015-06-16 14:28:05.258913', 1, 'night', 'No'],
                    ['2015-06-29 14:26:04.477710', 5, 'night', 'No'],
                    ['2015-06-30 14:28:05.258913', 3, 'night', 'No'],
                    ['2015-07-01 14:28:05.258913', 1, 'night', 'No'],
                    ['2015-07-02 14:28:05.258913', 3, 'night', 'No'],
                    ['2015-07-03 14:28:05.258913', 1, 'night', 'No'],
                    ['2015-07-04 14:26:04.477710', 5, 'night', 'No'],
                    ['2015-07-10 14:28:05.258913', 3, 'night', 'No'],
                    ['2015-07-11 14:28:05.258913', 1, 'night', 'No']], 
                    columns=['time','inout','day','breeding'])
data_test['time'] = pd.to_datetime(data_test.time)

##################################
# Functions for Preprocessing Data
##################################

def data_year(data):
    data_plot=data['inout'].groupby(data['time'].dt.to_period('Y')).sum()
    # making it a data frame again
    data_plot=data_plot.reset_index()
    # making to timestamp
    data_plot['time'] = data_plot['time'].dt.to_timestamp('Y')
    return data_plot

def data_hour(data):
    data_plot=data['inout'].groupby(data['time'].dt.to_period('H')).sum()
    #making it a data frame again
    data_plot=data_plot.reset_index()
    # making to timestamp
    data_plot['time'] = data_plot['time'].dt.to_timestamp('H')
    return data_plot

def data_day(data):
   data_plot=data['inout'].groupby(data['time'].dt.to_period('d')).sum()
   # making it a data frame again
   data_plot=data_plot.reset_index()
   # making to timestamp
   data_plot['time'] = data_plot['time'].dt.to_timestamp('d')
   return data_plot

def data_month(data):
   data_plot=data['inout'].groupby(data['time'].dt.to_period('m')).sum()
   # making it a data frame again
   data_plot=data_plot.reset_index()
   # making to timestamp
   data_plot['time'] = data_plot['time'].dt.to_timestamp('d')
   return data_plot

# Function to know where to indicate night
def night_lines(data):
    """
    Parameter:
    data - a pandas DataFrame
    
    """
    v_lines = []
    if data.iloc[0]['day']==False:
        v_lines.append(data.iloc[0]['time'])
    for i in range(1,len(data)-1):
        if data.iloc[i]['day'] ==False and data.iloc[i-1]['day'] ==True:
            v_lines.append(data.iloc[i]['time'])
        elif data.iloc[i]['day'] ==False and data.iloc[i+1]['day'] ==True:
            v_lines.append(data.iloc[i]['time'])
    if data.iloc[-1]['day']==False:
        v_lines.append(data.iloc[-1]['time'])
    return v_lines


###########################
# Function for Plotting 
###########################
   
# Function used to plot 
def plot_bird(plot_freq, data, start, end, night=None):
    """
    Parameters:
    * plot_freq - 'hour', 'day', 'month' or 'year' 
    * data - the data returned from data_hour, data_day, data_month or data_year
    * start - start date ex '2015-01-26'
    * end - end date ex '2015-02-03'
    * night - the returned object from night_lines function (needed
      to plot by hour)
    """
    start=pd.to_datetime(start)
    end=pd.to_datetime(end)
    # per hour
    if plot_freq == 'hour':
        data = data[(data['time']>=start) & (data['time']<=end)]
        night = [night[i] for i in range(len(night)) if night[i]>=start and night[i]<=end]
        if len(night)%2!=0:
            night.append(end)
        fig, ax =subplots()
        # Note the units for date axis is in days 
        ax.bar((data['time']), data['inout'], width = 0.04) 
        for i in range(len(night)):
            if i%2 == 0:
                ax.axvspan(night[i], night[i+1], alpha=0.2, color='black')
        if len(data)>80:
            interval_val = round(len(data)/40)
        else:
            interval_val = 1
        ax.xaxis.set_major_locator(dates.DayLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
        ax.xaxis.set_minor_locator(dates.HourLocator(interval = interval_val))
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%H'))
        ax.axis([min(data['time']), max(data['time']), 0, 1.1*max(data['inout'])])
        xticks(rotation=75)
        xlabel('Hour')
        ylabel('Number of moves')
        title('Number of Times Entering or Leaving the Nest Per Hour')
    # per day
    if plot_freq == 'day':
        #A list needs to contain something in order for .append to work, the fives are later removed.
        breeding = list([5])
        feeding = list([5])
        ## Cheching for specific months and days and adding to breeding and feeding.
        ##I adjusted the times to fit the data, and realised that there was most likely 
        ##two separete breeding/feeding periods, which is possible according to google.##
        for x in range (data.shape[0]):
            if '-04-' in str(data.iloc[x,0]):
                s = str(data.iloc[x,0])
                
                if int(s[8:10]) > 26 :
                    breeding.append([data.iloc[x,0],data.iloc[x,1]])
                    
            if '-05-' in str(data.iloc[x,0]):
                s = str(data.iloc[x,0])
                if int(s[8:10])< 13:
                    breeding.append([data.iloc[x,0],data.iloc[x,1]])
                    
                if int(s[8:10])> 12 and int(s[8:10])< 29:
                    feeding.append([data.iloc[x,0],data.iloc[x,1]])
                    
            if '-06-' in str(data.iloc[x,0]):
                s = str(data.iloc[x,0])
                if int(s[8:10])> 11 and int(s[8:10])<26:
                    breeding.append([data.iloc[x,0],data.iloc[x,1]])
                    
                    
                if int(s[8:10])> 24:
                    feeding.append([data.iloc[x,0],data.iloc[x,1]])
                    
            if '-07-' in str(data.iloc[x,0]):
                s = str(data.iloc[x,0])
                if int(s[8:10])< 12:
                    feeding.append([data.iloc[x,0],data.iloc[x,1]])
                
                    
        ##Removing the first item (the five from earlier) from breeding and feeding
        breeding.pop(0)
        feeding.pop(0)
        #Making them DataFrames
        breeding = pd.DataFrame(breeding)
        feeding = pd.DataFrame(feeding)
        data = data[(data['time']>=start) & (data['time']<=end)]
        fig, ax =subplots()
#       fig.set_size_inches(20,15) (I needed this because otherwise the plot was tiny on my screen)
        ax.bar((data['time']), data['inout'], width=0.95)
        #Blue is the standard color. I made breeding and incubating yellow 
        # and feeding red to make them stand out.
        ax.bar((breeding[0]), breeding[1], width=0.95, color = 'Yellow')
        ax.bar((feeding[0]), feeding[1], width=0.95, color = 'Red')
        
        
        if len(data)>36:
                interval_val = round(len(data)/18)
        else:
            interval_val = 1
        ax.xaxis.set_major_locator(dates.YearLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
        ax.xaxis.set_minor_locator(dates.DayLocator(interval = interval_val))
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%m-%d'))
        ax.axis([min(data['time']), max(data['time']), 0, 1.1*max(data['inout'])])
        xticks(rotation=75)
        xlabel('Day')
        ylabel('Number of moves')
        title('Number of Times Entering or Leaving the Nest Per Day')
    # per month
    if plot_freq == 'month':
        data = data[(data['time']>=start) & (data['time']<=end)]
        fig, ax =subplots()
        ax.bar((data['time']), data['inout'], width=27) 
        ax.xaxis.set_major_locator(dates.YearLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
        ax.xaxis.set_minor_locator(dates.MonthLocator())
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
        xticks(rotation=75)
        xlabel('Month')
        ylabel('Number of moves')
        title('Number of Times Entering or Leaving the Nest Per Month')   
    # per year    
    if plot_freq == 'year':
        data = data[(data['time'].dt.to_period('Y')>=start.to_period('Y')) & (data['time'].dt.to_period('Y')<=end.to_period('Y'))]
        fig, ax =subplots()
        ax.bar((data['time']), data['inout'], width= 350)
        ax.set_xticks(data['time'])
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
        ax.xaxis.set_minor_formatter(dates.DateFormatter('%Y'))
        xlabel('Year')
        ylabel('Number of moves')
        title('Number of Times Entering or Leaving the Nest Per Year')


##Testing##        
#data_test = data_day(data_test)
#plot_bird('day',data_test,'2015-06-01','2015-07-27') 
         