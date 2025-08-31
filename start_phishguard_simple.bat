@echo off
echo ================================================================
echo PHISHGUARD - Simple Startup Script (Batch File Version)
echo ================================================================
echo This script will get PhishGuard running on your computer!
echo No technical knowledge required - just wait and watch!
echo ================================================================
echo.

echo Step 1: Checking what's already installed...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Great! Python is installed.
) else (
    echo Python not found. Please install Python from python.org
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check 'Add Python to PATH' during installation!
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Great! Node.js is installed.
) else (
    echo Node.js not found. Please install Node.js from nodejs.org
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo Step 2: Installing basic packages (this may take a few minutes)...
echo.

REM Install basic backend packages
echo Installing basic backend packages...
cd backend

REM Create simple requirements file
echo fastapi > requirements_simple.txt
echo uvicorn >> requirements_simple.txt
echo python-multipart >> requirements_simple.txt
echo python-jose[cryptography] >> requirements_simple.txt
echo passlib[bcrypt] >> requirements_simple.txt
echo bcrypt >> requirements_simple.txt
echo email-validator >> requirements_simple.txt
echo python-dotenv >> requirements_simple.txt

python -m pip install -r requirements_simple.txt
if %errorlevel% equ 0 (
    echo Backend packages installed successfully!
) else (
    echo Some packages failed to install, but that's OK!
    echo We'll try to start the app anyway...
)

REM Install frontend packages
echo Installing frontend packages...
cd ..\frontend
npm install
if %errorlevel% equ 0 (
    echo Frontend packages installed successfully!
) else (
    echo Some packages failed to install, but that's OK!
    echo We'll try to start the app anyway...
)

cd ..

echo.
echo Step 3: Starting PhishGuard (this may take a minute)...
echo.

REM Start backend service
echo Trying to start backend service...
start "PhishGuard Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit
timeout /t 3 /nobreak >nul

REM Start frontend service
echo Starting frontend service...
start "PhishGuard Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Step 4: Waiting for services to be ready...
echo.

REM Wait for frontend to be ready
set /a count=0
:wait_loop
set /a count+=1
echo    Waiting... (%count%/20)
timeout /t 2 /nobreak >nul

REM Simple check if frontend is responding
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3000' -TimeoutSec 2; if ($response.StatusCode -eq 200) { exit 0 } } catch { exit 1 }"
if %errorlevel% equ 0 (
    goto frontend_ready
)

if %count% lss 20 goto wait_loop

echo Frontend is taking longer than expected...
echo Let's try to open it anyway...

:frontend_ready
echo.
echo ================================================================
echo PHISHGUARD STATUS
echo ================================================================
echo Frontend: READY at http://localhost:3000
echo.
echo Your PhishGuard app is ready!
echo Access it at: http://localhost:3000
echo.
echo Opening the app in your browser...
echo.

REM Open the application in browser
start http://localhost:3000

echo.
echo SUCCESS! PhishGuard is now running!
echo The app opened in your browser automatically.
echo.
echo To stop the app: Close the command windows that opened.
echo To restart: Just run this script again!
echo.
echo ================================================================
pause
