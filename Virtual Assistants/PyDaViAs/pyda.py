import os
import gtts as gTTS
import playsound as playsound
import wx
import wolframalpha
import wikipedia
import win32com.client as wincl  # computer talk
import speech_recognition as sr  # computer hear
from pynput.keyboard import Key, Controller
import pyttsx3  # computer talk
import winreg


def assistant_speaks(output):
    engine.say(output)
    engine.runAndWait()


# function used to open application
# present inside the system.
def open_application(query):
    if "chrome" in query:
        assistant_speaks("Opening Google Chrome")
        handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\excel.exe")
        os.startfile(handle)
        return


def get_audio():
    rObject = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Speak...")
        # recording the audio using speech recognition
        # audio = rObject.listen(source, phrase_time_limit=5)
        audio = rObject.listen(source)
    print("Stop.")
    try:
        # text = rObject.recognize_google(audio, language='en-US')
        text = rObject.recognize_google(audio)
        print("You : ", text)
        return text
    except:
        assistant_speaks("Could not understand your audio, PLease try again !")
        return ""


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
                          pos=wx.DefaultPosition, size=wx.Size(450, 100),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                                wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          title="PyDa")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel, label="Hello I am Pyda the Python Digital Assistant. How Can I Help You?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(400, 30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def on_enter(self, event):
        query = self.txt.GetValue()
        query = query.lower()
        if query == '':
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                self.txt.SetValue(r.recognize_google(audio))
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request from Google Speech Recognition service; {0}".format(e))
        else:
            try:
                # wolframalpha
                app_id = "GVPRK9-QK7EP6RR7X"
                client = wolframalpha.Client(app_id)
                res = client.query(query)  # query
                answer = next(res.results).text
                print(answer)
                engine.say("The answer is " + answer)
            except:
                # wikipedia
                query = query.split(' ')
                query = ' '.join(query[2:])
                engine.say("Searched for " + query)
                print(wikipedia.summary(query))  # query


def process_text(input, MyFrame):
    if input == '':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            MyFrame.self.txt.SetValue(r.recognize_google(audio))
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request from Google Speech Recognition service; {0}".format(e))
    else:
        if "open" in input:
            # open_application("chrome")
            assistant_speaks("Not Implemented Yet! Need To Implement In The Future!!!")
        else:
            try:
                # wolframalpha
                app_id = "GVPRK9-QK7EP6RR7X"
                client = wolframalpha.Client(app_id)
                res = client.query(input)  # query
                answer = next(res.results).text
                print(answer)
                engine.say("The answer is " + answer)
            except:
                # wikipedia
                query = input.split(' ')
                query = ' '.join(query[2:])
                engine.say("Searched for " + query)
                print(wikipedia.summary(query))  # query


if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    assistant_speaks("What's your name Human?")
    name = 'Human'
    name = get_audio()
    assistant_speaks("Hello, " + name + '.')
    # speak = wincl.Dispatch("SAPI.SpVoice")
    # speak.Speak("Welcome Back Sir!")
    keyboard = Controller()
    # app.MainLoop()
    while True:
        assistant_speaks("What can i do for you?")
        text = get_audio().lower()
        if text == 0:
            continue
        if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
            assistant_speaks("Ok bye, " + name + '.')
            break
        # calling process text to process the query
        process_text(text, frame)

"""
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
"""
