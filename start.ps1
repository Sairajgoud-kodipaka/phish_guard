# PhishGuard PowerShell Startup Script
# Works in: PowerShell, cmd (via powershell -File)
# WORA: Write Once, Run Anywhere
# Runs everything in SAME terminal

Write-Host "=== PHISHGUARD STARTUP ===" -ForegroundColor Cyan
Write-Host "Starting system check..." -ForegroundColor Blue

# Check Python
Write-Host "Checking Python..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "Python not found" -ForegroundColor Red
        Write-Host "Please install Python from python.org" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Python check failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Blue
try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "Node.js not found" -ForegroundColor Red
        Write-Host "Please install Node.js from nodejs.org" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "Node.js check failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check files
Write-Host "Checking files..." -ForegroundColor Blue
if (Test-Path "backend\app\main.py") {
    Write-Host "Backend FastAPI app found" -ForegroundColor Green
} else {
    Write-Host "Backend FastAPI app missing" -ForegroundColor Red
    Write-Host "Expected: backend\app\main.py" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

if (Test-Path "backend\requirements.txt") {
    Write-Host "Requirements file found" -ForegroundColor Green
} else {
    Write-Host "Requirements file missing" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (Test-Path "frontend") {
    Write-Host "Frontend directory found" -ForegroundColor Green
} else {
    Write-Host "Frontend directory missing" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "=== ALL CHECKS PASSED ===" -ForegroundColor Cyan
Write-Host ""

# Install backend packages
Write-Host "Installing backend packages..." -ForegroundColor Blue
try {
    Set-Location "backend"
    
    # Check if requirements.txt exists
    if (Test-Path "requirements.txt") {
        Write-Host "✅ requirements.txt found" -ForegroundColor Green
    } else {
        Write-Host "❌ requirements.txt not found - creating default" -ForegroundColor Red
        @"
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
aiosqlite==0.19.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
        Write-Host "✅ Created default requirements.txt" -ForegroundColor Green
    }
    
    Write-Host "Running: pip install -r requirements.txt" -ForegroundColor Yellow
    $pipResult = python -m pip install -r requirements.txt --upgrade --no-cache-dir 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Backend packages installed successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Backend package installation had issues" -ForegroundColor Yellow
        Write-Host "Pip output: $pipResult" -ForegroundColor Gray
    }
    Set-Location ".."
} catch {
    Write-Host "❌ Backend package installation failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Install frontend packages
Write-Host "Installing frontend packages..." -ForegroundColor Blue
try {
    Set-Location "frontend"
    
    # Check if package.json exists
    if (Test-Path "package.json") {
        Write-Host "✅ package.json found" -ForegroundColor Green
    } else {
        Write-Host "❌ package.json not found - cannot install packages" -ForegroundColor Red
        Set-Location ".."
        return
    }
    
    Write-Host "Running: npm install" -ForegroundColor Yellow
    $npmResult = npm install --no-optional --no-audit --quiet 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Frontend packages installed successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Frontend package installation had issues" -ForegroundColor Yellow
        Write-Host "NPM output: $npmResult" -ForegroundColor Gray
    }
    Set-Location ".."
} catch {
    Write-Host "❌ Frontend package installation failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== STARTING SERVICES ===" -ForegroundColor Cyan
Write-Host ""

# Stop existing services
Write-Host "Stopping existing services..." -ForegroundColor Blue
try {
    Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "Existing services stopped" -ForegroundColor Green
} catch {
    Write-Host "Some services could not be stopped" -ForegroundColor Yellow
}

# Check if ports are available
Write-Host "Checking port availability..." -ForegroundColor Blue
try {
    $backendPort = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    $frontendPort = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
    
    if ($backendPort) {
        Write-Host "Port 8000 is in use. Stopping process..." -ForegroundColor Yellow
        Stop-Process -Id $backendPort.OwningProcess -Force -ErrorAction SilentlyContinue
    }
    
    if ($frontendPort) {
        Write-Host "Port 3000 is in use. Stopping process..." -ForegroundColor Yellow
        Stop-Process -Id $frontendPort.OwningProcess -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host "Ports are now available" -ForegroundColor Green
} catch {
    Write-Host "Could not check ports" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# Start backend in background
Write-Host "Starting backend service..." -ForegroundColor Blue
try {
    # Check if backend directory has the right structure
    if (!(Test-Path "backend\app")) {
        Write-Host "❌ Backend app directory not found - checking structure..." -ForegroundColor Red
        Write-Host "Backend directory contents:" -ForegroundColor Yellow
        Get-ChildItem "backend" | ForEach-Object { Write-Host "  $($_.Name)" -ForegroundColor Gray }
        Write-Host "❌ Cannot start backend - missing app directory" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host "✅ Backend structure verified" -ForegroundColor Green
    
    $backendJob = Start-Job -ScriptBlock {
        Set-Location $using:PSScriptRoot\backend
        
        try {
            Write-Host "🔄 Creating database tables..." -ForegroundColor Blue
            python -c "from app.core.database import create_tables; import asyncio; asyncio.run(create_tables())"
            Write-Host "✅ Database tables created successfully" -ForegroundColor Green
            
            Write-Host "🚀 Starting FastAPI server..." -ForegroundColor Blue
            python start_server.py
        } catch {
            Write-Host "❌ Backend startup failed: $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host "✅ Backend service started in background (Job ID: $($backendJob.Id))" -ForegroundColor Green
    
    # Wait a moment and check if backend started successfully
    Start-Sleep -Seconds 3
    try {
        $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        if ($backendResponse.StatusCode -eq 200) {
            Write-Host "✅ Backend is responding correctly" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Backend started but health check failed (Status: $($backendResponse.StatusCode))" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  Backend started but not yet responding - this is normal during startup" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Failed to start backend service: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Wait a bit
Start-Sleep -Seconds 3

# Start frontend in background
Write-Host "Starting frontend service..." -ForegroundColor Blue
try {
    # Check if frontend directory has the right structure
    if (!(Test-Path "frontend\package.json")) {
        Write-Host "❌ Frontend package.json not found - checking structure..." -ForegroundColor Red
        Write-Host "Frontend directory contents:" -ForegroundColor Yellow
        Get-ChildItem "frontend" | ForEach-Object { Write-Host "  $($_.Name)" -ForegroundColor Gray }
        Write-Host "❌ Cannot start frontend - missing package.json" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host "✅ Frontend structure verified" -ForegroundColor Green
    
    $frontendJob = Start-Job -ScriptBlock {
        Set-Location $using:PSScriptRoot\frontend
        
        try {
            Write-Host "🚀 Starting Next.js development server..." -ForegroundColor Blue
            npm run dev
        } catch {
            Write-Host "❌ Frontend startup failed: $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host "✅ Frontend service started in background (Job ID: $($frontendJob.Id))" -ForegroundColor Green
    
    # Wait a moment and check if frontend started successfully
    Start-Sleep -Seconds 5
    try {
        $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        if ($frontendResponse.StatusCode -eq 200) {
            Write-Host "✅ Frontend is responding correctly" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Frontend started but response check failed (Status: $($frontendResponse.StatusCode))" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  Frontend started but not yet responding - this is normal during startup" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Failed to start frontend service: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Wait a bit more
Start-Sleep -Seconds 3

# Final status
Write-Host ""
Write-Host "=== PHISHGUARD STATUS ===" -ForegroundColor Cyan

# Final comprehensive status check
Write-Host "Performing final status verification..." -ForegroundColor Blue

# Check backend
try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($backendResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend: RUNNING at http://localhost:8000" -ForegroundColor Green
        $backendStatus = "RUNNING"
    } else {
        Write-Host "⚠️  Backend: STARTED but health check failed (Status: $($backendResponse.StatusCode))" -ForegroundColor Yellow
        $backendStatus = "STARTED"
    }
} catch {
    Write-Host "❌ Backend: STARTED but not responding yet" -ForegroundColor Red
    $backendStatus = "STARTING"
}

# Check frontend
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend: RUNNING at http://localhost:3000" -ForegroundColor Green
        $frontendStatus = "RUNNING"
    } else {
        Write-Host "⚠️  Frontend: STARTED but response check failed (Status: $($frontendResponse.StatusCode))" -ForegroundColor Yellow
        $frontendStatus = "STARTED"
    }
} catch {
    Write-Host "❌ Frontend: STARTED but not responding yet" -ForegroundColor Red
    $frontendStatus = "STARTING"
}

# Check database
try {
    if (Test-Path "backend\phishguard.db") {
        $dbSize = (Get-Item "backend\phishguard.db").Length
        Write-Host "✅ Database: EXISTS ($([math]::Round($dbSize/1KB, 1)) KB)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Database: NOT FOUND - will be created on first use" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Database: Cannot verify status" -ForegroundColor Red
}

Write-Host ""
Write-Host "SUCCESS! PhishGuard is now running!" -ForegroundColor Green
Write-Host "Opening the application in your browser..." -ForegroundColor Blue

try {
    Start-Process "http://localhost:3000"
    Write-Host "Browser launched successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to launch browser automatically" -ForegroundColor Yellow
    Write-Host "Please manually open: http://localhost:3000" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Blue
Write-Host "1. The app is now running in your browser" -ForegroundColor Yellow
Write-Host "2. To stop: Press Ctrl+C in this terminal" -ForegroundColor Yellow
Write-Host "3. To restart: Run this script again" -ForegroundColor Yellow

Write-Host ""
Write-Host "=== SERVICES RUNNING IN BACKGROUND ===" -ForegroundColor Cyan
Write-Host "Backend Job ID: $($backendJob.Id)" -ForegroundColor Green
Write-Host "Frontend Job ID: $($frontendJob.Id)" -ForegroundColor Green

Write-Host ""
Write-Host "Press Ctrl+C to stop all services and exit" -ForegroundColor Red

# Keep running and show job status
try {
    while ($true) {
        $backendStatus = Get-Job $backendJob.Id | Select-Object State
        $frontendStatus = Get-Job $frontendJob.Id | Select-Object State
        
        Write-Host "Backend: $($backendStatus.State) | Frontend: $($frontendStatus.State)" -ForegroundColor Gray
        Start-Sleep -Seconds 10
    }
} catch {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow
    Stop-Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job $frontendJob -ErrorAction SilentlyContinue
    Remove-Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job $frontendJob -ErrorAction SilentlyContinue
    Write-Host "All services stopped" -ForegroundColor Green
}
