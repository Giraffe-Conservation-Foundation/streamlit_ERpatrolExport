@echo off
REM Windows Quick Start Script for Patrol Shapefile Downloader

echo ========================================
echo Patrol Shapefile Downloader Setup
echo ========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install requirements
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Test setup
echo Testing setup...
python test_setup.py
echo.

REM Ask to run app
echo ========================================
echo Setup complete!
echo ========================================
echo.
set /p run_app="Do you want to run the app now? (Y/N): "
if /i "%run_app%"=="Y" (
    echo.
    echo Starting Streamlit app...
    echo Press Ctrl+C to stop the server
    echo.
    streamlit run app.py
) else (
    echo.
    echo To run the app later, use:
    echo   venv\Scripts\activate
    echo   streamlit run app.py
    echo.
)

pause
