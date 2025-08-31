# PhishGuard Application Startup Script (PowerShell)
# Starts both frontend and backend services and makes the application ready

Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "PHISHGUARD - AI-Powered Email Security Platform" -ForegroundColor Yellow
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "Backend: FastAPI + ML Models" -ForegroundColor Green
Write-Host "Frontend: Next.js + React" -ForegroundColor Blue
Write-Host "AI: Spam Detection & Threat Analysis" -ForegroundColor Magenta
Write-Host "===============================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Checking system requirements..." -ForegroundColor Yellow

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "Python not found. Please install Python 3.8+" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Python not found. Please install Python 3.8+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "Node.js not found. Please install Node.js" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Node.js not found. Please install Node.js" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if npm is available
try {
    $npmVersion = npm --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "npm found: $npmVersion" -ForegroundColor Green
    } else {
        Write-Host "npm not found. Please install npm" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "npm not found. Please install npm" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow

# Install backend dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Blue
Set-Location "backend"
try {
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Backend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "Failed to install backend dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Failed to install backend dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Blue
Set-Location "..\frontend"
try {
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Frontend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "Failed to install frontend dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Failed to install frontend dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Starting PhishGuard services..." -ForegroundColor Yellow

# Start backend in a new window
Write-Host "Starting backend service..." -ForegroundColor Blue
Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d $PSScriptRoot\backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal

# Wait a bit for backend to start
Start-Sleep -Seconds 5

# Start frontend in a new window
Write-Host "Starting frontend service..." -ForegroundColor Blue
Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d $PSScriptRoot\frontend && npm run dev" -WindowStyle Normal

# Wait a bit for frontend to start
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
                Write-Host "Backend service is ready" -ForegroundColor Green
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
                Write-Host "Frontend service is ready" -ForegroundColor Green
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
Write-Host "PHISHGUARD STATUS" -ForegroundColor Yellow
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "Backend: RUNNING (http://localhost:8000)" -ForegroundColor Green
Write-Host "Frontend: RUNNING (http://localhost:3000)" -ForegroundColor Green
Write-Host ""
Write-Host "Your PhishGuard application is ready!" -ForegroundColor Yellow
Write-Host "Access your application at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API documentation at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Close the command windows to stop the services" -ForegroundColor Gray
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
Read-Host "Press Enter to exit this launcher (services will continue running)"
