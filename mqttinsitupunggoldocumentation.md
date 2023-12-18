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

