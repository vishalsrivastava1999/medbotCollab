import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
import json
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import random
import re

#greeting file
gr = pd.read_csv('GreetingDataset.csv', engine='python')
gr = np.array(gr)
gd = gr[:,1]

#thankyou file
tu = pd.read_csv('ThankYou.csv', engine='python')
tu = np.array(tu)
td = gr[:,0]

#welcome file
wc = pd.read_csv('WelcomeDataset.csv', engine='python')
wc = np.array(wc)
wd = wc[:,0]

#age file
ag = pd.read_csv('AGEDataset.csv', engine='python')
ag = np.array(ag)
ad = ag[:,1]

#bye file
by = pd.read_csv('BYEDataset.csv', engine='python')
by = np.array(by)
bd = by[:,1]

#name file
nm = pd.read_csv('NameDataset.csv', engine='python')
nm = np.array(nm)
nd = nm[:,0]

def stopWords(text):
    #text is a sentence
    stopw = set(stopwords.words('english'))
    filtered = []
    words = word_tokenize(text)
    for i in words:
        if i not in stopw:
            filtered.append(i)
    return filtered

def stemming(text):
    #text could be a sent or word
    ps = PorterStemmer()
    empty = []
    for w in text:
        empty.append(w)
    return empty

def getAge(text):
    #text is a sentence(string)
    #expected output: age in number
    filtered = stopWords(text)
    for i in filtered:
        try:
            age1 = int(i)
        except Exception as e:
            print("Please enter valid age")
            askAge()
            continue
    return age1        

def getName(text):
    #text is a/many sentence
    #takes the user response and returns name of the user
    filtered = stopWords(text)
    stemmed = stemming(filtered)
##    print("stemmed",stemmed)
    tag = nltk.pos_tag(stemmed)
    #print(tag)
    noun=[]
    for i in range(len(tag)):
##        print(tag[i][1])
        if ((str(tag[i][1])=='NN' or str(tag[i][1])=='NNP') and str(tag[i][0])!='name'):
            noun.append(tag[i][0])
##    print(noun)
##    chunkGram = r"""Chunk: {<NN+>*}  """
##    chunkParser = nltk.RegexpParser(chunkGram)
##    chunked = chunkParser.parse(tag)
##    print(chunked)
##    for i in chunked:
##        if i != ('name', 'NN'):
##            name = i
##            print('i=',i[0])
##
##    print(name[0])
    return noun

def greet():
    k = random.randint(0,50)
    print(gd[k%11])

def askName():
    k = random.randint(0,50)
    print(nd[k%7])
    inp = input()
    return inp

def askAge():
    k = random.randint(0,50)
    print(ad[k%6])
    inp = input()
    return inp

def Bye():
    k = random.randint(0,50)
    print(bd[k%20])

def askGender():
    print('Are you a Male or a Female?')
    inp = input()
    return inp

def sorry():
    print('I\'m sorry I could not understand that. Let\'s try again.')

def getGender(text):
    #text is a sentence(string)
    #expected output: 'Male' or 'Female'
    filtered = stopWords(text)
    flag=0
    for i in filtered:
        if i.lower()=='male' or i.lower()=='female':
            gender = i
            flag=1
    if flag!=1:
        return 0
    else:
        return gender

def getEmail():
    email = input ("Please type in an email address \n")
    print("")
    if re.match("\A(?P<name>[\w\-_]+)@(?P<domain>[\w\-_]+).(?P<toplevel>[\w]+)\Z",email,re.IGNORECASE):
        print("")
    else:
        print("Please enter a valid email address")
        getEmail()
    return email

def smokeAndAlc():
    print('Do you smoke?')
    inp1 = input()
    res1=0
    for i in inp1:
        stem = stemming(i)
        if 'yes' in stem or 'yea' in stem or 'yeah' in stem:
            res1=1
    print('Do you consume Alcohol?')
    inp2 = input()
    res2=0
    for i in inp2:
        stem = stemming(i)
        if 'yes' in stem or 'yea' in stem or 'yeah' in stem:
            res2=1
    return (res1*10)+res2
'''
def postalValidate(S):
   S = S.replace(" ","") 
   if len(S) != 6 or S.isalpha() or S.isdigit(): 
      return False  
   if not S[0:5:2].isalpha(): 
      return False  
   if not S[1:6:2].isdigit(): 
      return False 
   return S.upper()
'''

def getZip():
    S = input()
    S = S.replace(" ","")
    if len(S) != 6 or S.isalpha() or S.isdigit():
        return False
    if not S[0:5:2].isalpha():
        return False
    if not S[1:6:2].isdigit():
        return False
    return S.upper()

def extDisease():
    print('Before we ask you your symptoms, we would like to know your health status.')
    print('If yout have any existing Medical Conditions or Problems, please provide them here.')
    print('If you dont, you can reply with a \'no\'')
    inp = input()
    tok = word_tokenize(inp)
    fl=0
    for i in tok:
        stem = stemming(i)
        for i in tok:
            if 'no' in tok:
                fl=1
                break
    if fl==0:
            return inp
    else:
        return 'Nothing Sevre'

def getSymptoms():
    inp = input()
    filtered = stopWords(inp)
    stemmed = stemming(filtered)
    
    

#Starting the conversation 
greet()
print('I\'m Novus, your personal health assistant.')
print("I can help you find out what's going on with a simple symptom assessment.")
ufName = askName()
name = getName(ufName)
ufAge = askAge()
age = getAge(ufAge)
ufGender = askGender()
gender = getGender(ufGender)
while gender==0:
    sorry()
    ufGender = askGender()
    gender = getGender(ufGender)
print('To help you keep a record of your symptoms and enable us to provide you with better assistance, we would like you to provide us with your email. This is mandatory.')
email = getEmail()
print('Your ZipCode would enable us to provide personalised suggestions for hospitals. This is mandatory.')
zip = getZip()
sa=smokeAndAlc()
#sa = (smoke*10)+alc
existingDiseases = extDisease()

print('name = {}, age = {}'.format(name[0],age))
#print Everything
print(name, age, gender, email, zip, sa, existingDiseases)
print('Okay {} '.format(name[0]))

import symptom1
Bye()