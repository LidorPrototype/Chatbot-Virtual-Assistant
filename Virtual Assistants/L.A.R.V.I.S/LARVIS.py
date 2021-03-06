from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pyttsx3 as pyttsx3
import speech_recognition as sr
import os
import sys
import re
import webbrowser
import subprocess
import smtplib
import wikipedia
from random import randrange
from time import strftime
import wolframalpha
import pytz
import requests
import calendar
from selenium import webdriver  # to control browser operations
from pyowm import OWM
import youtube_dl
# import vlc
import urllib
import time
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import win32com.client

# If modifying scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]
CALENDAR_OPTIONS = ["what do i have", "do i have plans", "am i busy"]
NOTE_OPTIONS = ["make a note", "write this down", "remember this"]


def larvis_response(audio):
    print(audio)
    response = pyttsx3.init()
    voices = response.getProperty('voices')
    response.setProperty('voice', voices[2].id)
    response.say(audio)
    response.runAndWait()


def larvis_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....ERROR....')
        command = larvis_command()
    return command.lower()


def larvis_web_search(find):
    if 'search google for' in find.lower():
        reg_ex = re.search('search (.+)', find)
        if reg_ex:
            url = "https://www.google.com.tr/search?q={}".format(find[17:])
            webbrowser.open(url)
            larvis_response('I\'ve searched Google for ' + find[17:] + ', here are the results')
        else:
            print('ERROR!')
            pass
    elif 'search youtube for' in find.lower():  # 10
        reg_ex = re.search('search (.+)', find)
        if reg_ex:
            domain = reg_ex.group(1)
            domain = domain[:7]
            print('Domain Is: ' + domain)
            url = 'https://www.' + domain + '.com/results?search_query=' + find[18:]
            webbrowser.open(url)
            larvis_response('I\'ve searched youtube for ' + find[18:] + ', here are the results')
        else:
            print('ERROR!')
            pass
    elif 'search wikipedia for' in find.lower():  # 11
        reg_ex = re.search('search (.+)', find)
        if reg_ex:
            webbrowser.open("https://en.wikipedia.org/wiki/" + (find[20:]))
            larvis_response('I\'ve searched wikipedia for ' + find[20:] + ', here is the result')
        else:
            print('ERROR!')
            pass


def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_events(day, service):
    # Calls the calender API
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                          timeMax=end_date.isoformat(), singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        larvis_response('No upcoming events found.')
    else:
        larvis_response(f"You have {len(events)} events on this day.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("+")[0])  # -
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time = start_time + "pm"
            larvis_response(event["summary"] + " at " + start_time)


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count('today') > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month < today.month and month != -1:
        year = year + 1
    if month == -1 and day != -1:
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week
        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7
        return today + datetime.timedelta(dif)
    if day != -1:
        return datetime.date(month=month, day=day, year=year)


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])


def give_date():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]  # e.g. Monday
    month_num = now.month
    day_num = now.day
    month_names = ['January', 'February', 'March', 'April', 'May',
                   'June', 'July', 'August', 'September', 'October', 'November',
                   'December']
    ordinal_numbers = ['1st', '2nd', '3rd', '4th', '5th', '6th',
                       '7th', '8th', '9th', '10th', '11th', '12th',
                       '13th', '14th', '15th', '16th', '17th',
                       '18th', '19th', '20th', '21st', '22nd',
                       '23rd', '24th', '25th', '26th', '27th',
                       '28th', '29th', '30th', '31st']
    larvis_response('Today is '
                    + weekday
                    + ' ' + month_names[month_num - 1]
                    + ' the ' + ordinal_numbers[day_num - 1]
                    + '.')


def larvis(user_input):
    print(user_input)
    if 'hello' in user_input:  # Greet Sofia
        day_time = int(strftime('%H'))
        if day_time < 12:
            larvis_response('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            larvis_response('Hello Sir. Good afternoon')
        else:
            larvis_response('Hello Sir. Good evening')
    elif "who are you" in user_input or "define yourself" in user_input:
        speak = '''Hello, I am LARVIS. Your personal Assistant. 
        I am here to make your life easier. You can command me to perform 
        various tasks such as calculating sums or opening applications etcetra'''
        larvis_response(speak)
    elif "who made you" in user_input or "created you" in user_input:
        speak = "I have been created by Lidor Eliyahu Shelef from Israel!"
        larvis_response(speak)
    elif "date" in user_input:
        give_date()
    elif 'open reddit' in user_input:  # open subreddit Reddit      #1
        reg_ex = re.search('open reddit (.*)', user_input)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        larvis_response('The Reddit content has been opened for you Sir.')
    elif 'open' in user_input:  # 2
        reg_ex = re.search('open (.+)', user_input)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain + '.com'
            webbrowser.open(url)
            larvis_response('The website you have requested has been opened for you Sir.')
        else:
            pass
    elif 'search' in user_input:
        larvis_web_search(user_input)
    elif 'what\'s up' in user_input or 'how are you' in user_input:  # 3
        arr = ['Chilling', 'I\'m Ok', 'Just Doing What I\'m Supposed To Do', 'Waiting For Your Command',
               'I\'m Just Fine', 'Just Dandy', 'Quite Alright', 'I\'m Find, Thank You', 'Just Developing Myself',
               'I\'m Good, And I\'m Here To Serve You']
        random = randrange(10)
        larvis_response(arr[random] + ' Sir!')
    elif 'joke' in user_input:  # 4
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"}
        )
        if res.status_code == requests.codes.ok:
            larvis_response(str(res.json()['joke']))
        else:
            larvis_response('oops!I ran out of jokes')
        print('joke has been told')
    elif 'email' in user_input:  # 5
        larvis_response('Who is the recipient?')
        recipient = larvis_command()
        if 'John' in recipient:
            larvis_response('What should I say?')
            content = larvis_command()
            # init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            # identify to server
            mail.ehlo()
            # encrypt session
            mail.starttls()
            # login
            mail.login('username', 'password')
            # send our mssg
            mail.sendmail('PERSON NAME', 'email address@w/e.com', content)
            # close mail connection
            mail.close()
            larvis_response('Email sent!')
    elif 'time' in user_input:  # 6
        import datetime
        now = datetime.datetime.now()
        larvis_response('Current time is %d , %d ' % (now.hour, now.minute))
    elif 'tell me about' in user_input:  # 7
        reg_ex = re.search('tell me about (.*)', user_input)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                larvis_response(ny.content[:500].encode('utf-8'))
        except Exception as e:
            larvis_response('Something Wrong happened Sir Here is The Problem Roots: ' + e)
    elif "calculate" in user_input.lower():  # 8
        app_id = "WOLFRAMALPHA_APP_ID"  # write your wolframalpha app_id here
        client = wolframalpha.Client(app_id)
        idx = user_input.lower().split().index('calculate')
        query = user_input.split()[idx + 1:]
        res = client.query(' '.join(query))
        answer = next(res.results).text
        larvis_response("The answer is " + answer)
    elif 'error' in user_input:
        larvis_response('I Can\'t Fucking Hear You Sir,Speak Up For,The Love Of God Speak Up, Bloody Israeli People!')
    elif 'help me' in user_input:
        larvis_response("""
            You can use these commands and I'll help you out:
            1... Open The SubReddit Website,
            2... Open xyz : replace xyz with any website name,
            3... Ask me how I\'m doing,
            4... Tell you a joke, I\'m Very Funny,
            5... Send email/email : Follow up questions such as recipient name, content will be asked in order,
            6... Time : Current system time,
            7... Tell me about xyz : tells you about xyz,
            8... Calculate anything you want,
            10... Search Youtube for a song,
            11... Search Wikipedia for anything you want,
            12... Search Google for anything you want,
            13... Make a note for you in notepad,
            14... Look at your calendar and give you your schedule for any day you want.
            """)
    elif 'exit' in user_input or 'goodbye' in user_input or 'good-bye' in user_input or 'good bye' in user_input \
            or 'bye' in user_input or 'shutdown' in user_input or 'good night' in user_input \
            or 'shut down' in user_input:
        larvis_response('Ok, Good-Bye Sir!')
        sys.exit()
    else:
        larvis_response('I Don\'t Know What To Say, Sorry Sir!')


# Driver Code
if __name__ == "__main__":
    WAKE = ["wake up", "larvis", "hey larvis", "good morning", "ok larvis"]
    SERVICE = authenticate_google()
    print("Start")
    while True:
        print("Listening")
        text = larvis_command()
        if text.count(WAKE[0]) > 0 or text.count(WAKE[1]) > 0 or text.count(WAKE[2]) > 0:
            larvis_response("Hello, What can i do for you?")
            text = larvis_command()
            for phrase in CALENDAR_OPTIONS:
                if phrase in text:
                    cheack_date = get_date(text)
                    if cheack_date:
                        get_events(cheack_date, SERVICE)
                    else:
                        larvis_response("I don't understand")
            for phrase in NOTE_OPTIONS:
                if phrase in text:
                    larvis_response("What would you like me to write down?")
                    note_text = larvis_command()
                    note(note_text)
                    larvis_response("I've made a note of that.")
            larvis(text)
        elif text == "terminate":
            print("Terminated by your command: " + text)
            sys.exit()
