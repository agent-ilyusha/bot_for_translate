# -- coding: utf-8

import speech_recognition as sr



def func_speech(path_wav):
    try:
        speech = sr.Recognizer()
        with sr.AudioFile(path_wav) as source:
            audiof = speech.record(source)
            return speech.recognize_google(audiof, language='ru')
    except sr.exceptions.UnknownValueError():
        return 'Текст не распознан'


