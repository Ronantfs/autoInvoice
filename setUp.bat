@echo off
REM Customise the Python version and environment name as needed
py -3.8 -m venv autoInvoice_venv

REM Check if Python is installed
where python >nul 2>nul || (
    echo Python not found. Please install Python and add it to the PATH.
    exit /b 1
)

REM Check if the virtual environment exists
if not exist autoInvoice_venv (
    REM Create virtual environment
    echo Creating Virtual Environment...
    python -m venv autoInvoice_venv
    echo Virtual environment created successfully.
)

REM Activate virtual environment
call autoInvoice_venv\Scripts\activate.bat

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo requirements.txt not found. Please make sure it's in the same directory as this batch file.
    exit /b 1
)

REM Install or upgrade pip to the latest version
echo Checking and upgrading pip...
python -m pip install --upgrade pip

REM Install required packages from requirements.txt
echo Installing required packages...
python -m pip install -r requirements.txt || (
    echo ERROR: Failed to install all requirements. Please ensure your Python installation is complete, including 'distutils'.
    echo If this problem persists, consider reinstalling Python and ensuring all components of the standard library are included.
    pause
    exit /b 1
)

echo Setup Complete. You can now run the Python script.
pause
