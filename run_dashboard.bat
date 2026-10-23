@echo off
cd /d "%~dp0"
echo Installing dashboard dependencies if needed...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed. Check that Python is installed and available in PATH.
  pause
  exit /b 1
)
python -m streamlit run app.py
pause
