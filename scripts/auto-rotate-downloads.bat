@echo off
cd /d %~dp0
rem Run auto rotate on the current user download directory (windows 7 default)
rem Also the -e flag will delete files older than a year.
..\autorotatedir\autorotatedir.py -e 365 %USERPROFILE%\Downloads
