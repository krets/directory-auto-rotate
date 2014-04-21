@echo off
rem http://danrice.net/articles/run-a-batch-script-minimized
if not "%minimized%"=="" goto :minimized
set minimized=true
start /min cmd /C "%~dpnx0"
goto :EOF
:minimized
rem Anything after here will run in a minimized window
cd /d %~dp0
rem Run auto rotate on the current user download directory (windows 7 default)
rem Also the -e flag will delete files older than a year.
..\autorotatedir\autorotatedir.py -e 365 %USERPROFILE%\Downloads
