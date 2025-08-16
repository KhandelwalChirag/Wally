@echo off

REM Create a virtual environment using uv
uv venv

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Install the packages using uv
uv pip install -r requirements.txt

echo "Setup complete. You can now run the application with 'run.bat'"