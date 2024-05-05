@echo off
set /p TIMEOUT="Enter timeout duration in seconds (e.g., 1200 for 20 minutes): "
cd /d "%~dp0"
timeout /t %TIMEOUT%
python ca.py
pause