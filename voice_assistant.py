import speech_recognition as sr
import webbrowser
#import python_weather 
#import asyncio
import pyjokes
import pyautogui
import os
from gtts import gTTS
import random
import playsound
import time
from datetime import datetime
import requests,json
import wolframalpha

#Things to do
#1. remove additional while loops.  ✅ 
#2. find alternative for pyjoke  
#3. Try using weather api(openweather)   ✅
#4. Remove unwanted commented code 

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
    global name 
    name = takeCommand().capitalize()
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
        print("Please say that again .")
        speak('Please say that again .')
        takeCommand()
        return ''

# async def getweather():
#     '''Fetches the weather in Bangalore using python_weather package'''
#     client = python_weather.Client(format=python_weather.IMPERIAL)
#     weather = await client.find("Bangalore")
#     #print(weather.current.temperature)
#     a='The temperature in bangalore is currently '+ str((weather.current.temperature-32)*5//9)+' degree celsius'
#     #print(a)
#     speak(a)
#     await client.close()
def weather():
    api_key = '44a26f75a38784ba68059ac9d623a4d5'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = 'Bangalore'
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
         y = x["main"]
         current_temperature = round(y["temp"]-273.15,2)
         min_temperature = round(y["temp_min"]-273.15 , 2)
         max_temperature = round(y["temp_max"]-273.15 , 2)
         current_pressure = y["pressure"]
         current_humidity = y["humidity"]
         z = x["weather"]
         weather_description = z[0]["description"]
         weather_info=f'The Temperature in Bengaluru is currently{str(current_temperature)} degree Celsius with a low of {min_temperature} and a high of {max_temperature}.\nHumidity level is {str(current_humidity)} %.\n'
         speak(weather_info)
    else:
        print(" City Not Found ")

def fetch_time():
    '''Tells current time'''
    s=''
    if(present_time.hour<12):
        s='a.m.'
    else:
        s='p.m.'

    t='The time is '+str(present_time.hour)+' : '+str(present_time.minute)+' '+s
    speak(t)

def fetch_date():
    '''Tells current date'''
    d=f"Today's date is {str(present_time.day)} , {str(present_time.month)} , {str(present_time.year)}"
    speak(d)
    
def calc(l):
    '''Performs basic mathematical calculations of two numbers'''
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

    elif 'wikipedia' in query:
        webbrowser.open('https://www.wikipedia.org/', new=2)
        query='exit'

    elif 'youtube' in query:
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

    elif 'joke' in query:
        joke= pyjokes.get_joke(language="en", category="neutral")
        #print(joke)
        speak(joke)
        speak('Would you like to hear another joke?')
        query=takeCommand()
        if(query=='yes'):
            performCommand('joke')
        elif(query=='no'):
            speak('Okay. Anything else that I may help you with?')

    elif 'weather' in query:
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(getweather())
        weather() 
    
    elif 'google' in query:
        speak('What should I search for, '+name+'?')
        query2=takeCommand()
        if(query2 is not exit):
        # while(query2==''):
        #     query2=takeCommand()
        #pyautogui.typewrite(query2,interval=0.1)
            webbrowser.open('https://www.google.co.in/search?q='+query2)
            pyautogui.press('enter')
            query='exit'
    
    elif 'location' in query:
        speak('What is the location?')
        location = takeCommand()
        url = 'https://www.google.nl/maps/place/' + location + '/&amp;'
        speak('Here is the location')
        webbrowser.open(url)
        query = 'exit'
    
    elif'terminal' in query:
        os.system("gnome-terminal")
        speak('What should I search?')
        query2=takeCommand()
        # while(query2==''):
        #     query2=takeCommand()
        pyautogui.typewrite(query2,interval=0.1)
        pyautogui.press('enter')
        query='exit'
    
    elif 'time' in query:
        fetch_time() 
    
    elif 'date' in query:
        fetch_date()
    
    elif any(i in query for i in operations): #checks if query matches any element from the list 'operations'
        l=query.split()
        #print(l)
        speak(str(calc(l)))

    elif 'thank you' in query:
        thankYou='You are welcome'+name
        speak(thankYou)
    
    else:
        try:
            api='U2UHK6-4H49EG2LR3'
            client = wolframalpha.Client(api)
            res = client.query(query)
            answer = next(res.results).text
            print('Fetching your result.......')
            speak(answer)
        except:
            speak("Sorry could't find anything on that")

    return query


if __name__ == "__main__":

    global present_time
    present_time = datetime.now()
    #print(present_time)
    wish(int(present_time.hour))
    query = ''
    #print('How may I help you?')
    speak('How may I help you?')
    while(query!='exit'):
        query = takeCommand()  
        query=performCommand(query)     


