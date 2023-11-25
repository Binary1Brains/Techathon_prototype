import random 
import json
import pickle
import numpy as np
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import nltk 
from nltk.stem import WordNetLemmatizer 

import pandas as pd

from keras.models import load_model

lemmatizer = WordNetLemmatizer ()

intents = json.loads (open ('intents.json').read())

words = pickle.load(open('words.pkl','rb'))

classes = pickle.load(open('classes.pkl','rb'))

model = load_model('chatbotmodel.h5')

def Remove ( sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def Word_set ( sentence ):
    sentence_words = Remove(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate ( words):
            if word == w :
                bag [i] = 1
    return np.arrray(bag)


def predict_class (sentence):
    bow = Word_set(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate (res) if r > ERROR_THRESHOLD ]
    results.sort ( key = lambda x : x[1], reverse = True)
    return_list=[]
    for r in results :
        return_list.append( {'intent': classes[r[0]],'probability': str(r[1])})
    return return_list


def GenResponse (intents_list , intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print ("Hi How can I help you")

def speak (text , rate = 120 ):
    engine.setProperty('rate',rate)
    print (text)
    engine.say (text)
    engine.runAndWait()
    
    
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty ('voice' , voices[0].id)
while True:
    message = input ("User:- ")
    ints = predict_class(message)
    res = GenResponse(ints,intents)
    speak (res)
    print ('Bot:- ', res)