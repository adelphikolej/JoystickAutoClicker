@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo   Joystick AutoClicker - EXE Builder
echo ============================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python was not found.
    echo Install Python 3.10+ from https://www.python.org/downloads/
    echo During installation, tick "Add Python to PATH".
    pause
    exit /b 1
  )
  set "PY=python"
)

echo [1/3] Installing Python packages...
%PY% -m pip install --upgrade pip
if errorlevel 1 goto fail
%PY% -m pip install -r requirements.txt
if errorlevel 1 goto fail
%PY% -m pip install pyinstaller
if errorlevel 1 goto fail

echo.
echo [2/3] Building the EXE...
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name JoystickAutoClicker main.py
if errorlevel 1 goto fail

echo.
echo [3/3] Build complete!
echo Your EXE should be here:
echo %CD%\dist\JoystickAutoClicker.exe
echo.
echo Note: the virtual gamepad driver is installed separately and is NOT bundled.
pause
exit /b 0

:fail
echo.
echo Build failed. Read the error above, check your Python installation and internet connection, then try again.
pause
exit /b 1
