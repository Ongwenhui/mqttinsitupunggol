import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
#from PIL import Image
from io import BytesIO
import numpy as np
import sounddevice as sd 
import soundfile as sf
import time 
import queue
import sys
import threading
import math
import csv
import pandas as pd
import random
from pydub import AudioSegment
import sys
import tty
import termios
import dtchecker
import random
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder, iotshadow
import os

varymaskers = False
MEOW = False

cwd = os.getcwd()
calibjsonpath = f"{cwd}/calib.json"

def interpolate(masker,gain):
    f = open(calibjsonpath, "r")
    # calib = f.read()
    # print(calib)
    calib = json.load(f)
    # # calib = json.loads(f.read())
    keepgoing = True
    counter = 0
    chosengain = 0
    while keepgoing == True:
        currval = abs(gain - calib[masker][counter])
        if counter < (len(calib[masker])-1):
            nextval = abs(gain - calib[masker][counter + 1])
        else: 
            nextval = abs(gain - calib[masker][0])
        if nextval >= currval:
            keepgoing = False
            chosengain = calib[masker][counter]
        if counter < (len(calib[masker])-1):
            counter += 1
        else:
            counter = 0
    if counter>0: 
        finaldb = counter -1 + 46
    else:
        finaldb = 46+37

    # print("chosengain = {}".format(chosengain))
    # print("counter -1 = {}".format(counter -1))
    return finaldb

def readcsv(csvfile):
    calibgains = {}
    with open(csvfile, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            entrycount = 0
            currmasker = ""
            nextgain = 0
            for entry in row:
                if entrycount == 0:
                    calibgains[entry] = {}
                    currmasker = entry
                elif entrycount != 0 and (entrycount % 2) != 0:
                    nextgain = float(entry)
                elif entrycount != 0 and (entrycount % 2) == 0:
                    calibgains[currmasker][str(int(round(float(entry))))] = nextgain 
                entrycount += 1
    return calibgains

calibgains = readcsv(f"{cwd}/Calibrations_final_speaker_moukey.csv")

LOCATION_ID = 'demo'
optimaldistance = 1
numofspeakers = 4
class soundplayer:
    def __init__(self,
        shadow_name      = None,
        thing_name       = None,
        event_loop_group = None,
        host_resolver    = None,
        client_bootstrap = None,
        mqtt_connection  = None,
        connected_future = None,
        shadow_client    = None,
                 ):
        self.mqttENDPOINT="a5i03kombapo4-ats.iot.ap-southeast-1.amazonaws.com"
        self.mqttCLIENT_ID= "AIMEGET"
        self.mqttcertfolder=f"{cwd}/certs/"
        self.mqttPATH_TO_CERTIFICATE = self.mqttcertfolder + "c86008d5f6f3eb115159777ba9da6c0b97bfdf2309c15020c8d1d2747e4f6bdc-certificate.pem.crt"
        self.mqttPATH_TO_AMAZON_ROOT_CA_1 = self.mqttcertfolder + "AmazonRootCA1.pem"
        self.mqttPATH_TO_PRIVATE_KEY=self.mqttcertfolder + "c86008d5f6f3eb115159777ba9da6c0b97bfdf2309c15020c8d1d2747e4f6bdc-private.pem.key"
        self.mqttTOPIC="amss/{}/prediction".format(LOCATION_ID)
        self.mqttRANGE=20
        self.currentdoa = 90
        self.MQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(self.mqttCLIENT_ID)
        self.MQTTClient.configureEndpoint(self.mqttENDPOINT, 8883)
        self.MQTTClient.configureCredentials(self.mqttPATH_TO_AMAZON_ROOT_CA_1, self.mqttPATH_TO_PRIVATE_KEY, self.mqttPATH_TO_CERTIFICATE)
        # self.msgdict = {'predictions': [{'rank': 1, 'id': 'bird_00075', 'gain': 0.01793866604566574, 'score': 0.47396957874298096}, {'rank': 2, 'id': 'bird_00075', 'gain': 0.020203232765197754, 'score': 0.47391098737716675}, {'rank': 3, 'id': 'bird_00075', 'gain': 0.02149977907538414, 'score': 0.47387757897377014}, {'rank': 4, 'id': 'bird_00069', 'gain': 0.05129025876522064, 'score': 0.4719516634941101}, {'rank': 5, 'id': 'bird_00075', 'gain': 0.10646381229162216, 'score': 0.47165820002555847}, {'rank': 6, 'id': 'bird_00069', 'gain': 0.10134433209896088, 'score': 0.4705403745174408}, {'rank': 7, 'id': 'bird_00025', 'gain': 0.0057005020789802074, 'score': 0.470207154750824}, {'rank': 8, 'id': 'bird_00069', 'gain': 0.15140660107135773, 'score': 0.46911484003067017}, {'rank': 9, 'id': 'bird_00025', 'gain': 0.08437956869602203, 'score': 0.46776485443115234}, {'rank': 10, 'id': 'bird_00071', 'gain': 0.06381088495254517, 'score': 0.4665457308292389}, {'rank': 11, 'id': 'bird_00069', 'gain': 0.25197258591651917, 'score': 0.46620792150497437}, {'rank': 12, 'id': 'bird_00046', 'gain': 0.07355550676584244, 'score': 0.46558114886283875}], 'base_score': 0.33999258279800415, 
        # 'doa': self.currentdoa, 'from': 'ntu-gazebo01', 'timestamp': 1654067860.26, 'base_spl': 68.10846120156562} if not MEOW else {'predictions': [{'rank': 1, 'id': 'meow', 'gain': 1, 'score': 0.47396957874298096}, {'rank': 2, 'id': 'meow', 'gain': 1, 'score': 0.47391098737716675}, {'rank': 3, 'id': 'meow', 'gain': 1, 'score': 0.47387757897377014}, {'rank': 4, 'id': 'meow', 'gain': 1, 'score': 0.4719516634941101}, {'rank': 5, 'id': 'meow', 'gain': 1, 'score': 0.47165820002555847}], 'base_score': 0.33999258279800415, 
        # 'doa': self.currentdoa, 'from': 'ntu-gazebo01', 'timestamp': 1654067860.26, 'base_spl': 68.10846120156562}
        self.fixedmasker = 'playing fixed masker = '
        self.msgdict = None
        self.currentmasker = "bird_00075" if not MEOW else "meow"
        self.maskerpath = f"{cwd}/maskers/"
        self.maskergain = 1.2
        self.gainweight = 1    
        self.maskerdiff = 0.0001
        self.gainlimit = 1000
        self.weightedgain = 0
        self.buffersize = 20
        self.blocksize = 4096
        self.q = queue.Queue()#(maxsize=self.buffersize)
        self.q2 = queue.Queue()
        self.msgq = None
        self.msgqeval = None
        self.event = threading.Event()
        self.fadelength = 80
        self.maskercounter = 0
        self.currentmaskerorig = "bird_00075" if not MEOW else "meow"
        self.maskergainorig = 1
        self.doadiff = 20
        self.ambientspl = 68.1
        self.nexttrackmsg = 'playback starting...'
        self.beforeevaluationmsg = 'evaluation starting...'
        self.duringevaluationmsg = 'evaluation in progress, press any key to proceed to the next track.'
        self.endmsg = 'end of study'
        self.voicePromptGain = 0.1
        
        self.statereturntopic = 'mqtt/statereturn'
        self.shadow_name = shadow_name
        self.thing_name = thing_name
        #self.ENDPOINT = ENDPOINT
        #self.PATH_TO_CERTIFICATE = PATH_TO_CERTIFICATE
        #self.PATH_TO_PRIVATE_KEY = PATH_TO_PRIVATE_KEY
        #self.client_bootstrap = client_bootstrap
        #self.PATH_TO_AMAZON_ROOT_CA_1 = PATH_TO_AMAZON_ROOT_CA_1
        #self.CLIENT_ID = CLIENT_ID
        #self.clean_session = False
        #self.keep_alive_secs = 6
        
        self.event_loop_group = event_loop_group
        self.host_resolver = host_resolver
        self.client_bootstrap = client_bootstrap
        self.mqtt_connection = mqtt_connection
        self.connected_future = connected_future
        self.shadow_client = shadow_client

    def insitucompensate(self, numofspeakers,distance):
        compensated = round(20*math.log10(distance) - 10*math.log10(numofspeakers))
        return compensated

    def insituMultiMaskercompensate(self, numofspeakers,distance,noOfMaskers):
        compensated = round(20*math.log10(distance) - 
                            10*math.log10(numofspeakers) -
                            20*math.log10(noOfMaskers))
        return compensated
    def iotsend(inputdict):
        mqtt_connection.connect()
        mqtt_connection.publish(topic="test/AIMEdebugging", payload=(inputdict), qos=mqtt.QoS.AT_MOST_ONCE)
    def spatialize(self, masker, angle, normalize=True, offset=-65, k=1.0):
        # masker.shape = (n_samples,)2
        # angle in degrees
        # offset in degrees
        
        # speaker locations assumed to be (RF, RB, LB, LF) i.e., (45, 135, 225, 315) deg
        # counting CW relative to the 0 deg line of the UMA
        # use offset to shift the speaker locations as needed
        
        '''
                0 deg
        [LF]----------[RF]
        |       ^       |
        |       |       |
        |     [UMA]     |
        |               |
        |               |
        [LB]----------[RB]
        
        
        e.g. if UMA is actually pointing at RF, then offset should be 45 deg
        i.e. set offset to negative of whereever UMA is pointing as if the UMA is pointing at 0 deg
        '''
            
        masker = np.squeeze(masker)
        
        anglerad = -np.deg2rad(angle + offset)
        x = k * np.cos(anglerad)
        y = k * np.sin(anglerad)
        
        lf = 1 + x + y # 1 + 1/2)
        lb = 1 - x + y
        rb = 1 - x - y
        rf = 1 + x - y

        # lf = 0
        # lb = 0
        # rb = 0
        # rf = 0

        
        gains = np.array([rb, lb, lf, rf])
        
        if normalize:
            gains = gains / np.sqrt(1 + 2*k*k)
    
        masker4c = masker[:, None] * gains[None, :] # (n_samples, 4)
        
        return masker4c        

    def msgcallback(self, client, userdata, message):
        print("GETTING PREDICTIONS FROM AWS")
        incomingmsg=json.loads(message.payload.decode('utf-8'))
        # self.q.put_nowait(incomingmsg)
        # self.q2.put_nowait(incomingmsg)
        self.msgq = incomingmsg
        print("Recommended Masker is: " + str(incomingmsg['predictions'][0]["id"]))
        print("Recommended Gain is: {} ({}dB)".format(incomingmsg['predictions'][0]["gain"], interpolate(incomingmsg['predictions'][0]["id"],incomingmsg['predictions'][0]["gain"])))
        print("BaseSPL is: {}".format(incomingmsg["base_spl"]))
        # data, fs = sf.read(msgdict['predictions'][0]["id"]+'.wav', dtype='float32')  
        # sd.play(data, fs, device=1)
    def ambient(self):
        time.sleep(30)
    def playsilence(self):
        print('playing silence')
        silence, silencefs = sf.read(self.maskerpath + "silence3s.wav", dtype='float32')
        sd.play(silence, silencefs, device=1)
        sd.wait()
    def playtesttone(self):
        testtone, testtonefs = sf.read(f"{cwd}/4channel.wav")
        sd.play(testtone, testtonefs, device=1)
        sd.wait()

    def playbirdprior(self):
        bird_prior, fs = sf.read(self.maskerpath + 'bird_prior.wav')
        bird_priorgain = 0.056027

        location = f'{LOCATION_ID}'
        sendmasker = 'bird_prior'
        predictionsdict = {"Prediction": sendmasker, "basescore": 0, "doa": 0, "basespl": bird_priorgain, "from": location}
        print(predictionsdict)
        predictionsdict = str(predictionsdict).replace("'", '"')
        #compensated gain for distance and num of speakers
        compGain = math.pow(10,self.insitucompensate(numofspeakers,optimaldistance)/20)
        print('Compensated gain: {} dB'.format(20*math.log10(compGain)))
        print(self.maskerpath + 'bird_prior')
        print('now playing fixed masker {} with gain: {} as DOA {}'.format('bird_prior', bird_priorgain*compGain, self.currentdoa))

        sd.play(bird_prior*bird_priorgain*compGain, fs, device=1)
        sd.wait()
        try:
            amssClient.publish(topic=amssTOPIC, payload = (str(predictionsdict)), QoS=mqtt.QoS.AT_MOST_ONCE)
        except:
            pass

    def playwaterprior(self):
        water_prior, fs = sf.read(self.maskerpath + 'water_prior.wav')
        water_priorgain = 0.036370

        location = f'{LOCATION_ID}'
        sendmasker = 'water_prior'
        predictionsdict = {"Prediction": sendmasker, "basescore": 0, "doa": 0, "basespl": gain, "from": location}
        print(predictionsdict)
        predictionsdict = str(predictionsdict).replace("'", '"')
        #compensated gain for distance and num of speakers
        compGain = math.pow(10,self.insitucompensate(numofspeakers,optimaldistance)/20)
        print('Compensated gain: {} dB'.format(20*math.log10(compGain)))
        print(self.maskerpath + name)
        print('now playing fixed masker {} with gain: {} as DOA {}'.format('water_prior', water_priorgain*compGain, self.currentdoa))

        sd.play(water_prior*water_priorgain*compGain, fs, device=1)
        sd.wait()
        try:
            amssClient.publish(topic=amssTOPIC, payload = (str(predictionsdict)), QoS=mqtt.QoS.AT_MOST_ONCE)
        except:
            pass
        
    def playfixedmasker(self, name, gain):
        fixedmaskers, fs = sf.read(self.maskerpath + name + '.wav')
        f = open(calibjsonpath, "r")
        calib = json.load(f)
        gainindex = gain - 46
        for maskerkey in calib:
            if name == maskerkey:
                realgain = calib[name][gainindex]
                print(realgain)
                
        location = f'{LOCATION_ID}'
        sendmasker = f'{name}'
        predictionsdict = {"Prediction": sendmasker, "basescore": 0, "doa": 0, "basespl": gain, "from": location}
        print(predictionsdict)
        predictionsdict = str(predictionsdict).replace("'", '"')
        #compensated gain for distance and num of speakers
        compGain = math.pow(10,self.insitucompensate(numofspeakers,optimaldistance)/20)
        print('Compensated gain: {} dB'.format(20*math.log10(compGain)))
        print(self.maskerpath + name)
        print('now playing fixed masker {} with gain: {} as DOA {}'.format(name, realgain*compGain, self.currentdoa))

        sd.play(fixedmaskers*realgain*compGain, fs, device=1)
        sd.wait()
        try:
            amssClient.publish(topic=amssTOPIC, payload = (str(predictionsdict)), QoS=mqtt.QoS.AT_MOST_ONCE)
        except:
            pass
        
    def playrandommasker(self):
        randomlist = ['bird', 'water', 'wind']
        randomchoice = random.choice(randomlist)
        if randomchoice == 'wind':
            randomnumber = random.randrange(1, 41)
            if randomnumber < 10:
                randomnumber = '0' + str(randomnumber)
        else:
            randomnumber = random.randrange(1, 81)
            if randomnumber < 10:
                randomnumber = '0' + str(randomnumber)
        print(f'random masker = {randomchoice}, randomnumber = {randomnumber}')
        randomgain = random.randrange(46, 84)
        randommasker = (f'{randomchoice}_000{randomnumber}')
        fixedmaskers, fs = sf.read(self.maskerpath + randommasker + '.wav')
        f = open(calibjsonpath, "r")
        calib = json.load(f)
        randomgain = 64
        gainindex = randomgain - 46
        for maskerkey in calib:
            if randommasker == maskerkey:
                realgain = calib[randommasker][gainindex]
                print(realgain)

        #compensated gain for distance and num of speakers
        compGain = math.pow(10,self.insitucompensate(numofspeakers,optimaldistance)/20)
        location = f'{LOCATION_ID}'
        sendmasker = f'{randommasker}'
        predictionsdict = {"Prediction": sendmasker, "basescore": 0, "doa": 0, "basespl": randomgain, "from": location}
        print(predictionsdict)
        predictionsdict = str(predictionsdict).replace("'", '"')
        try:
            amssClient.publish(topic=amssTOPIC, payload = (str(predictionsdict)), QoS=mqtt.QoS.AT_MOST_ONCE)
        except:
            pass
        
        print('Compensated gain: {} dB'.format(20*math.log10(compGain)))
        print(self.maskerpath + randommasker)
        print('now playing random masker {} with gain: {} as DOA {}'.format(randommasker, realgain*compGain, self.currentdoa))

        sd.play(fixedmaskers*realgain*compGain, fs, device=1)
        sd.wait()
    def playmasker(self):
        self.q = queue.Queue()
        newmasker = None
        newweightedgain = None
        newdoa = None
        self.msgdict = self.msgq
        self.msgqeval = self.msgdict
        #why q2?    
        if not self.q2.empty():
            self.msgdict = self.msgq
            self.ambientspl = self.msgdict["base_spl"]

        if self.msgdict != None: #If there is a prediction
            predictionlist =[]
            uniquepredictionlist = []
            for prediction in self.msgdict['predictions']:
                for indexes in range(len(self.msgdict['predictions'])):
                    predictionlist.append(self.msgdict['predictions'][indexes]['rank'])
                    predictionlist.append(self.msgdict['predictions'][indexes]['id'])
                for item in predictionlist:
                    if type(item) == str:
                        if item not in uniquepredictionlist:
                            uniquepredictionlist.append(item)
                            uniquepredictionlist.append(predictionlist.index(item)-1)
            self.currentmasker1 = uniquepredictionlist[0]
            self.maskerindex1 = uniquepredictionlist[1]
            print('top rated masker = {}'.format(self.currentmasker1))
            print('index of top masker = {}'.format(self.maskerindex1))
            # if the masker to be played is not self.currentmasker, set self.maskergain to the gain of the masker to be played
            # self.currentmasker is set to bird_00075 by default
            if (self.msgdict['predictions'][self.maskerindex1]["id"] != self.currentmasker) or (abs(self.msgdict['predictions'][self.maskercounter]["gain"]-self.maskergain)*self.gainweight>self.maskerdiff) or (abs(self.currentdoa - self.msgdict["doa"])>self.doadiff):
                self.maskergain1 = self.msgdict['predictions'][self.maskerindex1]["gain"]
                # if self.maskergain (set in previous step) less than gainlimit (set at 1000)
                if self.maskergain1*self.gainweight < self.gainlimit:
                    print("self.maskergain1 = {}".format(self.maskergain1))
                    # calculate amssgain
                    amssgain = interpolate(self.msgdict['predictions'][self.maskerindex1]["id"],self.maskergain1) + self.insitucompensate(numofspeakers,optimaldistance)
                    # set amssgaint to min 45 and max 83
                    if amssgain >45 and amssgain <= 83:
                        pass
                    elif amssgain >83:
                        amssgain = 83
                    elif amssgain <46:
                        amssgain = 46
                    amssgain1 = amssgain
                    self.weightedgain1 = calibgains[self.msgdict['predictions'][self.maskerindex1]["id"]+'.wav'][str(amssgain1)]
                    print("self.weightedgain1 = {}".format(self.weightedgain1))
                else:
                    self.weightedgain1 = self.gainlimit
                self.currentdoa = self.msgdict["doa"]
        else:
            pass
        try:
            f1, fs1 = sf.read(self.maskerpath + self.currentmasker1 +'.wav')
            print("stream created using {} with gain: {} at DOA: {}".format(self.currentmasker1,
                                                                                   self.weightedgain1,
                                                                                   self.currentdoa))
            location = f'{LOCATION_ID}'
            sendmasker = f'{self.currentmasker1}'
            predictionsdict = {"Prediction": sendmasker, "basescore": self.msgdict['base_score'], "doa": self.msgdict['doa'], "basespl": self.msgdict['base_spl'], "from": location}
            print(predictionsdict)
            predictionsdict = str(predictionsdict).replace("'", '"')

            data1 = f1*self.weightedgain1
            compGain = math.pow(10,self.insitucompensate(numofspeakers,optimaldistance)/20)
            print('Compensated gain: {} dB'.format(20*math.log10(compGain)))
            try:
                amssClient.publish(topic=amssTOPIC, payload = (str(predictionsdict)), QoS=mqtt.QoS.AT_MOST_ONCE)
            except:
                pass
            sd.play(data1*compGain, fs1, device=1)
            sd.wait()
        except KeyboardInterrupt:
            pass

    def streamcallback(self, outdata, frames, time, status):
        data = np.zeros((self.blocksize,1))
        assert frames == self.blocksize
        # if status.output_underflow:
        #     print('Output underflow: increase blocksize?', file=sys.stderr)
        #     raise sd.CallbackAbort
        assert not status
        # try:
        data = self.q.get_nowait()
        # except queue.Empty as e:
        #     raise sd.CallbackAbort from e
        if len(data) < len(outdata) and not self.q.empty():
            outdata[:len(data)] = data
            outdata[len(data):].fill(0)
            print("track ending")
            raise sd.CallbackStop
        else:
            outdata[:] = data
       
    # save terminal settings

    def soundlooper(self):
        #wait for predictions to load first
        notprinted_flag = True
        while self.msgq == None:
            if notprinted_flag:
                print("Waiting for predictions")
                notprinted_flag = False

        while True:
            dateindex = 0
            print(dateindex)
            switch, date = dtchecker.main()
            for date2 in datelist:
                date2 = str(date2)    
                if date == date2:
                    masker = dummycsv['mode'][dateindex]
                    gain = dummycsv['spl'][dateindex]
                    print(f'masker = {masker}, gain = {gain}')
                    print(f'switch = {switch}')
                    print(f'globalswitch = {globalswitch}')
                    if switch == 0:
                        print('Quiet hours')
                        self.playsilence()
                    if switch == 1:
                        if globalswitch == 0:
                            self.playsilence()
                        if globalswitch == 1:
                            self.playmasker()
                        if globalswitch == 2:
                            self.playtesttone()
                        if globalswitch == 7:
                            self.playrandommasker()
                        if globalswitch == 8:
                            self.playbirdprior()
                        if globalswitch == 9:
                            if masker == 'amss':
                                self.playmasker()
                            elif masker == 'random':
                                self.playrandommasker()
                            elif masker == 'silence':
                                self.playsilence()
                            else:
                                self.playfixedmasker(masker, gain)
                    elif switch == 0:
                        self.ambient()
                dateindex += 1

    def mqttlooper(self):               
        while True:
            try:             
                self.MQTTClient.subscribeAsync(self.mqttTOPIC, 0,messageCallback = self.msgcallback)
            except:
                pass
            time.sleep(0.5)
            try:
                self.open_get_request()
            except Exception as e:
                print(f'open_get_request exception: {e.message}')
                pass
            time.sleep(0.5)
            try:
                self.get_accepted_responses()
            except Exception as e:
                print(f'get_accepted_responses exception: {e.message}')
                pass
            time.sleep(0.5)
            try:
                self.send_back_to_iot(globalswitch, LOCATION_ID)
            except Exception as e:
                print(f'send_back_to_iot exception: {e.message}')
                pass
            time.sleep(0.5)

    # Publish blank payload to mqttnbs shadow to request for the current state of the shadow
    # don't seem to be working? Not sure what's wrong
    # usual exception: 0: 5131 (AWS_ERROR_MQTT_NOT_CONNECTED): The requested operation is invalid as the connection is not open
    def open_get_request(self):
        print("-------------------open_get_request starts here-----------------------")
        self.open_get_request_future = self.shadow_client.publish_get_named_shadow(
            request=iotshadow.GetNamedShadowRequest(
                shadow_name = self.shadow_name,
                thing_name = self.thing_name
            ),
            qos=mqtt.QoS.AT_MOST_ONCE
        )
        
        # Implement backoff in the case of closed connection
        sleep_time = 2
        num_retries = 4
        for x in range(0, num_retries):
            try:
                self.open_get_request_future.result()
                str_error = None
            except Exception as e:
                str_error = str(f'{x}: {e}')
                print(str_error)
            if str_error:
                time.sleep(sleep_time)
                sleep_time += 1
            else:
                break

    # Subscribes to the /get/accepted topic after the get request is opened in open_get_request. Callback = on_get_shadow_accepted
    def get_accepted_responses(self):
        print("-------------------get_accept_responses starts here-----------------------")
        self.get_accepted_subscribed_future, self.get_shadow_accepted_topic = self.shadow_client.subscribe_to_get_named_shadow_accepted(
            request=iotshadow.GetNamedShadowSubscriptionRequest(shadow_name = self.shadow_name, thing_name = self.thing_name),
            qos=mqtt.QoS.AT_MOST_ONCE,
            callback=self.on_get_shadow_accepted)
 
        sleep_time = 2
        num_retries = 4
        for x in range(0, num_retries):
            try:
                self.get_accepted_subscribed_future.result()
                str_error = None
            except Exception as e:
                str_error = str(f'{x}: {e}')
                print(str_error)
            if str_error:
                time.sleep(sleep_time)
                sleep_time += 1
            else:
                print("-------------------get_accept_responses ends here-----------------------")
                break

    # Callback retrieves the new state from the response and assigns that value to globalswitch
    def on_get_shadow_accepted(self, response):
        print("-------------------on_get_shadow_accepted starts here-----------------------")
        if response:
            print(response)
            global globalswitch
            if response.state.desired['location_id'] == LOCATION_ID:
                globalswitch = response.state.desired['onoff']
            else:
                pass
            print(f"globalswitch = {globalswitch}")
            return globalswitch
        else:
            print('eeeeee')

    # Publishes the current state of the device back to the IoT Core topic 'mqtt/statereturn'
    def send_back_to_iot(self, globalswitch, LOCATION_ID):
        print('-------------------send_back_to_iot starts here-----------------------')
        self.returnmessage = f'globalswitch at {LOCATION_ID} is now {globalswitch}'
        self.returnmessagedict = {"message" : self.returnmessage, "state" : globalswitch}
        print(f'return message = {self.returnmessagedict}')
        self.mqtt_connection.publish(
            topic=self.statereturntopic,
            payload=json.dumps(self.returnmessagedict),
            qos=mqtt.QoS.AT_MOST_ONCE,
            retain=True)
        print('-------------------send_back_to_iot ends here-----------------------')
        
        
        

# Configuration for connection to IoT Core for software switch
ENDPOINT = "a5i03kombapo4-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "enviropluspi"
PATH_TO_CERTIFICATE = f"{cwd}/certs/9972587da4767d10db7001fc18bab5b9124945c4762ebf246b6266e08352970b-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = f"{cwd}/certs/9972587da4767d10db7001fc18bab5b9124945c4762ebf246b6266e08352970b-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = f"{cwd}/certs/AmazonRootCA1.pem"

thing_name = "WenhuiAWSthing"
shadow_name = "mqttnbs"


event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
connected_future = mqtt_connection.connect()
shadow_client = iotshadow.IotShadowClient(mqtt_connection)
connected_future.result()
# Make the connect() call
print("Connected to device shadow")

sp = soundplayer(
    shadow_name = shadow_name,
    thing_name = thing_name,
    event_loop_group = event_loop_group,
    host_resolver = host_resolver,
    client_bootstrap = client_bootstrap,
    mqtt_connection = mqtt_connection,
    connected_future = connected_future,
    shadow_client = shadow_client,
)

sp.MQTTClient.connectAsync()
print("connected to mqtt")

# Set to 9 by default for Punggol study, comment out if is YNG study
globalswitch = 1

dummycsv = pd.read_csv(f"{cwd}/dummy.csv")
print(dummycsv)
datelist = list(dummycsv['date'])
print(datelist)

# Configuration for connection to IoT Core to log predictions from AMSS mode
CLIENT_IDlogging = 'AMSSlogging'
amssTOPIC = 'amss/logging'
amssClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_IDlogging)
amssClient.configureEndpoint(ENDPOINT, 8883)
amssClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_IDlogging,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_IDlogging))
amssClient.connectAsync()
print('Connected to amss/logging')

mqtt_thread = threading.Thread(
        target=sp.mqttlooper,
        name="mqtt",
        args=(),
        daemon=True,
    )

soundlooper_thread = threading.Thread(
        target=sp.soundlooper,
        name="soundlooper",
        args=(),
        daemon=True,
    )

mqtt_thread.start()
soundlooper_thread.start()
soundlooper_thread.join()
mqtt_thread.join()

# sp.MQTTClient.subscribeAsync(sp.mqttTOPIC, 0,messageCallback = sp.msgcallback)
# sp.playmasker()
