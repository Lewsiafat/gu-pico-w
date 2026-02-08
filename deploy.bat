@echo off
echo Deploying code to Pico...
cd /d "%~dp0src"
python -m mpremote cp -r . :
echo.
echo Deployment complete!
pause
