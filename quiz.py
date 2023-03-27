from flask_wtf import FlaskForm as Form
from wtforms import RadioField
import plotly.express as px
from wtforms.validators import ValidationError, InputRequired
import logging
import sqlite3
import matplotlib.pyplot as plt

logging.basicConfig(filename='record.log', level=logging.DEBUG)

score = 0

class QuizUser: 
  def __init__(self, formNum, questions):
    self.formNum = formNum
    self.questions = questions 
    self.answers = []
    
    #percents added in calculateScore
    partyPercents = []

    #getters and setters
    def getFormNum(self):
        return self.formNum

    def setFormNum(fNum):
        self.formNum = fNum
        
    def getQuestions(self):
        return self.questions
        
    def setQuestions(arr):
        self.questions = arr
        
    def getAnswers(self):
        return self.answers
        
    def setAnswers(arr):
        self.answers = arr
        
    def calculateScore(self, user, partyPercents, answers):
        for i in self.answers:
            partyPercents[answers[i]] += 1
            
        #num for keeping track of highest score
        num = 0
        for j in self.partyPercents:
            if partyPercents[i] > num:
                num = partyPercents[i]
            user.setParty(num)
        
        
    def printQuiz(self):
       for i in self.questions:
        print(questions[i])

class CheckAnswer(object):
    #pScore = printScore()
    def __init__(self, answer):
        logging.debug("CheckAnswer init Called %s", answer)
        self.answer = answer

    def __call__(self):
        logging.debug("CheckAnswer call Called")
    
    def printField(self,field):
         logging.debug("CheckAnswer field is Called : %s", field.data)


class printScore(Form):
    leftscore = 0
    rightscore = 0
    indscore = 0
    valalign = 0
    marcalign = 0
    ronalign = 0
    charalign = 0
    candidates = []

    def __init__(self, form):
        logging.debug("PrintScore Init Called")
        #for fieldname, value in form.data.items:
        #    logging.debug("%s : %s", fieldname, value)
        d = form.to_dict()

        # 3 accounts for first two questions and submit button
        questionnum = (len(d) - 3)

        # we do not need this for governer or senator because it is just FL
        #state = d.get('state')

        # for representatives by district
        district = d.get('district')
        con = sqlite3.connect("user_data.db")
        cursor = con.cursor()
        cursor.execute('SELECT * FROM candidates WHERE district = ?', [district])
        con.commit()
        cands = cursor.fetchall()
        logging.debug(cands)
        self.cand1 = cands[0][0]
        logging.debug(self.cand1)
        self.cand2 = cands[1][0]
        self.party1 = cands[0][1]
        self.party2 = cands[1][1]
        self.bio1 = cands[0][2]
        self.bio2 = cands[1][2]
        self.state1 = cands[0][3]
        self.state2 = cands[1][3]
        self.run1 = cands[0][4]
        self.run2 = cands[1][4]
        dist1 = cands[0][5]
        self.dist1 = dist1
        dist2 = cands[1][5]
        self.dist2 = dist2
        self.site1 = cands[0][6]
        self.site2 = cands[1][6]

            

        dict = {'1': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '2': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"}, 
        '3': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"}, 
        '4': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"}, 
        '5': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"}, 
        '6': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '7': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '8': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '9': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '10': {},
        '11': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '12': {"q1":"No","q2":"Yes","q3":"No","q4":"No","q5":"Yes","q6":"No","q7":"No","q8":"Yes","q9":"Yes","q10":"No","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '13': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '14': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '15': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '16': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '17': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '18': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '19': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '20': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '21': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '22': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '23': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '24': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '25' : {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '26': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '27': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '28': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '29': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '30': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '31': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '32': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '33': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '34': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '35': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '36': {"q1":"No","q2":"No","q3":"No","q4":"Yes","q5":"Yes","q6":"Yes","q7":"Yes","q8":"No","q9":"Yes","q10":"No","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"No","q18":"Pro-Life"},
        '37': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '38': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '39': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '40': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '41': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '42': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '43': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '44': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '45': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '46': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '47': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '48': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '49': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '50': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '51': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '52': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '53': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '54': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"},
        '55': {"q1":"No","q2":"No","q3":"No","q4":"No","q5":"Yes","q6":"Yes","q7":"No","q8":"No","q9":"Yes","q10":"Yes","q11":"Yes","q12":"No","q13":"No","q14":"Yes","q15":"Yes","q16":"Yes","q17":"Yes","q18":"Pro-Life"},
        '56': {"q1":"Yes","q2":"Yes","q3":"Yes","q4":"Yes","q5":"No","q6":"Yes","q7":"Yes","q8":"Yes","q9":"Yes","q10":"Yes","q11":"No","q12":"Yes","q13":"No","q14":"Yes","q15":"Yes","q16":"No","q17":"Yes","q18":"Pro-Choice"}}

        if questionnum != 0:
            logging.debug('DICT')
            # cand 1
            var = dist1 - 1
            d1 = (dist1 - var) + 4
            if dist1 == 1:
                d1 = dist1
            d1 = str(d1)
            logging.debug(d1)
            dict1 = dict[d1]
            cand1_shared = {k: dict1[k] for k in dict1 if k in d and dict1[k] == d[k]}
            lencand1 = len(cand1_shared)
            self.cand1score = "{0:.0%}".format(lencand1/questionnum)
            self.rotatecand1 = (lencand1/questionnum) * 180
            logging.debug('DICT1')
            logging.debug(dist1)
            logging.debug(d1)
            logging.debug(dict1)
            logging.debug(lencand1)

            #if self.cand2 != 0:
            # cand 2
            d2 = dist2 * 2
            d2 = str(d2)
            dict2 = dict[d2]
            cand2_shared = {k: dict2[k] for k in dict2 if k in d and dict2[k] == d[k]}
            lencand2 = len(cand2_shared)
            self.cand2score = "{0:.0%}".format(lencand2/questionnum)
            self.rotatecand2 = (lencand2/questionnum) * 180
            logging.debug('DICT2')
            logging.debug(d2)
            logging.debug(dict2)
            logging.debug(self.cand2score)
            logging.debug(self.rotatecand2)
            logging.debug(dict1)
        
        else:
            self.cand1 = "{0:.0%}".format(0)
            self.cand2 = "{0:.0%}".format(0)
            self.party1 = "{0:.0%}".format(0)
            self.party2 = "{0:.0%}".format(0)
            self.bio1 = "{0:.0%}".format(0)
            self.bio2 = "{0:.0%}".format(0)
            self.state1 = "{0:.0%}".format(0)
            self.state2 = "{0:.0%}".format(0)
            self.run1 = "{0:.0%}".format(0)
            self.run2 = "{0:.0%}".format(0)
            self.dist1 = 0
            self.dist2 = "{0:.0%}".format(0)
            self.site1 = "{0:.0%}".format(0)
            self.site2 = "{0:.0%}".format(0)
            dict1 = "{0:.0%}".format(0)
            dict2 = "{0:.0%}".format(0)
            self.rotatecand1 = "{0:.0%}".format(0)
            self.rotatecand2 = "{0:.0%}".format(0)
            self.cand1score = 0
            self.cand2score = 0

        
        logging.debug(cands)



        if questionnum != 0:
            rightwing = {"q1":"Yes", "q2":"No", "q3":"Yes", "q4":"No", "q5":"Yes", "q6":"No", "q7":"No", "q8":"No", "q9":"No", "q10":"Yes", "q11":"Yes", "q12":"No", "q13":"Yes", "q14":"Yes", "q15":"No", "q16":"Yes", "q17":"No", "q18":"Pro-Life"}
            right_shared = {k: rightwing[k] for k in rightwing if k in d and rightwing[k] == d[k]}
            right = len(right_shared)
            self.right = right
            self.rightscore = "{0:.0%}".format(right/questionnum)

            leftwing = {"q1":"No", "q2":"Yes", "q3":"No", "q4":"Yes", "q5":"No", "q6":"Yes", "q7":"Yes", "q8":"Yes", "q9":"Yes", "q10":"No", "q11":"No", "q12":"Yes", "q13":"No", "q14":"No", "q15":"Yes", "q16":"No", "q17":"Yes", "q18":"Pro-Choice"}
            left_shared = {k: leftwing[k] for k in leftwing if k in d and leftwing[k] == d[k]}
            left = len(left_shared)
            lefttotal = (left * (-1))
            self.left = left
            self.leftscore = "{0:.0%}".format(left/questionnum)
        
            indwing = {"q1":"I don't know", "q2":"I don't know", "q3":"I don't know", "q4":"I don't know", "q5":"I don't know", "q6":"I don't know", "q7":"I don't know", "q8":"I don't know", "q9":"I don't know", "q10":"I don't know", "q11":"I don't know", "q12":"I don't know", "q13":"I don't know", "q14":"I don't know", "q15":"I don't know", "q16":"I don't know", "q17":"I don't know", "q18":"I don't know"}
            ind_shared = {k: indwing[k] for k in indwing if k in d and indwing[k] == d[k]}
            ind = len(ind_shared)
            self.ind = ind
            self.indscore = "{0:.0%}".format(ind/questionnum)

            totalscore = right + lefttotal


            valwing = {"q1":"I don't know", "q2":"Yes", "q3":"I don't know", "q4":"Yes", "q5":"No", "q6":"Yes", "q7":"Yes", "q8":"Yes", "q9":"Yes", "q10":"Yes", "q11":"I don't know", "q12":"I don't know", "q13":"No", "q14":"I don't know", "q15":"Yes", "q16":"Yes", "q17":"Yes", "q18":"Pro-Choice"}
            val_shared = {k: valwing[k] for k in valwing if k in d and valwing[k] == d[k]}
            valnum = len(val_shared)
            self.valalign = "{0:.0%}".format(valnum/questionnum)
            self.rotateval = (valnum/questionnum) * 180

            marcwing = {"q1":"Yes", "q2":"No", "q3":"No", "q4":"No", "q5":"Yes", "q6":"No", "q7":"No", "q8":"No", "q9":"No", "q10":"Yes", "q11":"Yes", "q12":"No", "q13":"Yes", "q14":"Yes", "q15":"No", "q16":"Yes", "q17":"No", "q18":"Pro-Life"}
            marc_shared = {k: marcwing[k] for k in marcwing if k in d and marcwing[k] == d[k]}
            marcnum = len(marc_shared)
            self.marcalign = "{0:.0%}".format(marcnum/questionnum)
            self.rotatemarc = (marcnum/questionnum) * 180


            ronwing = {"q1":"Yes", "q2":"No", "q3":"Yes", "q4":"No", "q5":"Yes", "q6":"No", "q7":"No", "q8":"No", "q9":"No", "q10":"Yes", "q11":"Yes", "q12":"No", "q13":"Yes", "q14":"Yes", "q15":"No", "q16":"Yes", "q17":"No", "q18":"Pro-Life"}
            ron_shared = {k: ronwing[k] for k in ronwing if k in d and ronwing[k] == d[k]}
            ronnum = len(ron_shared)
            self.ronalign = "{0:.0%}".format(ronnum/questionnum)
            self.rotateron = (ronnum/questionnum) * 180


            charwing = {"q1":"No", "q2":"Yes", "q3":"No", "q4":"Yes", "q5":"No", "q6":"Yes", "q7":"Yes", "q8":"Yes", "q9":"Yes", "q10":"No", "q11":"No", "q12":"Yes", "q13":"No", "q14":"No", "q15":"Yes", "q16":"No", "q17":"Yes", "q18":"Pro-Choice"}
            char_shared = {k: charwing[k] for k in charwing if k in d and charwing[k] == d[k]}
            charnum = len(char_shared)
            self.charalign = "{0:.0%}".format(charnum/questionnum)
            self.rotatechar = (charnum/questionnum) * 180

            

        else:
            self.rightscore = "{0:.0%}".format(0)
            self.leftscore = "{0:.0%}".format(0)
            self.indscore = "{0:.0%}".format(0)
            self.valalign = "{0:.0%}".format(0)
            self.marcalign = "{0:.0%}".format(0)
            self.ronalign = "{0:.0%}".format(0)
            self.charalign = "{0:.0%}".format(0)
            self.totalscore = "{0:.0%}".format(0)
            self.rotatechar = "{0:.0%}".format(0)
            self.rotateval = "{0:.0%}".format(0)
            self.rotateron = "{0:.0%}".format(0)
            self.rotatemarc = "{0:.0%}".format(0)
            
        
        logging.debug(len(d))
        logging.debug(d)
        #logging.debug(form)

        #self.score = 0
        
    def __call__(self, rightscore, totalscore, leftscore, indscore, valalign, marcalign, ronalign, charalign, candidates, rotatechar, rotatemarc, rotateval, rotateron, rotatec1, rotatec2, cand1, cand2, cand1score, cand2score, dict1, dict2, dist1, dist2, site1, site2, right, left, ind):
        logging.debug("PrintScore Call Called")
        self.rightscore = rightscore
        self.leftscore = leftscore
        self.indscore = indscore
        self.valalign = valalign
        self.totalscore = totalscore
        self.fmarcalign = marcalign
        self.ronalign = ronalign
        self.charalign = charalign
        self.candidates = candidates
        self.rotatemarc = rotatemarc
        self.rotateval = rotateval
        self.rotateron = rotateron
        self.rotatechar = rotatechar
        self.rotatecand1 = rotatec1
        self.rotatecand2 = rotatec2
        self.cand1 = cand1
        self.cand2 = cand2
        self.cand1score = cand1score
        self.cand2score = cand2score
        self.dict1 = dict1
        self.dict2 = dict2
        self.dist1 = dist1
        self.dist2 = dist2
        self.site1 = site1
        self.site2 = site2
        self.right = right
        self.left = left
        self.ind = ind

class PopQuiz(Form):
    class Meta:
        csrf = False

    state = RadioField("What state do you live in?", 
    choices = [("Florida", "Florida")], validators=[InputRequired()])
    
    district = RadioField("Which Florida Disctrict do you reside in?", 
    choices = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"), ("11", "11"), ("12", "12"), ("13", "13"), ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"), ("18", "18"), ("19", "19"), ("20", "20"), ("21", "21"), ("22", "22"), ("23", "23"), ("24", "24"), ("25", "25"), ("26", "26"), ("27", "27")], validators=[InputRequired()])

    q1 = RadioField("1. Do you trust the sanctity of United States’ elections?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("Yes")])
    
    q2 = RadioField("2. Do you believe in a person’s right to reproductive freedom?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q3 = RadioField("3. Do you think the existing government is going in the right direction to benefit the people of the country?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("Yes")])

    q4 = RadioField("4. Do you think gun control laws and regulations should be changed?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q5 = RadioField("5. Do you think possession of guns should be allowed to everyone?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("Yes")])

    q6 = RadioField("6. Do you think there should be stricter rules and regulations on the use of money in political campaigns?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q7 = RadioField("7. Should there be policies to resolve the gap between the rich and the poor?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q8 = RadioField("8. Should there be more emphasis on the rehabilitation of criminals than punishment?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q9 = RadioField("9. Should all ethnicities be integrated into society?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q10 = RadioField("10. Have you been a member of the same party your whole life?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("Yes")])

    q11 = RadioField("11. Would you always support your country, whether it was right or wrong?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("Yes")])

    q12 = RadioField("12. Is it foolish to be proud of your country of birth, since no one chooses it?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q13 = RadioField("13. Do you think our race has many superior qualities, compared to other races?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("Yes")])

    q14 = RadioField("14. Is military action that defies international law sometimes justified?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("Yes")])

    q15 = RadioField("15. Do you think that there is a worrying fusion of information and entertainment nowadays?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q16 = RadioField("16. Do you only believe in traditional marriage: i.e. Man and Woman?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q17 = RadioField("17. Do you support the LGBTQ+ community?", 
    choices = [("Yes", "Yes"), ("No", "No"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("No")])

    q18 = RadioField("18. Are your beliefs about women's reproduction more pro-life or more pro-choice?", 
    choices = [("Pro-Life", "Pro-Life"), ("Pro-Choice", "Pro-Choice"), ("I don't know", "I don't know")],
    validators = [CheckAnswer("I don't know")])





