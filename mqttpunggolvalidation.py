import numpy as np
import sounddevice as sd 
import soundfile as sf
import json
import pandas as pd
import math


optimaldistance = 1 #Punggol MSCP
numofspeakers = 1

def validation(masker, gain):
    validationmasker, validationfs = sf.read(maskerpath + masker + '.wav')
    gainindex = gain - 46
    for maskerkey in calib:
        if masker == maskerkey:
            realgain = calib[masker][gainindex]
            print(realgain)
    #compensated gain for distance and num of speakers
    compGain = math.pow(10,insitucompensate(numofspeakers,optimaldistance)/20)
    print('Compensated gain: {} dB'.format(20*math.log10(compGain)))
    print(maskerpath)
    print('now playing random masker {} with gain: {} as DOA {}'.format(masker, realgain*compGain, currentdoa))

    sd.play(validationmasker*realgain*compGain, validationfs, device=2)
    sd.wait()
    
def insitucompensate( numofspeakers,distance):
    compensated = round(20*math.log10(distance) - 10*math.log10(numofspeakers))
    return compensated

currentdoa = 90
maskerpath = ('/home/pi/mqtt_client/maskers/')

calibjsonpath = "calib.json"
calibdf = pd.read_json("calib.json")
print(calibdf)
f = open(calibjsonpath, "r")
calib = json.load(f)
masker = str(input('input masker name: '))
gain = int(input('input masker spl: '))
validation(masker,gain)

