@echo off

REM Frontend build script for Windows
echo Building Smart Cart Builder Extension...

REM Install dependencies
echo Installing dependencies...
npm install

REM Build the extension
echo Building extension...
npm run build

echo Extension built successfully!
echo To load in Chrome:
echo 1. Open Chrome and go to chrome://extensions/
echo 2. Enable 'Developer mode'
echo 3. Click 'Load unpacked' and select the 'extension' folder
pause