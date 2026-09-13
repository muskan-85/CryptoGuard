@echo off
set LAUNCHER=%~dp0run_app.bat

:: Register cryptoguard protocol to point directly to run_app.bat
reg add "HKCU\Software\Classes\cryptoguard" /ve /d "URL:CryptoGuard Protocol" /f
reg add "HKCU\Software\Classes\cryptoguard" /v "URL Protocol" /d "" /f
reg add "HKCU\Software\Classes\cryptoguard\shell\open\command" /ve /d "\"%LAUNCHER%\"" /f

echo Protocol updated successfully!
pause