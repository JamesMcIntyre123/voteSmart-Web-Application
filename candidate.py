#import NumPy library
import numpy
from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms.validators import ValidationError, InputRequired
import logging
import sqlite3

class Candidate: 
    def __init__(self, name, party, gender, facts, agenda):
        self.name = name
        self.party = party
        self.gender = gender 
        self.facts = facts 
        self.agenda = agenda
    
    def getName(self):
        return self.name
        
    def setName(self, n):
        self.name = n
        
    def getParty(self):
        return self.party
        
    def setParty(self, p):
        self.party = p
        
    def getGender(self):
        return self.gender
        
    def setGender(self, g):
        self.gender = g
        
    def getFacts(self):
        return self.facts
    
    def setFacts(self, f):
        self.facts = f
        
    def getAgenda(self):
        return self.agenda
        
    def setAgenda(self, a):
        self.agenda
        
    def modifyFacts(self, i, f):
        self.facts[i] = f
        
    def modifyAgenda(self, i, a):
        self.agenda[i] = a
        
    def addFact(self, f):
        self.facts.append(f)
        
    def addTooAgenda(self, a):
        self.agenda.append(a)


class printCandidate(Form):
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

class StateQuiz(Form):
    class Meta:
        csrf = False

    state = RadioField("What state do you live in?", 
    choices = [("Florida", "Florida")], validators=[InputRequired()])
    
    district = RadioField("Which Florida Disctrict do you reside in?", 
    choices = [("Seminole", "Seminole"), ("I don't know", "I don't know")], validators=[InputRequired()])

   