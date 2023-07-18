######################### Necessary Packages ####################
from sentence_transformers import SentenceTransformer, util
import speech_recognition as sr
import simpleaudio as sa
# from playsound import playsound
import json
import os
# from multiprocessing import Process
from threading import Thread
import time
######################### Environment Variables ######################
f = open('config.json')

data = json.load(f)
route_faq = data['FAQ']
route_mainFlow = data['mainFlow']
audio_format = data['format']
threshold = data['threshold']
FAQs = data['FAQs']
num_mainflow = len(os.listdir(route_mainFlow))-1
audio_length = data['audio_length']
######################### speech to text ###########################
model = SentenceTransformer('all-MiniLM-L6-v2')
query = ""
def get_similarity(text1, text2):
    en_1 = model.encode(text1)
    en_2 = model.encode(text2)
    result = util.cos_sim(en_1, en_2)
    result_float = result.item()
    return result_float
def play_audio(name):
    wave_obj = sa.WaveObject.from_wave_file(name)
    play_obj = wave_obj.play()
    play_obj.wait_done()
######################### Calculate semantic similarity #################
def similarity(voice):
    for i in range(len(FAQs)):
        s = get_similarity(voice, FAQs[i])
        if s > threshold:
            print(s)
            print(FAQs[i])
            return i
    return -1
######################### Microphone recognition ##################################
r = sr.Recognizer()
def takeCommand():
    with sr.Microphone() as source:
        print('Listening....')
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=5)
    try:
        print("Recognizing.....")
        mic = r.recognize_google(audio, language='en-US')
        # mic = r.recognize_sphinx(audio, language='en-US')
        # mic = r.recognize_vosk(audio, language='en-US')
        # mic = r.recognize_whisper(audio, language='en-US')
        print(" Customer Said: {} \n".format(mic))
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return -1
    except sr.RequestError:
        print("Sorry, my speech service is not available right now.")
        return ""
    return mic.lower()

def timer(t):
    global query
    time.sleep(t)
    query = takeCommand()
    
######################### BOT ##############################
def bot():
    for i in range(num_mainflow):
        print(i+1)
        if i == (num_mainflow -1):
            play_audio(route_mainFlow + str(i+1) + audio_format)
            exit()
        threadlist = []
        threadlist.append(Thread(target=play_audio, args=[route_mainFlow + str(i+1) + audio_format]))
        threadlist.append(Thread(target=timer, args=[audio_length[i]]))
        
        for t in threadlist:
            t.start()

        for t in threadlist:
            t.join()
        print(query)
        # play_audio(route_mainFlow + str(i+1) + audio_format)
        # query = takeCommand()
        if query == -1:
            if i == 0:
                exit()
            else:
                continue
        n = similarity(query)
        if n == -1:
            continue
        elif n == 10:
            play_audio(route_mainFlow + 'end' + audio_format)
            exit()
        play_audio(route_faq + FAQs[n] + audio_format)

if __name__ == "__main__":
    bot()