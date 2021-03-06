import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
# import youtube_dl
# import vlc
import urllib
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime
import win32com.client


def sofiaResponse(audio):
    print(audio)
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(audio)


def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command


def assistant(command):
    if 'hello' in command:  # Greet Sofia
        day_time = int(strftime('%H'))
        if day_time < 12:
            sofiaResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            sofiaResponse('Hello Sir. Good afternoon')
        else:
            sofiaResponse('Hello Sir. Good evening')

    elif 'joke' in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            sofiaResponse(str(res.json()['joke']))
        else:
            sofiaResponse('oops!I ran out of jokes')

    elif 'open reddit' in command:  # open subreddit Reddit
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        sofiaResponse('The Reddit content has been opened for you Sir.')

    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sofiaResponse('The website you have requested has been opened for you Sir.')
        else:
            print('ERROR')
            sofiaResponse('Some Error Happened Sir!')
            pass

    elif 'email' in command:
        sofiaResponse('Who is the recipient?')
        recipient = myCommand()
        if 'rajat' in recipient:  # rajat meaning? why rajat?
            sofiaResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('your_email_address', 'your_password')
            mail.sendmail('sender_email', 'receiver_email', content)
            mail.close()
            sofiaResponse('Email has been sent successfuly. You can check your inbox.')
        else:
            sofiaResponse('I don\'t know what you mean!')

    # below got problem
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname + ".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
            sofiaResponse('I have launched the desired application')

    # below got problem
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            sofiaResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature'
                          ' is %0.2f degree celsius' % (city, k, x['temp_max'], x['temp_min']))

    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    # below got problem
    elif 'play me a song' in command:
        sofiaResponse('Not Implemented Correctly Sir, You Still Have Some Bugs To Fix In Here Sir!')
        # path = '/Users/nageshsinghchauhan/Documents/videos/'
        # folder = path
        # for the_file in os.listdir(folder):
        #     file_path = os.path.join(folder, the_file)
        #     try:
        #         if os.path.isfile(file_path):
        #             os.unlink(file_path)
        #     except Exception as e:
        #         print(e)
        # sofiaResponse('What song shall I play Sir?')
        # mySong = myCommand()
        # if mySong:
        #     flag = 0
        #     url = "https://www.youtube.com/results?search_query=" + mySong.replace(' ', '+')
        #     response = urllib.urlopen(url)  # originally urllib2 was here
        #     html = response.read()
        #     soup1 = soup(html, "lxml")
        #     url_list = []
        #     for vid in soup1.findAll(attrs={'class': 'yt-uix-tile-link'}):
        #         if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
        #             flag = 1
        #             final_url = 'https://www.youtube.com' + vid['href']
        #             url_list.append(final_url)
        # url = url_list[0]
        # ydl_opts = {}
        # os.chdir(path)
        # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #     ydl.download([url])
        # vlc.play(path)
        # if flag == 0:
        #     sofiaResponse('I have not found anything in Youtube ')

    # below got problem
    elif 'change wallpaper' in command:
        folder = '/Users/nageshsinghchauhan/Documents/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key  # pic from unspalsh.com
        f = urllib.urlopen(url)  # urllib2 was originally here
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urllib.urlretrieve(photo,
                           "/Users/nageshsinghchauhan/Documents/wallpaper/a")  # Location where we download the image to
        subprocess.call(["killall Dock"], shell=True)
        sofiaResponse('wallpaper changed successfully')

    # below got problem
    elif 'news for today' in command:
        sofiaResponse('Not Implemented Correctly Sir, You Still Have Some Bugs To Fix In Here Sir!')
        # try:
        #     news_url = "https://news.google.com/news/rss"
        #     Client = urlopen(news_url)
        #     xml_page = Client.read()
        #     Client.close()
        #     soup_page = soup(xml_page, "xml")
        #     news_list = soup_page.findAll("item")
        #     for news in news_list[:15]:
        #         sofiaResponse(news.title.text.encode('utf-8'))
        # except Exception as e:
        #     print('ERROR! THE ERROR IS: ' + e)

    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                sofiaResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
            sofiaResponse('Something Wrong happened Sir Here is The Problem Roots: ' + e)

    elif 'help me' in command:
        sofiaResponse("""
            You can use these commands and I'll help you out:
            1... Open reddit subreddit : Opens the subreddit in default browser.
            2... Open xyz.com : replace xyz with any website name
            3... Send email/email : Follow up questions such as recipient name, content will be asked in order.
            4... Current weather in {city name} : Tells you the current condition and temperature
            5... Ask me how I\'m doing
            6... (Not Implemented Yet Sir!) play me a video : Plays song in your VLC media player
            7... change wallpaper : Change desktop wallpaper
            8... news for today : reads top news of today
            9... time : Current system time
            10... top stories from google news (R.S.S. feeds)
            11... tell me about xyz : tells you about xyz
            """)

    elif 'shutdown' in command or 'shut down' in command:
        sofiaResponse('Bye bye Sir. Have a nice day')
        sys.exit()


sofiaResponse('Hello Sir! My name is Sofia and I will be your assistant, You can ask me to do stuff for you, '
              'or simply say "help me" and I will tell you everything I can do for you.')

while True:
    assistant(myCommand())
