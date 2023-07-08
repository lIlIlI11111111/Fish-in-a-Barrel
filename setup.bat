@echo off

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
venv\Scripts\activate

REM Install required packages
pip install -r requirements.txt

REM Run the main script
python main.py

REM Deactivate the virtual environment (optional)
deactivate
