# -*- coding: utf-8 -*-
"""
Created on Mon May 31 11:42:50 2021

@author: Saranya
"""

from flask import Flask,render_template,redirect
import warnings
warnings.filterwarnings('ignore')

app = Flask("__name__")

import speech_recognition as sr
import pyttsx3
import pywhatkit
import pyautogui
import datetime
import wikipedia
import pyjokes
import webbrowser
import sys




listener = sr.Recognizer()

def engine_talk(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def user_commands():
    try:
        with sr.Microphone() as source:
            engine_talk('Start speaking')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa','')
                print(command)
    except:
        pass
    return command

def run_alexa():
    
    command = user_commands()
   
    #Play music 
    if 'play' in command:
        command = command.replace('play','')
        engine_talk('Playing'+command)
        pywhatkit.playonyt(command)
        
    #Current Time
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        engine_talk('The current time is' +time)
        
    #Search in Wikipedia
    elif 'who is' in command:
        name = command.replace('who is' , '')
        info =  wikipedia.summary(name, 1)
        print(info)
        engine_talk(info)
        
    #Joke
    elif 'joke' in command:
        engine_talk(pyjokes.get_joke())
        
    #Screenshot
    elif 'screenshot' in command:
        pic = pyautogui.screenshot()
        pic.save('D:/screenshot/SS.png')
        engine_talk('screenshot taken')
        
    #Search
    elif 'search' in command:
        search_term = command.split('for')[-1]
        url='https://google.com/search?q='+search_term
        webbrowser.get().open(url)
        engine_talk('Here is what I found for on google')
        
    elif 'stop' in command:
        engine_talk('Bye')
        sys.exit()        
    
    else:
        engine_talk('I could not hear you properly')  
        
        
@app.route('/')
def hello():
    return render_template("alexa.html")

@app.route("/home")
def home():
    return redirect('/')

@app.route('/',methods=['POST', 'GET'])
def submit():
    while True:
        run_alexa()
    return render_template("alexa.html")
        

if __name__ =="__main__":
    app.run(debug=True)
