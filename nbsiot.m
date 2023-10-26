pe = pyenv;
pe.Status
if pe.Status == "Loaded" && pe.Version ~= "3.10"
    disp('To change the Python version, restart MATLAB, then call pyenv(Version="3.10").')
else
    pyenv('Version', '/Library/Frameworks/Python.framework/Versions/3.10/bin/python3');
end
pyenv("ExecutionMode","OutOfProcess")
values = [9999 0]; % Participant ID and true/false to turn the script on and off
pyrunfile("sendtoiot2.py", values=values);
