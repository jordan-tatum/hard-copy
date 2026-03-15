@echo off
title Hard Copy Launcher
color 0A

echo.
echo  ==========================================
echo    H A R D   C O P Y
echo    DVD Collection Tracker
echo  ==========================================
echo.

:: -----------------------------------------------
:: STEP 1 — Start PostgreSQL
:: -----------------------------------------------
echo  [1/3] Starting PostgreSQL...

net start postgresql-x64-18 >nul 2>&1

:: Error level 0 = just started, 2 = already running — both are fine
if %errorlevel% equ 0 (
  echo        PostgreSQL started.
) else if %errorlevel% equ 2 (
  echo        PostgreSQL already running.
) else (
  echo        ERROR: Could not start PostgreSQL.
  echo        Try right-clicking this file and running as Administrator.
  pause
  exit /b 1
)
echo.

:: -----------------------------------------------
:: STEP 2 — Navigate to project folder
:: -----------------------------------------------
echo  [2/3] Locating project...

:: %~dp0 = the folder this .bat file lives in
cd /d "%~dp0"

if not exist ".venv\Scripts\activate.bat" (
  echo        ERROR: Virtual environment not found.
  echo        Run setup.bat first.
  pause
  exit /b 1
)

echo        Found at %cd%
echo.

:: -----------------------------------------------
:: STEP 3 — Start FastAPI
:: -----------------------------------------------
echo  [3/3] Starting FastAPI server...
echo.
echo  ==========================================
echo    Running at  http://localhost:8000
echo    API docs at http://localhost:8000/docs
echo.
echo    Press Ctrl+C to stop
echo  ==========================================
echo.

call .venv\Scripts\activate.bat
python run.py

echo.
echo  Server stopped.
pause
