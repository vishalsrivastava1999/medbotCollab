import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
import json
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import random
from sklearn.metrics.pairwise import cosine_similarity

import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)


'''
text1 = 'This is a foo bar sentence .'
text2 = 'This sentence is similar to a foo bar sentence .'

vector1 = text_to_vector(text1)
vector2 = text_to_vector(text2)

cosine = get_cosine(vector1, vector2)

print 'Cosine:', cosine
'''


#new libraries
import difflib

sr = pd.read_csv('/home/ragnar/AI data/docbot/finaldataset.csv', engine='python')
sr = np.array(sr)
dis = sr[:,1]
symp = sr[:,2]

dis = np.array(dis)
symp = np.array(symp)

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

def getSymptoms():
    print('Please tell me about your symptoms')
    inp = input()
    sent = sent_tokenize(inp)
    filt = stopWords(inp)
    
    #compare input with csv file with filtered sentence
    i1=i2=i3=0
    max1=0
    max2=0
    max3=0
    #print(symp.size)
    for i in range(symp.size):
        #sequence = difflib.SequenceMatcher(isjunk=None, a=filt, b=symp[i])
        #sequence = difflib.SequenceMatcher(a=inp,b=symp[i])
        vector1 = text_to_vector(inp)
        vector2 = text_to_vector(symp[i])
        sequence = get_cosine(vector1, vector2)
        diff = sequence*100
        if(diff>max1):
            max3=max2
            max2=max1
            max1=diff
            i1=i
        elif(diff>max2):
            max3=max2
            max2=diff
            i2=i
        elif(diff>max3):
            max3=diff
            i3=i

    print('Diagnosed Diseases are:')
    if(i1!=i2!=i3):
        print(dis[i1])
        print(dis[i2])
        print(dis[i3])
    else:
        print(dis[i1])


Sym = getSymptoms()

