# -*- coding: utf-8 -*-
"""
Created on Thu May 21 10:32:56 2020

@author: Jesper
"""


import tkinter as tk
import tkinter.ttk as ttk
from numpy import *

import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from datetime import date
import datetime
from datetime import datetime
import birdplotBreedandfeed as bp
import pandas as pd
from tkinter import messagebox as mb

class Application:
    
    def __init__(self, master):
        #Creates the two primare frames
        self.SettingsFrame = tk.Frame(master)
        self.SettingsFrame.pack(side = tk.RIGHT)
        self.DisplayFrame = tk.Frame(master)
        self.DisplayFrame.pack(side = tk.LEFT)
        
        Label1 = tk.Label(self.SettingsFrame, text = "Starting Date")
        Label2 = tk.Label(self.SettingsFrame, text = "Endinging Date")
        Label1.grid(row = 2)
        Label2.grid(row = 3)
        
        #Creates entry fields
        self.E1 = tk.StringVar()
        self.E2 = tk.StringVar() 
        self.Entry1 = tk.Entry(self.SettingsFrame, textvariable = self.E1)
        self.Entry2 = tk.Entry(self.SettingsFrame, textvariable = self.E2)
        self.E1.set("2015-01-25 14:05")
        self.E2.set("2015-01-27 14:28")
        
        self.Entry1.grid(row = 2, column = 1)
        self.Entry2.grid(row = 3, column = 1)
    
        Label3 = tk.Label(self.SettingsFrame, text = "Display Data By:")
        Label3.grid(row = 4)
        #Creates the combobox for selecting a time frame
        self.TimeFrameSettings = ttk.Combobox(self.SettingsFrame, 
                            values=[
                                    "Hour", 
                                    "Day",
                                    "Month",
                                    "Year"])
        self.TimeFrameSettings.grid(row=4, column = 1)
        self.TimeFrameSettings.current(1)
        
    
        #creates buttons for applying/restoring settings and binds them to functions
        self.ApplyButton = tk.Button(self.SettingsFrame, text = "Apply Settings", command = self.applySettings)
        self.defaultButton = tk.Button(self.SettingsFrame, text = "Restore Settings", command = self.defaultSettings)
        
        self.ApplyButton.grid(row = 6)
        self.defaultButton.grid(row = 6, column = 1)
        
        
        

        
        
        #Creates and places the figure/toolbar
        
        self.fig = plt.Figure(figsize=(5,5), dpi=100)
        
        self.ax = self.fig.add_subplot(111)
        
        
        
        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()

        toolbar = NavigationToolbar2Tk(self.canvas, master)
        toolbar.update()

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
    def UpdatePlot(self):
        #Clears the plot and creates a new one depending on the selected timeframe
        import birdsFinally as bird
        dateTimes = bird.DatesTimes2
        moves = bird.moves2
        daynight = bird.daynight 
        feeding = bird.feeding
        roosting = bird.roosting

        data = pd.DataFrame({'time':dateTimes, 'inout':moves,
                     'day':daynight, 'feeding':feeding, 'roosting':roosting})
        
        dataHour = bp.data_hour(data)
        dataDay = bp.data_day(data)
        dataMonth =bp.data_month(data)
        dataYear = bp.data_year(data)
        
        night = bp.night_lines(data)
        
        start=datetime.strptime(self.E1.get(), "%Y-%m-%d %H:%M")#pd.to_datetime(start)
        end=datetime.strptime(self.E2.get(), "%Y-%m-%d %H:%M")#pd.to_datetime(end)
        
        self.ax.clear()
        if self.TimeFrameSettings.current() == 0:
            data = data[(data['time']>=start) & (data['time']<=end)]
            night = [night[i] for i in range(len(night)) if night[i]>=start and night[i]<=end]
            if len(night)%2!=0:
                night.append(end)
            
            for i in range(len(night)):
                 if i%2 == 0:
                     self.ax.axvspan(night[i], night[i+1], alpha=0.2, color='black')
            if len(data)>80:
                interval_val = round(len(data)/40)
            else:
                interval_val = 1
            
            self.ax.bar((dataHour['time']), dataHour['inout'], width=0.025) # might have to change setting for width
            #ax.set_xticks(data_plot['time'])
            self.ax.xaxis.set_major_locator(dates.DayLocator())
            self.ax.xaxis.set_major_formatter(dates.DateFormatter('%m-%d'))
            self.ax.xaxis.set_minor_locator(dates.HourLocator())
            self.ax.xaxis.set_minor_formatter(dates.DateFormatter('%H'))
           
            self.canvas.draw()
        
        if self.TimeFrameSettings.current() == 1:
            data = data[(data['time']>=start) & (data['time']<=end)]
            self.ax.bar((dataDay['time']), dataDay['inout']) # might have to change setting for width
            #ax.set_xticks(data_plot['time'])
            if len(data)>36:
                interval_val = round(len(data)/18)
            else:
                interval_val = 1
            
            self.ax.xaxis.set_major_locator(dates.YearLocator())
            self.ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
            self.ax.xaxis.set_minor_locator(dates.DayLocator())
            self.ax.xaxis.set_minor_formatter(dates.DateFormatter('%m-%d'))
           
            self.canvas.draw()
        
        if self.TimeFrameSettings.current() == 2:
            self.ax.bar((data['time']), data['inout'], width=27) 
            self.ax.xaxis.set_major_locator(dates.YearLocator())
            self.ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
            self.ax.xaxis.set_minor_locator(dates.MonthLocator())
            self.ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
            
            self.canvas.draw()
        if self.TimeFrameSettings.current() == 3:
            self.ax.bar((dataYear['time']), dataYear['inout'])
            self.ax.set_xticks(dataYear['time'])
            self.ax.xaxis.set_major_formatter(dates.DateFormatter('%Y'))
            self.ax.xaxis.set_minor_formatter(dates.DateFormatter('%Y'))
           
            self.canvas.draw()
        
        
    
        #Activated when ApplySettings-button is pressed
    def applySettings(self, *args):
        try:
        #import birdPlot as bp
        #testData = bp.data1
        #dataHour = bp.data_hour(testData)
        #This is where most of the interaction with the plots will happen
            StartDateTime = datetime.strptime(self.E1.get(), "%Y-%m-%d %H:%M")
            EndDateTime = datetime.strptime(self.E2.get(), "%Y-%m-%d %H:%M") #Retrieves dates to display between (WIP)
            print(StartDateTime) 
            print("Settings Applied")
            self.UpdatePlot() #Updates the plot
        except:
            mb.showerror("Answer", "One or more of the times is faulty, please try again and use the form year-month-day hour:minute")
        
        #Activated when Reestore Settings-button is pressed
    def defaultSettings(self):
        print("Default Settings Restored")
        

        
 
           
 
root = tk.Tk()

Application(root)#These lines start the program

root.mainloop()