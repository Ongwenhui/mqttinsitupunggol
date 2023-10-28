% Ensure that the MATLAB current working directory is the same as the
% directory the python and MATLAB file is located. To get the current
% working directory, type 'pwd' in the MATLAB console. To change the
% current working directory, navigate to the correct directory using the
% navigation bar at the top of the MATLAB console.

pe = pyenv;
pe.Status
if pe.Status == "Loaded" && pe.Version ~= "3.10"
    disp('To change the Python version, restart MATLAB, then call pyenv(Version="3.10").')
else
    pyenv('Version', '/Library/Frameworks/Python.framework/Versions/3.10/bin/python3');
end
pyenv("ExecutionMode","OutOfProcess")

% location_id for locations:
% YNG: NTU_YNG_639798
% PCP: PCP_820222

location_id = "PCP_820222" % Change this as necessary
values = {9999 0 location_id}; % Participant ID and true/false to turn the script on and off
pyrunfile("sendtoiot2.py", values=values);
