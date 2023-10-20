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
# YNG Study Setup
Read this before reading the part about Playback codes below! The YNG setup is slightly different!

## Docker for YNG setup
The YNG is running in a docker container called <code>mqttpunggol</code> for additional stability and integration with the NBS study. There are several modes of operation that must be toggled using the software switch:<br>
Mode 0: Plays silence<br>
Mode 1: Playback is running in AMSS mode<br>
Mode 2: Plays the 4channel test tone<br>
Mode 9: Reads the playback mode from <code>dummy.csv</code><br>

The YNG playback RPi is set to restart everyday at 3am. Set <code>device=1</code> for all instances of <code>sd.play()</code>.

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

## mqttinsitupunggol.py
Requires screen to run <code>(apt-get install screen)</code>. Run the script in a separate screen so that it continues running even when terminal is killed. Main function to play maskers from <code>dummy.csv</code> in specified order.

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
