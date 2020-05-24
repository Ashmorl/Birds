# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(Petter)s
"""

from numpy import*
from matplotlib.pyplot import*
import sys
from datetime import*
from astral import LocationInfo
from astral.sun import sun
import pytz

#reading the file (wherever it is in your computer):
birds=open(r"bird_jan25jan16.txt","r")

#extracting and separating the data in two lists:
datestimes=[]
total_moves=[]
daynight=[]
roosting=[]
feeding=[]



for line in birds.readlines():
    if "   " in line.split("    ")[0]:
        datestimes.append(line.split("   ")[0])
        total_moves.append(line.split("   ")[1])
    else:
        datestimes.append(line.split("    ")[0])
        total_moves.append(line.split("    ")[1])

#converting dates and times to datetime objects:
DatesTimes=list(datetime.strptime(datestimes[i],"%Y-%m-%d %H:%M:%S.%f",) for i in range(len(datestimes)))

#converting number of moves to integers
for i in range(len(total_moves)):
    total_moves[i]=int(total_moves[i])
    
#fixing the counts that are incompletely reported.
#The double inequation avoids problems with the "jumps"
for i in range(1,len(total_moves)):
    if total_moves[i]<total_moves[i-1]<=total_moves[i+1]:
        total_moves[i]=total_moves[i-1]

#removing the lines that go "back in time"
skip=0
for i in range(1,len(DatesTimes)): 
    i=i-skip
    if DatesTimes[i]<DatesTimes[i-1]:
        del(DatesTimes[i])
        del(total_moves[i])
        skip=skip+1

#counting the number of moves per 2 minutes period by calculating the difference.
moves=list(diff(total_moves))
DatesTimes1=DatesTimes[1:]

#Fixing the "gaps" by introducing lines every two minutes.
#No movement is recorded for the periods when we're missing information.
DatesTimes2=[DatesTimes1[0]]
moves2=[moves[0]]
for i in range(1,len(DatesTimes1)):
    if DatesTimes1[i]-DatesTimes1[i-1]>timedelta(seconds=180):
        for j in range(1,1000):
            extraline=DatesTimes1[i-1]+j*timedelta(seconds=120)
            DatesTimes2.append(extraline)
            moves2.append(0)
            if extraline+timedelta(seconds=180)>DatesTimes1[i]:
                DatesTimes2.append(DatesTimes1[i])
                moves2.append(moves[i])
                break                
    else:
        DatesTimes2.append(DatesTimes1[i])
        moves2.append(moves[i])

#fixing "jumps" in the counts
# fixing "wrong" data for biological reasons by limitting the motions to maximal 4 per minute
for i in range(len(moves)):
    if moves[i]<0:
        moves[i]=1
    if moves[i]>8:
        moves[i]=8

uct=pytz.timezone('UCT')
tz=pytz.timezone('Europe/Stockholm')
DTS1=[]
DTS2=[]
for i in range(len(DatesTimes2)):
    dtsl=uct.localize(DatesTimes2[i])
    dts2=dtsl.astimezone(tz)
    DTS2.append(dts2)
    DTS1.append(dtsl)
    
#sets up the location for astral
city=LocationInfo('Lund', 'Sweden', 'Europe/Stockholm', 55.70,13.19)
# this part creates a list for if the sun was up (True) or down (False) at a specific data point
sunup=[]
sundown=[]
for i in range(len(DTS2)):
    s = sun(city.observer, date=datetime.date(DTS2[i]), tzinfo=pytz.timezone(city.timezone))
    sunup.append(s['sunrise'])
    sundown.append(s['sunset'])
    if DTS2[i].hour < sundown[i].hour and DTS2[i].hour > sunup[i].hour or DTS2[i].hour==sunup[i].hour and DTS2[i].minute > sunup[i].minute or DTS2[i].hour==sundown[i].hour and DTS2[i].minute < sundown[i].minute:
        daynight.append(True)
    else:
        daynight.append(False)

for i in range(len(DTS2)):
    if DTS2[i].month==4 and DTS2[i].day>=15 or DTS2[i].month==5 and DTS2[i].day<=15:
        roosting.append(True)
    else:
        roosting.append(False)
        
for i in range(len(DTS2)):
    if DTS2[i].month==4 and DTS2[i].day>=28 or DTS2[i].month==5 and DTS2[i].day<=28:
        feeding.append(True)
    else:
        feeding.append(False)

