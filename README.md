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
Contains dates and the maskers to be played on those dates. Also contains target SPL information that is currently not in use at the moment.

## mqttpunggolvalidation.py
Script to validate levels of maskers played. Input the name of the masker to be played in full (e.g. <code>bird_00075</code> and the target SPL from between 46 and 83. If specified masker has no gain information in the csv file (e.g. <code>White_0.2_30s</code>, input 0 as the target SPL instead.
