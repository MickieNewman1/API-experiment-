# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:18:48 2021

@author: Mickie Newman
"""

#API 
# Mickie Newman 
#20/04/03


import pygame
from random import * #imports all the random functions
import numpy as np # math library
import urllib #accesses online data
import json #processes online data
import requests
import pdb
pygame.init()

#set up our screen (global variables)
screen = pygame.display.set_mode((400,400)) 
screen.fill((0,0,0))

#import data GLOBAL variable with website!!
URL = 'https://api.weather.gov/gridpoints/BOU/53,74/forecast'

#create classes
#use API data (temperature) to control sizes of different circles
#from script template
class tempCirc:
    def __init__(self,screen,URL=URL,location=[50,100],color=(0,0,0)): #special method that runs when we instantiate our object
        self.data=self.getData(URL)#our data will automatically get stored here when we run self.updatData in the next line
        self.numCirc=6 #number of circles to draw
        self.radius,self.forecast= self.parseData() #store the temp data to self.radius
        self.location= location
        self.color= color
        self.screen=screen
#create objects/inital conditions/local variables
    #(from script template)
    def getData(self, URL=URL):
        
        #Pull data from the URL
        return requests.get(URL).json() #pull data from your URL
    #(from script template)
    def parseData(self):
       '
        #create data variable with values you want to work with.  
        #Here I'll just use temp
        temp=[]
        for i in range(self.numCirc):
            temp.append(self.data['properties']['periods'][i]['temperature']) #list of temp
    
        #example second data (not used)
        forecast=[]
        for i in range(self.numCirc):
            forecast.append(self.data['properties']['periods'][i]['shortForecast']) #list of short forecast descriptions
        return temp, forecast
    
    
    def labelData(self,idx,loc,xoffset=0, yoffset=0, fontsize = 40,fontcolor=(255,255,255),background=(0,0,0)):
        '''Adds text to describe data. Gets called when circles are drawn, but can be called whenever'''
        # adds text to describe data. gets called when circles are drawn 
        font = font = pygame.font.Font('freesansbold.ttf', fontsize) 
      
        label=self.data['properties']['periods'][idx]['name'] #CHANGE THIS to your datase label, if any
      
        #Add text from: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
        text = font.render(label, True, fontcolor) 
        # create a rectangular object for the 
        # text surface object 
        textRect = text.get_rect()  
      
        # set the center of the rectangular object. 
        textRect.center = (loc[0]+xoffset // 2, loc[1]+yoffset // 2) 
        
        # copying the text surface object 
        # to the display surface object  
        # at the center coordinate. 
        screen.blit(text, textRect) 

    def drawCirc(self,label=True):#(from script template)
        
        circList = []
        for i in range(self.numCirc):
            loc = (self.location[0], int(self.location[1] + i*50)) #space circles by 10
            circList.append(pygame.draw.circle(self.screen,self.color,loc,int(self.radius[i]/2)))
            #add labels
            if label:
                self.labelData(i,loc,xoffset=400,yoffset=0) #offsets control locations...
                            
    def timeOfDay(self):
        """shows by a circle if it is daytime or night time"""
        timeColors = [(0,0,0),(255,255,0)]
        time = []
        for i in range(self.numCirc):
            time.append(self.data['properties']['periods'][i]['isDaytime']) #list of whether it is daytime in boolians 
            if time[i] == True:
                pygame.draw.circle(self.screen,timeColors[1],(400,400),50)
            elif time[i]== False:
                pygame.draw.circle(self.screen,timeColors[0],(400,400),50)
                
        
  
    def backgroundColor(self):
        '''changes background color based on the temputure of the day'''
        colors = [(225,0,0),(0,225,0),(0,0,225)]
        temp=[]
        for i in range(self.numCirc):
            temp.append(self.data['properties']['periods'][i]['temperature']) #list of temp
            if temp[i] <= 60:
                color= colors[2]
                print('PUT ON A COAT!!!!!')
            elif temp[i] <= 80:
                color = colors[1]
                print('GO OUTSIDE IT IS NICE OUT!')
            elif temp[i] > 80:
                color = colors [0]  
                print('WEAR SHORTS!!!!')    
        screen.fill(color)

#create object
bubble = tempCirc(screen) #our object only has one required 

#game loop
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
    #create actions
    bubble.backgroundColor()
    bubble.timeOfDay()
    bubble.drawCirc()
    
    #update screen
    pygame.display.update()
    
pygame.quit()