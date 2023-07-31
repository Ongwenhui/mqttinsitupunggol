# mqttinsitupunggol

Rmb to change location_id<br>
Make sure device=7 for older versions of MCHStreamer (PCP setup) for all instances of sd.play()

## Calibrations_finals_speaker_moukey.csv
csv file with updated gain values for the new Moukey speakers.

## Dockerfile
Deprecated

## dtchecker.py
Script to check date and time. If dt.now() falls in between target time period, return 1 and the current datetime in str format. Else, return 0 and the current datetime in str format. Import this function and call dtchecker.main() to use.

## mqttinsitupunggol.py
Requires screen to run <code>(apt-get install screen)</code>. Run the script in a separate screen so that it continues running even when terminal is killed. Main function to play maskers from <code>dummy.csv</code> in specified order.

## dummy.csv
Contains dates and the maskers to be played on those dates. Also contains target SPL information that is currently not in use at the moment.

## mqttinsitupunggoldocker.py
Deprecated

## mqttpunggolvalidation.py
Script to validate levels of maskers played. Input the name of the masker to be played in full (e.g. <code>bird_00075</code> and the target SPL from between 46 and 83. If specified masker has no gain information in the csv file (e.g. <code>White_0.2_30s</code>, input 0 as the target SPL instead.
