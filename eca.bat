@echo off
set /p TIMEOUT="Enter timeout duration in seconds (e.g., 1200 for 20 minutes): "
cd /d "C:\Users\BC\Documents\cabal_macros"
timeout /t %TIMEOUT%
python eca.py
pause