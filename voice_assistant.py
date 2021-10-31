import speech_recognition as sr
import webbrowser
import python_weather 
import asyncio
import pyjokes
import pyautogui
import os
from gtts import gTTS
import random
import playsound
import time

def speak(audio):
    tts= gTTS(text=audio, lang = 'en-uk')
    r = random.randint(1,1000000)
    audiofile = 'audio'+str(r)+'.mp3'
    tts.save(audiofile)
    print(audio)
    playsound.playsound(audiofile)
    os.remove(audiofile)
    time.sleep(0.3)

def getUserName():
    speak('What may I call you')
    name=takeCommand()
    return name

def wish():
    name=getUserName()
    if(name==''):
        name=getUserName()
    #print('Good Evening Rohith.')
    speak('Good Evening, '+name)
    
def takeCommand():
    '''To take microphone input and return string output'''
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print('Recognizing...')
        query = r.recognize_google(audio,language='en-US').lower()
        print(f'User said {query}')
        return query
    except Exception as e:
        #print(e)
        print("Say that again please.")
        speak('Please say that again .')
        return ''

async def getweather():

    client = python_weather.Client(format=python_weather.IMPERIAL)

    weather = await client.find("Bangalore")
    #print(weather.current.temperature)
    a='The temperature in bangalore is currently '+ str((weather.current.temperature-32)*5//9)+' degree celsius'
    print(a)
    speak(a)
    await client.close()

def calc(l):
    if '+' in l:
        index=l.index('+')
    elif '-' in l:
        index=l.index('-')
    elif 'into' in l:
        index=l.index('into')
    elif 'by' in l:
        index = l.index('by')
    operand=l[index]
    a=int(l[index-1])
    b=int(l[index+1])
    if operand == '+':
        return a+b
    if operand == '-':
        return a-b
    if operand == 'into':
        return a*b
    if operand == 'by':
        return a/b

def performCommand(query):

    if 'who are you' in query:
        speak('I am Priya, your voice assistant')

    if 'wikipedia' in query:
        webbrowser.open('https://www.wikipedia.org/', new=2)
        query='exit'

    if 'youtube' in query:
        speak('what should I search')
        query2=takeCommand()
        if(query2==''):
            query2=takeCommand()
        webbrowser.open('https://www.youtube.com/results?search_query='+query2, new=2)
        #try adding pyautogui here as well
        query='exit'

    if 'joke' in query:
        joke= pyjokes.get_joke()
        print(joke)
        speak(joke)

    if 'weather' in query:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(getweather())
    
    if 'google' in query:
        webbrowser.open('https://www.google.co.in/')
        speak('What should I search?')
        query2=takeCommand()
        if(query2==''):
            query2=takeCommand()
        pyautogui.typewrite(query2,interval=0.1)
        pyautogui.press('enter')
        query='exit'
    
    if 'location' in query:
        speak('What is the location?')
        location = takeCommand()
        url = 'https://www.google.nl/maps/place/' + location + '/&amp;'
        speak('Here is the location')
        webbrowser.open(url)
        query = 'exit'
    
    if'terminal' in query:
        os.system("gnome-terminal")
        speak('What should I search?')
        query2=takeCommand()
        if(query2==''):
            query2=takeCommand()
        pyautogui.typewrite(query2,interval=0.1)
        pyautogui.press('enter')
        query='exit'

    if '+' in query or '-' in query or 'into' in query or 'by' in query:
        #format a+b 
        l=query.split()
        #print(l)
        speak(str(calc(l)))

    return query


if __name__ == "__main__":

    wish()
    query = ''
    #print('How may I help you?')
    speak('How may I help you?')
    while(query!='exit'):
        query = takeCommand()  
        query=performCommand(query)     


