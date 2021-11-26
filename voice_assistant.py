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
from datetime import datetime

#Things to do
#1. remove additional while loops.  ✅ 
#2. find alternative for pyjoke  
#3. Try using weather api(openweather)  

operations = ['+','-','x','/','into','by','cross','power']

def speak(audio):
    '''Speaks out the text present in the string 'audio' '''
    tts= gTTS(text=audio, lang = 'en-uk')
    r = random.randint(1,1000000)
    audiofile = 'audio'+str(r)+'.mp3'
    tts.save(audiofile)
    print(audio)
    playsound.playsound(audiofile)
    os.remove(audiofile)
    time.sleep(0.3)

def getUserName():
    '''Fetches the name of the user. '''
    speak('What may I call you')
    name=takeCommand().capitalize()
    return name

def wish(hour):
    '''Greets the user according to the time of the day. '''
    greeting=''
    if(hour<12):
        greeting = 'Good Morning, '
    elif hour>=12 and hour <=3:
        greeting = 'Good Afternoon, '
    else:
        greeting = 'Good Evening, '  
    name=getUserName()
    if(name==''):
        name=getUserName()
    #print('Good Evening Rohith.')
    speak(greeting+name)
    
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
        takeCommand()
        return ''

async def getweather():
    '''Fetches the weather in Bangalore using python_weather package'''
    client = python_weather.Client(format=python_weather.IMPERIAL)
    weather = await client.find("Bangalore")
    #print(weather.current.temperature)
    a='The temperature in bangalore is currently '+ str((weather.current.temperature-32)*5//9)+' degree celsius'
    #print(a)
    speak(a)
    await client.close()

def calc(l):
    '''Performs basic mathematical calculations'''
    index=0
    if '+' in l:
        index=l.index('+')
    elif '-' in l:
        index=l.index('-')
    elif 'into' in l :
        index=l.index('into')
    elif 'cross' in l:
        index=l.index('cross')
    elif 'x' in l:
        index=l.index('x')
    elif 'by' in l:
        index = l.index('by')
    elif '/' in l:
        index = l.index('/')
    elif 'power' in l:
        index = l.index("power")
    operand=l[index]
    a=int(l[index-1])
    b=int(l[index+1])
    if operand == '+':
        return a+b
    if operand == '-':
        return a-b
    if operand == 'into' or operand =='cross' or operand == 'x':
        return a*b
    if operand == 'by' or operand == '/':
        return a/b
    if operand == 'power':
        return a**b

def performCommand(query):

    if 'who are you' in query:
        speak('I am Groot')

    if 'wikipedia' in query:
        webbrowser.open('https://www.wikipedia.org/', new=2)
        query='exit'

    if 'youtube' in query:
        speak('what should I search')
        query2=takeCommand()
        # while(query2==''):
        #     query2=takeCommand()
        webbrowser.open('https://www.youtube.com/results?search_query='+query2, new=2)
        time.sleep(3)
        speak('Shall I play the first recomended video?')
        query3=takeCommand()
        # while(query3==''):
        #     query3=takeCommand()
        print(query3)
        if query3 in ['yes','yeah','ok','sure','okay','yep'] :
        #pyautogui.moveTo(704,309)
            pyautogui.click(x=704,y=309)
        #try adding pyautogui here as well
        query='exit'

    if 'joke' in query:
        joke= pyjokes.get_joke(language="en", category="neutral")
        #print(joke)
        speak(joke)
        speak('Would you like to hear another joke?')
        query=takeCommand()
        if(query=='yes'):
            performCommand('joke')
        elif(query=='no'):
            speak('Okay. Anything else that I may help you with?')

    if 'weather' in query:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(getweather())
    
    if 'google' in query:
        speak('What should I search?')
        query2=takeCommand()
        # while(query2==''):
        #     query2=takeCommand()
        #pyautogui.typewrite(query2,interval=0.1)
        webbrowser.open('https://www.google.co.in/search?q='+query2)
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
        # while(query2==''):
        #     query2=takeCommand()
        pyautogui.typewrite(query2,interval=0.1)
        pyautogui.press('enter')
        query='exit'
    
    
    if any(i in query for i in operations): #checks if query matches any element from the list 'operations'
        l=query.split()
        #print(l)
        speak(str(calc(l)))

    return query


if __name__ == "__main__":

    present_time = datetime.now()
    #print(present_time)
    wish(int(present_time.hour))
    query = ''
    #print('How may I help you?')
    speak('How may I help you?')
    while(query!='exit'):
        query = takeCommand()  
        query=performCommand(query)     


