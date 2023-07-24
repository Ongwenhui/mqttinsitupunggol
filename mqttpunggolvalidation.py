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
    if gain == 0:
        sd.play(validationmasker, validationfs, device=2)
        sd.wait()
    else:
        maskerkeyindex = 0
        for maskerkey in calibdf['filename']:
            if masker in maskerkey:
                print(masker)
                maskerrow = list(calibdf.iloc[maskerkeyindex])
                print(maskerrow)
                for item in maskerrow:
                    if '_' in str(item):
                        pass
                    elif round(item) == gain:
                        print(gain)
                        realgain = maskerrow[maskerrow.index(item)-1]
            
            maskerkeyindex += 1
        print(realgain)
        #compensated gain for distance and num of speakers
        compGain = math.pow(10,insitucompensate(numofspeakers,optimaldistance)/20)
        print(compGain)
        print('Compensated gain: {} dB'.format(20*math.log10(compGain)))
        print(maskerpath)

        sd.play(validationmasker*realgain*compGain, validationfs, device=2)
        sd.wait()
    
def insitucompensate( numofspeakers,distance):
    compensated = round(20*math.log10(distance) - 10*math.log10(numofspeakers))
    return compensated

currentdoa = 90
maskerpath = ('/home/pi/mqtt_client/maskers/')

calibjsonpath = "Calibrations_final_speaker.csv"
calibdf = pd.read_csv("Calibrations_final_speaker_moukey.csv")
print(calibdf)
masker = str(input('input masker name: '))
gain = int(input('input masker spl: '))
validation(masker,gain)

