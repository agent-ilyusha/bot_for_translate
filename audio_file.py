# -- coding: utf-8
import soundfile as sf
from gtts import gTTS
import os


def func_soundFile(path):
    data, samplerate = sf.read(path)
    src = f'C:\\Users\\1\\Desktop\\new_bot\\audio_wav\\{path[37:-4]}.wav'
    sf.write(src, data, samplerate)
    return src


def func_gtts(text, path):
    tts = gTTS(text=text, lang='ru')
    path_file = f'C:\\Users\\1\\Desktop\\new_bot\\audio_ogg\\{path[37:-4]}.ogg'
    with open(path_file, 'wb') as audio:
        tts.write_to_fp(audio)

    return path_file


