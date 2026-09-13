@echo off
if "%1"=="min" goto RUN

:: Re-launch self minimized
start /min cmd /c "%~f0" min
exit

:RUN
cd /d "%~dp0..\.."
".venv\Scripts\python.exe" "cyber_lab\app.py"