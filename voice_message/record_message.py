#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 13:34:16 2020

@author: erdem
"""


import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from threading import Thread
from datetime import datetime
import os

fs = 44100
unit_record_time = 1

voice_records = []

stop = False
def start_recording():
    global voice_records
    global stop
    while not stop:
        record = sd.rec(int(unit_record_time * fs), samplerate=fs, channels=2)
        sd.wait()
        voice_records.append(record)

Thread(target = start_recording).start()

while True:
    inp = input()
    if inp.lower() == 'q':
        stop = True
        voice = np.vstack(voice_records)
        break

now = datetime.now()
file_name = f"{now.strftime('%d%m%Y_%H_%M_%S')}.wav"
file_path = os.path.join(os.getcwd(), "Messages")
if not os.path.exists(file_path):
    os.mkdir(file_path)

write(os.path.join(file_path, file_name), fs, voice)

