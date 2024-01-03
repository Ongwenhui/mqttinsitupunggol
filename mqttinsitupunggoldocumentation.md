# Updated 14/12/23
Version 5 changelog:<br>
- IMPORTANT: Updated docker so that it does not require rebuilding everytime edits are made to the content of the directory. Only restart of the docker is needed.<br>
- Updated to playback mode to use <code>aplay</code> (old version uses <code>sounddevice</code>).<br>
- Updated QoS to <code>AT_MOST_ONCE</code>.<br>
- Added new flags during printing for easier debugging.<br>
- Added backoff timer to <code>soundplayer.open_get_request()</code>.<br>

# Initializatiom
- Interpolate(masker,gain): Obsolete function that reads the old calibration values from an old json file. Will remove in the future, but won't touch for now in case removing it causes issues in the rest of the code.<br>
- readcsv(csvfile): Reads a csvfile and returns a dictionary with all the file names and calibrated gain values.<br>
- calibgains: Filepath of the csv file containing gains of each masker calibrated to SPL levels ranging from 43dB to 87dB using the Moukey speaker recorded at a distance of 1m.<br>
- LOCATION_ID: Location of the current setup (to be updated with the different location IDs I need to check).<br>
- optimaldistance: Distance from the speakers to the target area in meters.<br>
- numofspeakers: Number of speakers at the location.

## class soundplayer(self, shadow_name, thing_name, event_loop_group, host_resolver, client_bootstrap, mqtt_connection, connected_future, shadow_client)
Class containing all variables and functions related to the playback of the maskers.<br>

## Arguments
- shadow_name: name of the device shadow in AWS IoT Core.<br>
- thing_name: name of the IoT Core thing that the device shadow belongs to.<br>
- event_loop_group: assigned the value <code>io.EventLoopGroup(1)</code>. Starts a thread for I/O operations.<br>
- host_resolver: assigned the value <code>io.DefaultHostResolver(event_loop_group)</code>. Default DNS host resolver.<br>
- client_bootstrap:  assigned the value <code>io.ClientBootStrap(event_loop_group, host_resolver)</code>. Handles creation and setup of client socket connections.<br>
- mqtt_connection: establishes a connection to the endpoint.<br>
- connected_future: returns <code>None</code> if connection is successful, returns an exception if an error is encountered.<br>
- shadow_client: connection to the device shadow in AWS IoT Core.<br>

## Init variables
- self.mqttENDPOINT: endpoint that contains the topic with AMSS predictions.<br>
- self.mqttCLIENT_ID: client id used when subscribing to the AMSS predictions topic.<br>
- self.mqttcertfolder: directory containing the certificates required to connect to IoT Core. Currently set to be relative to the cwd.<br>
- self.mqttPATH_TO_CERTIFICATE: filepath to certificate required to connect to IoT Core.<br>
- self.mqttPATH_TO_AMAZON_ROOT_CA_1: filepath to the AmazonRootCA1.pem file required to connect to IoT Core.<br>
- self.mqttPATH_TO_PRIVATE_KEY: filepath to the private key required to connect to IoT Core.<br>
- self.mqttTOPIC: topic to subscribe to that contains the AMSS predictions. Varies with location (check LOCATION_ID).<br>
- self.MQTTclient: establishes a connection to the AMSS prediction topic.<br>
- self.maskerpath: directory containing the maskers.<br>
- self.statereturntopic: topic to publish the current state of the playback to. Varies with location.<br>
- self.playbackmasker: name of the masker to be played. Data in this wav file is overwritten whenever a new masker is to be played.<br>
- self.playbacksr: sample rate the masker is to be played back at. Optional.<br>
- self.defauitplaybackdevice: default device to use for playback with <code>aplay</code>.<br>
- self.playbackcommand: command to run using <code>os.system</code> whenever a masker is to be played.<br>

# Functions
## insitucompensate(self, numofspeakers, distance)
Performs compensation of the gain based on the number of speakers and distance from the speakers to the target location. Takes in the <code>soundplayer</code> class, <code>numofspeakers</code> and <code>distance</code>, and returns the compensated gain.<br>

## insituMultiMaskercompensate(self, numbofspeakers, distance, noOfMaskers)
Performs compensation of the gain based on the number of speakers, distance from the speakers to the target location, and the number of maskers to be played at the same. **Currently not in use**. Takes in the <code>soundplayer</code> class, <code>numofspeakers</code>, <code>distance</code> and <code>noOfMaskers</code>, and retuns the compensated gain.<br>

## iotsend(inputDict)
Establishes a connection to IoT Core and pubilshes a dictionary to the topic <code>AIMEdebugging</code>. **Currently not in use, need to delete in the future**.

## spatialize(self, masker, angle, normalize, offset, k)
Not sure what this does. **Currently not in use, might delete in the future**.

## msgcallback(self, client, userdata, message)
Callback function called when message containing is received. Assigns the dictionary containing the predictions to <code>incomingmsg</code>, then prints the top rated masker, the recommended gain for the top rated masker and the BaseSPL of the surroundings.

## playsilence(self)
Plays a 3 second long silence using <code>aplay</code>. Used when running the AUS system in ambient mode.

## playtesttone(self)
Plays a 4 channel wav file with different tones using <code>aplay</code>. Used to ensure that all 4 channels are working.

## playbirdprior(self)
Plays <code>bird_prior.wav</code> using <code>aplay</code>, and publishes information about the masker being played to <code>amssTOPIC</code> in IoT Core. The value of the gain the masker is played at is assigned to <code>bird_priorgain</code>.

## playwaterprior(self)
Plays <code>water_prior.wav</code> using <code>aplay</code>, and publishes information about the masker being played to <code>amssTOPIC</code> in IoT Core. The value of the gain the masker is played at is assigned to <code>water_priorgain</code>.

## playfixedmasker(self, name, gain)
Plays the masker specified in the row corresponding to the current date at the specified gain. This function takes in the name of the masker to be played and the SPL it should be played at as input arguments. After that, it plays the specified masker using <code>aplay</code>, and publishes information about the masker being played to <code>amssTOPIC</code> in IoT Core.

## playrandommasker(self)
Plays a random masker (selected from **bird 1 to bird 80, water 1 to water 80, and wind 1 to wind 40**). The value of the gain the masker is played at is assigned to <code>randomgain</code>. This function plays a random masker at the specified gain using <code>aplay</code>, and publishes information about the masker being played to <code>amssTOPIC</code>.

## playmasker(self)
Plays the top rated masker predicted by the AMSS using <code>aplay</code>, and publishes information about the masker being played to <code>amssTOPIC</code>.

## streamcallback(self, outdata, frames, time, status)
**OLD VERSION OF PLAYBACK USING STREAM. WILL DELETE IN THE FUTURE.**

## soundlooper(self)
This function runs in multithreading mode alongside <code>mqttlooper</code>. This function performas the following steps:<br>
1. Checks if the predictions have been received from AMSS. If the predictions have been received, starts a <code>while True</code> comprising of the following steps.<br>
2. Checks for the current date and time using the <code>dtchecker</code> script. Iterates through the list of dates, checking whether the current date exists in the list. Retrieves information about the masker to be played and the SPL to play it at from the dataframe obtained from <code>dummy.csv</code>.<br>
3. If the current time is within silent hours (0070 - 2230), the playback mode defaults to playing silence.<br>
4. Else, the functions checks for the current state of <code>globalswitch<code> (see <code>globalswitch</code> section below for more info on what it is).<br>
- If <code>globalswitch == 0</code>, <code>soundplayer.playslience()</code> is called.<br>
- If <code>globalswitch == 1</code>, <code>soundplayer.playmasker()</code> is called (AMSS mode).<br>
- If <code>globalswitch == 2</code>, <code>soundplayer.playtesttone()</code> is called.<br>
- If <code>globalswitch == 7</code>, <code>soundplayer.playrandommasker()</code> is called (random mode).<br>
- If <code>globalswitch == 8</code>, <code>soundplayer.playbirdprior()</code> is called.<br>
- If <code>globalswitch == 9</code>, the function checks the dateframe obtained from <code>dummy.csv</code> for the specific mode to play (csv mode).<br>


