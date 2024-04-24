@echo off
echo Running Alternative Main Python Script

REM Activate the virtual environment
call autoInvoice_venv\Scripts\activate.bat

REM Run the alternative Python script
python alt_main.py --mode all

pause

REM Deactivate the virtual environment
call autoInvoice_venv\Scripts\deactivate.bat
