@echo off
echo ================================================================
echo PHISHGUARD - AI-Powered Email Security Platform
echo ================================================================
echo Backend: FastAPI + ML Models
echo Frontend: Next.js + React
echo AI: Spam Detection & Threat Analysis
echo ================================================================

echo.
echo Checking system requirements...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo Python found

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js not found. Please install Node.js
    pause
    exit /b 1
)
echo Node.js found

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo npm not found. Please install npm
    pause
    exit /b 1
)
echo npm found

echo.
echo Installing dependencies...

REM Install backend dependencies
echo Installing backend dependencies...
cd backend
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)
echo Backend dependencies installed

REM Install frontend dependencies
echo Installing frontend dependencies...
cd ..\frontend
npm install
if errorlevel 1 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)
echo Frontend dependencies installed

echo.
echo Starting PhishGuard services...

REM Start backend in a new window
echo Starting backend service...
start "PhishGuard Backend" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in a new window
echo Starting frontend service...
start "PhishGuard Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

REM Wait a bit for frontend to start
timeout /t 8 /nobreak >nul

echo.
echo Waiting for services to be ready...

REM Wait for services to be ready
:wait_loop
timeout /t 2 /nobreak >nul

REM Test backend
curl -s http://localhost:8000/docs >nul 2>&1
if errorlevel 1 (
    echo    Waiting for backend... (Ctrl+C to stop)
    goto wait_loop
)
echo Backend service is ready

REM Test frontend
curl -s http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    echo    Waiting for frontend... (Ctrl+C to stop)
    goto wait_loop
)
echo Frontend service is ready

echo.
echo ================================================================
echo PHISHGUARD STATUS
echo ================================================================
echo Backend: RUNNING (http://localhost:8000)
echo Frontend: RUNNING (http://localhost:3000)
echo.
echo Your PhishGuard application is ready!
echo Access your application at: http://localhost:3000
echo API documentation at: http://localhost:8000/docs
echo.
echo Close the command windows to stop the services
echo ================================================================

REM Open the application in browser
echo.
echo Opening PhishGuard application...
start http://localhost:3000
start http://localhost:8000/docs

echo.
echo PhishGuard started successfully!
echo Press any key to exit this launcher (services will continue running)
pause >nul
