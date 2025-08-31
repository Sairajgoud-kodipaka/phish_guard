# PhishGuard Application Startup Script (PowerShell)
# ALL-IN-ONE SCRIPT - Setup and run PhishGuard for your team
# 
# WHAT THIS SCRIPT DOES:
# 1. Checks system requirements (Python, Node.js, npm)
# 2. Installs all dependencies automatically
# 3. Starts both backend and frontend services
# 4. Opens the application in your browser
# 5. Provides clear status and instructions
#
# FOR YOUR TEAMMATES:
# - Just run this script on any Windows PC
# - It will handle everything automatically
# - No manual setup required!

Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "PHISHGUARD - AI-Powered Email Security Platform" -ForegroundColor Yellow
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "This is an ALL-IN-ONE script for your team!" -ForegroundColor Green
Write-Host "Automatically sets up and runs everything" -ForegroundColor Green
Write-Host "Backend: FastAPI + ML Models (Port 8000)" -ForegroundColor Blue
Write-Host "Frontend: Next.js + React (Port 3000)" -ForegroundColor Magenta
Write-Host "AI: Spam Detection & Threat Analysis" -ForegroundColor Cyan
Write-Host "===============================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Checking system requirements..." -ForegroundColor Yellow

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK Python found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "ERROR Python not found. Please install Python 3.8+" -ForegroundColor Red
        Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "ERROR Python not found. Please install Python 3.8+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK Node.js found: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "ERROR Node.js not found. Please install Node.js" -ForegroundColor Red
        Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "ERROR Node.js not found. Please install Node.js" -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if npm is available
try {
    $npmVersion = npm --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK npm found: $npmVersion" -ForegroundColor Green
    } else {
        Write-Host "ERROR npm not found. Please install npm" -ForegroundColor Red
        Write-Host "Usually comes with Node.js" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "ERROR npm not found. Please install npm" -ForegroundColor Red
    Write-Host "Usually comes with Node.js" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow

# Install backend dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Blue
Set-Location "backend"
try {
    Write-Host "   Installing Python packages..." -ForegroundColor Gray
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK Backend dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "ERROR Failed to install backend dependencies" -ForegroundColor Red
        Write-Host "Try running: python -m pip install --upgrade pip" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "ERROR Failed to install backend dependencies" -ForegroundColor Red
    Write-Host "Try running: python -m pip install --upgrade pip" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Blue
Set-Location "..\frontend"
try {
    Write-Host "   Installing Node.js packages..." -ForegroundColor Gray
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK Frontend dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "ERROR Failed to install frontend dependencies" -ForegroundColor Red
        Write-Host "Try running: npm cache clean --force" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "ERROR Failed to install frontend dependencies" -ForegroundColor Red
    Write-Host "Try running: npm cache clean --force" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Return to root directory
Set-Location ".."

Write-Host ""
Write-Host "Starting PhishGuard services..." -ForegroundColor Yellow

# Start backend in a new window
Write-Host "Starting backend service..." -ForegroundColor Blue
Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d $PSScriptRoot\backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal

# Wait a bit for backend to start
Write-Host "   Waiting for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# Start frontend in a new window
Write-Host "Starting frontend service..." -ForegroundColor Blue
Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d $PSScriptRoot\frontend && npm run dev" -WindowStyle Normal

# Wait a bit for frontend to start
Write-Host "   Waiting for frontend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow

# Wait for services to be ready
$backendReady = $false
$frontendReady = $false

for ($i = 1; $i -le 30; $i++) {
    if (-not $backendReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $backendReady = $true
                Write-Host "OK Backend service is ready at http://localhost:8000" -ForegroundColor Green
            }
        } catch {
            # Service not ready yet
        }
    }
    
    if (-not $frontendReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $frontendReady = $true
                Write-Host "OK Frontend service is ready at http://localhost:3000" -ForegroundColor Green
            }
        } catch {
            # Service not ready yet
        }
    }
    
    if ($backendReady -and $frontendReady) {
        break
    }
    
    Write-Host "   Waiting... ($i/30)" -ForegroundColor Gray
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "PHISHGUARD STATUS - READY!" -ForegroundColor Yellow
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "Backend: RUNNING (http://localhost:8000)" -ForegroundColor Green
Write-Host "Frontend: RUNNING (http://localhost:3000)" -ForegroundColor Green
Write-Host ""
Write-Host "Your PhishGuard application is ready!" -ForegroundColor Yellow
Write-Host "Main Application: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: Close the command windows to stop the services" -ForegroundColor Gray
Write-Host "To restart: Just run this script again!" -ForegroundColor Green
Write-Host "===============================================================" -ForegroundColor Cyan

# Open the application in browser
Write-Host ""
Write-Host "Opening PhishGuard application..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"
Start-Process "http://localhost:8000/docs"

Write-Host ""
Write-Host "PhishGuard started successfully!" -ForegroundColor Green
Write-Host "Services are running in separate command windows." -ForegroundColor Gray
Write-Host "Close those windows to stop the services." -ForegroundColor Gray
Write-Host ""
Write-Host "FOR YOUR TEAM:" -ForegroundColor Yellow
Write-Host "   - Share this script with your teammates" -ForegroundColor White
Write-Host "   - They just need Python + Node.js installed" -ForegroundColor White
Write-Host "   - Run this script and everything works!" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit this launcher (services will continue running)"
