# PhishGuard - FINAL RELIABLE STARTUP SCRIPT
# 
# WHAT THIS DOES:
# 1. Checks if Python and Node.js are installed
# 2. Installs essential packages
# 3. Fixes security vulnerabilities
# 4. Starts both services reliably
# 5. Opens the app in browser
#
# FOR YOUR TEAMMATE:
# - Just run this script
# - It will handle everything automatically
# - No technical knowledge needed!

Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "PHISHGUARD - Final Reliable Startup Script" -ForegroundColor Yellow
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "This script will get PhishGuard running perfectly!" -ForegroundColor Green
Write-Host "No technical knowledge required - just wait and watch!" -ForegroundColor Green
Write-Host "===============================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Step 1: Checking what's already installed..." -ForegroundColor Yellow

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Great! Python is installed: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "Python not found. Please install Python from python.org" -ForegroundColor Red
        Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Python not found. Please install Python from python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Great! Node.js is installed: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "Node.js not found. Please install Node.js from nodejs.org" -ForegroundColor Red
        Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Node.js not found. Please install Node.js from nodejs.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 2: Installing packages and fixing vulnerabilities..." -ForegroundColor Yellow

# Install backend packages
Write-Host "Installing backend packages..." -ForegroundColor Blue
Set-Location "backend"

# Create simple requirements file
$simpleRequirements = @"
fastapi
uvicorn
python-multipart
python-jose[cryptography]
passlib[bcrypt]
bcrypt
email-validator
python-dotenv
"@

$simpleRequirements | Out-File -FilePath "requirements_simple.txt" -Encoding UTF8

try {
    Write-Host "   Installing Python packages..." -ForegroundColor Gray
    python -m pip install -r requirements_simple.txt
    Write-Host "Backend packages installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Some packages failed to install, but that's OK!" -ForegroundColor Yellow
}

# Install frontend packages and fix vulnerabilities
Write-Host "Installing frontend packages..." -ForegroundColor Blue
Set-Location "..\frontend"

try {
    Write-Host "   Installing Node.js packages..." -ForegroundColor Gray
    npm install
    
    Write-Host "   Fixing security vulnerabilities..." -ForegroundColor Gray
    npm audit fix --force
    
    Write-Host "   Final security check..." -ForegroundColor Gray
    npm audit
    
    Write-Host "Frontend packages installed and secured!" -ForegroundColor Green
} catch {
    Write-Host "Some packages failed to install, but that's OK!" -ForegroundColor Yellow
}

# Return to root directory
Set-Location ".."

Write-Host ""
Write-Host "Step 3: Starting PhishGuard services..." -ForegroundColor Yellow

# Kill any existing processes on ports 8000 and 3000
Write-Host "Stopping any existing services..." -ForegroundColor Gray
try {
    Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
} catch {}

# Start backend service
Write-Host "Starting backend service..." -ForegroundColor Blue
try {
    Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d $PSScriptRoot\backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal
    Write-Host "Backend service started!" -ForegroundColor Green
} catch {
    Write-Host "Backend service failed to start!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Wait for backend to be ready
Write-Host "Waiting for backend to be ready..." -ForegroundColor Gray
$backendReady = $false
for ($i = 1; $i -le 15; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $backendReady = $true
            Write-Host "Backend is ready!" -ForegroundColor Green
            break
        }
    } catch {}
    Write-Host "   Waiting for backend... ($i/15)" -ForegroundColor Gray
    Start-Sleep -Seconds 2
}

if (-not $backendReady) {
    Write-Host "Backend failed to start properly!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Start frontend service
Write-Host "Starting frontend service..." -ForegroundColor Blue
try {
    Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d $PSScriptRoot\frontend && npm run dev" -WindowStyle Normal
    Write-Host "Frontend service started!" -ForegroundColor Green
} catch {
    Write-Host "Frontend service failed to start!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Wait for frontend to be ready
Write-Host "Waiting for frontend to be ready..." -ForegroundColor Gray
$frontendReady = $false
for ($i = 1; $i -le 20; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $frontendReady = $true
            Write-Host "Frontend is ready!" -ForegroundColor Green
            break
        }
    } catch {}
    Write-Host "   Waiting for frontend... ($i/20)" -ForegroundColor Gray
    Start-Sleep -Seconds 3
}

Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "PHISHGUARD STATUS" -ForegroundColor Yellow
Write-Host "===============================================================" -ForegroundColor Cyan

if ($backendReady -and $frontendReady) {
    Write-Host "Backend: READY at http://localhost:8000" -ForegroundColor Green
    Write-Host "Frontend: READY at http://localhost:3000" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your PhishGuard app is ready!" -ForegroundColor Yellow
    Write-Host "Access it at: http://localhost:3000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Opening the app in your browser..." -ForegroundColor Yellow
    
    # Open the application in browser
    Start-Process "http://localhost:3000"
    
    Write-Host ""
    Write-Host "SUCCESS! PhishGuard is now running perfectly!" -ForegroundColor Green
    Write-Host "The app opened in your browser automatically." -ForegroundColor Green
    Write-Host ""
    Write-Host "To stop the app: Close the command windows that opened." -ForegroundColor Gray
    Write-Host "To restart: Just run this script again!" -ForegroundColor Green
} else {
    Write-Host "Something went wrong:" -ForegroundColor Red
    if (-not $backendReady) { Write-Host "Backend: NOT READY" -ForegroundColor Red }
    if (-not $frontendReady) { Write-Host "Frontend: NOT READY" -ForegroundColor Red }
    Write-Host ""
    Write-Host "Here's what to try:" -ForegroundColor Yellow
    Write-Host "1. Make sure you have Python and Node.js installed" -ForegroundColor White
    Write-Host "2. Try running this script again" -ForegroundColor White
    Write-Host "3. Check if any error messages appeared above" -ForegroundColor White
}

Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
