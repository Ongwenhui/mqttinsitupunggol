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
 arguments:<br>

 - shadow_name
