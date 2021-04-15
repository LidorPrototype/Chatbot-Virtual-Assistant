from gtts import gTTS
from random import randrange
import speech_recognition as sr
import os
import webbrowser
import smtplib
import pyttsx3
import re
import requests
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

global var_exit
var_exit = True


# Make The VA Talk
def talk_to_me(audio):
    print(audio)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)
    engine.say(audio)
    engine.runAndWait()


# Listen To Commands
def my_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        talk_to_me('What Can I Do For You Sir?')
        print('Talk Now!')
        # r.pause_threshold = 1
        # r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said:' + command + '\n')
    # loop back to listening if the command is without an answer for the VA
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        # assistant(my_command())
        command = 'error'
    return command


# if for making the command
def assistant(command):
    print(command)
    if 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain + '.com'
            webbrowser.open(url)
            talk_to_me('The website you have requested has been opened for you Sir.')
        else:
            pass
    elif 'search youtube' in command:
        reg_ex = re.search('search (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            domain = domain[:7]
            print('Domain Is: ' + domain)
            url = 'https://www.' + domain + '.com/results?search_query=' + command[14:]
            webbrowser.open(url)
            talk_to_me('The website you have requested has been opened for you Sir.')
        else:
            print('ERROR!')
            pass
    elif 'what\'s up' in command or 'how are you' in command:
        arr = ['Chilling', 'I\'m Ok', 'Just Doing What I\'m Supposed To Do', 'Waiting For Your Command',
               'I\'m Just Fine', 'Just Dandy', 'Quite Alright', 'I\'m Find, Thank You', 'Just Developing Myself',
               'I\'m Good, And I\'m Here To Serve You']
        random = randrange(10)
        talk_to_me(arr[random] + ' Sir!')
    elif 'joke' in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"}
        )
        if res.status_code == requests.codes.ok:
            talk_to_me(str(res.json()['joke']))
        else:
            talk_to_me('oops!I ran out of jokes')
        print('joke has been told')
    elif 'email' in command:
        talk_to_me('Who is the recipient?')
        recipient = my_command()
        if 'John' in recipient:
            talk_to_me('What should I say?')
            content = my_command()
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
            talk_to_me('Email sent!')
    elif 'error' in command:
        talk_to_me('I Can\'t Fucking Hear You Sir,Speak Up For,The Love Of God Speak Up, Bloody Israeli People!')
    elif 'exit' in command or 'goodbye' in command or 'good-bye' in command or 'good bye' in command \
            or 'bye' in command or 'bye-bye' in command or 'good night' in command:
        talk_to_me('Ok, Good-Bye Sir!')
        global var_exit
        var_exit = False
    else:
        talk_to_me('I Don\'t Know What To Say, Sorry Sir!')


while var_exit:
    assistant(my_command())
