# UMA8 Pi Setup
<b>The following instructions are meant for the UMA8 PI!</b>

## ausmqtt.service setup
Service to restart the aus_mqtt docker whenever the Rpi restarts. Ensure that <code>daily.sh</code> is in the correct directory and crontab has the correct lines (see below)<br>
Put in <code>/etc/systemd/system/</code><br>
Run <code>systemctl enable ausmqtt.service</code>. This ensures that the service runs on Rpi startup.

## trycatchrmaime.sh
Put in <code>/etc/myboard/codes/rpi_iot/</code>. Remember to run <code>chmod +x trycatchrmaime.sh</code>

## daily.sh
Put in <code>/etc/systemd/system/</code>

## crontab
```
0 3 * * * /etc/systemd/system/daily.sh
*/10 * * * * /etc/systemd/system/hourly.sh 150000
```
### ----------------------------------------------- END OF SECTION -----------------------------------------------
# YNG Study Setup
<b>Read this before reading the part about Playback codes below! The YNG setup is slightly different!</b>

## Docker for YNG setup
The YNG code is running in a docker container called <code>mqttpunggol</code> for additional stability and integration with the NBS study. There are several modes of operation that must be toggled using the software switch:<br>
Mode 0: Plays silence<br>
Mode 1: Runs AMSS mode (Use for NBS study).<br>
Mode 2: Plays the 4channel test tone<br>
Mode 9: Reads the playback mode from <code>dummy.csv</code><br>

The YNG playback RPi is set to restart everyday at 3am. Set <code>device=1</code> for all instances of <code>sd.play()</code>.<br><br>

## mqttinsitupunggol3.py and mqttinsitupunggoldocker3.py
<b>UPDATED 26/10/23!</b><br>
The latest version of the playback code connects to a device shadow on IoT Core instead of subscribing to a singular topic. The desired state of the device is stored in the device shadow and retrieved by the python script. The device also broadcasts the current state of the playback code to the topic 'mqtt/statereturn'.
```
thing_name = 'WenhuiAWSThing'
shadow_name = 'mqttnbs'
```

## nbsiot.m
Under pyenv('Version', '/Library/Frameworks/Python.framework/Versions/3.10/bin/python3');, replace the filepath with the absolute filepath to the Python executable installed on your computer.
Replace the values in values with the participant ID and a boolean value to turn the playback on and off respectively.
Under pyrunfile(), replace the first argument with the filepath to sendtoiot.py. For simplicity's sake, I recommend putting the python script in the same directory so that nothing needs to be edited.<br><br>
<b>ENSURE THAT PYTHON VERSION IS 3.10 OR LOWER! MATLAB DOES NOT SUPPORT PYTHON 3.11 OR NEWER!</b>

### ----------------------------------------------- END OF SECTION -----------------------------------------------

# Playback Pi codes
<b>The following instructions are for the playback Pi!</b>

## Playback Pi Password
Hi3bdoS@

## mqttinsitupunggol
Rmb to change location_id<br>
Make sure device=7 for older versions of MCHStreamer (PCP setup) for all instances of sd.play()

## Calibrations_finals_speaker_moukey.csv
csv file with updated gain values for the new Moukey speakers.

## dtchecker.py
Script to check date and time. If dt.now() falls in between target time period, return 1 and the current datetime in str format. Else, return 0 and the current datetime in str format. Import this function and call dtchecker.main() to use.

## mqttinsitupunggol.py (DEPRECATED!!!!!!)
==Requires screen to run <code>(apt-get install screen)</code>. Run the script in a separate screen so that it continues running even when terminal is killed. Main function to play maskers from <code>dummy.csv</code> in specified order.--

## dummy.csv
There are 4 headers in this csv file:

### date
Contains an integer that references the date that the masker in the same row will be played in the yyyymmdd format.

### mode
Contains a string detailing the mode the playback will operate in. There are 4 modes in which the masker playback can operate:<br>
1. <code>amss</code> runs the Automatic Masker Selection System.<br>
2. <code>silence</code> plays <code>maskers/silence3s.wav</code>.<br>
3. <code>random</code> plays a random masker at a random SPL.<br>
4. <code><masker_name></code> plays a specific masker at the SPL specified in the same row.

### spl
Only applicable for playing a fixed masker. Contains an integer specifying the SPL the masker is to be played at.

### location_id
Not in use for now.

## mqttpunggolvalidation.py
Script to validate levels of maskers played. Input the name of the masker to be played in full (e.g. <code>bird_00075</code> and the target SPL from between 46 and 83. If specified masker has no gain information in the csv file (e.g. <code>White_0.2_30s</code>, input 0 as the target SPL instead.
