@echo off
echo ========================================
echo Real-Time Stock Trading Simulator
echo Starting Application...
echo ========================================
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

:: Check if requirements are installed
if not exist "venv\Lib\site-packages\flask" (
    echo ERROR: Flask not found in virtual environment!
    echo Please run install.bat first to install requirements.
    echo.
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated successfully!
echo.

:: Check if app.py exists
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Please ensure you're running this from the correct directory.
    pause
    exit /b 1
)

echo Starting Real-Time Stock Trading Simulator...
echo.
echo The application will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the application
echo.

:: Start the application
python app.py

:: If we get here, the application has stopped
echo.
echo Application stopped.
pause
