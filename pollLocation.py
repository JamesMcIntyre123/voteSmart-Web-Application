#import NumPy library
import numpy
from flask_wtf import FlaskForm as Form
import sqlite3
from flask import Flask, render_template, url_for, make_response, request, redirect, session

class PollLocation:
  def __init__(self,streetNum,streetName,city,state,zip,hours):
    self.hours = hours
    self.streetNum = streetNum
    self.streetName = streetName
    self.city = city 
    self.state = state
    self.zip = zip 

  #getters & setters
    def getStreetNum(self):
        return self.streetNum
        
    def setStreetNum(num):
        self.streetNum = num
        
    def getStreetN(sameelf):
        return self.streetName
        
    def setStreetName(num):
        self.streetName = num
        
    def setCity(c):
        self.city = c
        
    def getCity(self):
        return self.city
        
    def getState(self):
        return self.state
        
    def setState(s):
        self.state = s
        
    def getZip(self):
        return self.zip
        
    def setZip(z):
        self.zip = z
        
    def getHours(self):
        return hours
        
    def setHours(h):
        self.hours = h


  #methods/functions/whatever
    def setHour(i, j, h):
        self.hours[i][j] = h
  
    def printHours(self):
        for row in self.hours:
            for val in row:
                print('{:4}'.format(val), print())

class printLocation(Form):

    def __init__(self, form):
        #for fieldname, value in form.data.items:
        #    logging.debug("%s : %s", fieldname, value)
        d = form.to_dict()

        c = d.get('county')
        con = sqlite3.connect("user_data.db")
        cursor = con.cursor()
        cursor.execute('SELECT * FROM polls WHERE county = ?', [c])
        con.commit()
        match = cursor.fetchone()
        if match:
            self.name = match[2]
            self.precinct = match[1]
            self.city = match[5]
            self.streetname = match[4]
            self.streetnum = match[3]
            self.county = match[0]
            self.zip = match[6]
            self.state = match[7]
            self.site = match[8]
        else:
            self.name = 0
            self.precinct = 0
            self.city = 0
            self.streetname = 0
            self.streetnum = 0
            self.county = 0
            self.zip = 0
            self.state = 0
            self.site = 0

    def __call__(self, county, streetname, streetnum, zip, state, name, precinct, city, match, site):
        self.county = county
        self.streetname = streetname
        self.streetnum = streetnum
        self.zip = zip
        self.state = state
        self.name = name
        self.precinct = precinct
        self.city = city
        self.match = match
        self.site = site