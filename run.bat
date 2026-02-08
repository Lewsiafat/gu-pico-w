@echo off
echo Running main.py on Pico...
cd /d "%~dp0src"
python -m mpremote run gu_main.py
