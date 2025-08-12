@echo off

REM Backend startup script for Windows
echo Starting Smart Cart Builder Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your API keys before running the server
    pause
    exit /b 1
)

REM Create user_data directory if it doesn't exist
if not exist "user_data" mkdir user_data

REM Start the server
echo Starting FastAPI server...
python main.py