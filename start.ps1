& "c:/Projects/Automotive Simulation/env/Scripts/Activate.ps1"
Start-Process .\env\Scripts\streamlit.exe 'run .\app.py'
Start-Process .\env\Scripts\python.exe .\forwarder.py
Start-Process .\env\Scripts\python.exe .\server.py
