# Updated 14/12/23
Changelog:<br>
- IMPORTANT: Updated docker so that it does not require rebuilding everytime edits are made to the content of the directory. Only restart of the docker is needed.<br>
- Updated to playback mode to use <code>aplay</code> (old version uses <code>sounddevice</code>).<br>
- Updated QoS to <code>AT_MOST_ONCE</code>.<br>
- Added new flags during printing for easier debugging.<br>
- Added backoff timer to <code>soundplayer.open_get_request()</code>.<br>
