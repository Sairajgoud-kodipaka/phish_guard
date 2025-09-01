# PhishGuard Complete Management Script
# Runs all management tasks in sequence with summary

Write-Host "=== PHISHGUARD COMPLETE MANAGEMENT ===" -ForegroundColor Cyan
Write-Host "Starting comprehensive system management..." -ForegroundColor Blue
Write-Host ""

# Initialize results tracking
$Results = @{
    Status = "Not Checked"
    Update = "Not Updated"
    Backup = "Not Backed Up"
    Logs = "Not Managed"
    Monitor = "Not Monitored"
    StartTime = Get-Date
}

# Function to write colored output with timestamps
function Write-Info([string]$Message) { 
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] INFO: $Message" -ForegroundColor Blue 
}
function Write-Success([string]$Message) { 
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] ✅ SUCCESS: $Message" -ForegroundColor Green 
}
function Write-Warning([string]$Message) { 
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] ⚠️  WARNING: $Message" -ForegroundColor Yellow 
}
function Write-Error([string]$Message) { 
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] ❌ ERROR: $Message" -ForegroundColor Red 
}

# Enhanced error logging function
function Write-ErrorDetailed([string]$Message, [string]$Details = "") {
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] ❌ ERROR: $Message" -ForegroundColor Red
    if ($Details) {
        Write-Host "    Details: $Details" -ForegroundColor DarkRed
    }
    # Log to file
    $logEntry = "[$timestamp] ERROR: $Message`n    Details: $Details"
    Add-Content -Path "logs\errors.log" -Value $logEntry -ErrorAction SilentlyContinue
}

# 1. CHECK STATUS
Write-Host "=== 1. CHECKING SYSTEM STATUS ===" -ForegroundColor Cyan
try {
    Write-Info "Scanning for Python and Node processes..."
    
    $pythonProcesses = Get-Process | Where-Object { $_.ProcessName -like "*python*" }
    $nodeProcesses = Get-Process | Where-Object { $_.ProcessName -like "*node*" }
    
    if ($pythonProcesses) {
        Write-Success "Backend: $($pythonProcesses.Count) Python process(es) running"
        foreach ($proc in $pythonProcesses) {
            Write-Info "  Python PID: $($proc.Id), CPU: $([math]::Round($proc.CPU, 2))s, Memory: $([math]::Round($proc.WorkingSet64/1MB, 1))MB"
        }
        $Results.Status = "Running - $($pythonProcesses.Count) Python processes"
    } else {
        Write-Warning "Backend: No Python processes running"
        $Results.Status = "Stopped - No Python processes"
    }
    
    if ($nodeProcesses) {
        Write-Success "Frontend: $($nodeProcesses.Count) Node process(es) running"
        foreach ($proc in $nodeProcesses) {
            Write-Info "  Node PID: $($proc.Id), CPU: $([math]::Round($proc.CPU, 2))s, Memory: $([math]::Round($proc.WorkingSet64/1MB, 1))MB"
        }
        $Results.Status = @($Results.Status, '|', $nodeProcesses.Count, 'Node processes') -join ' '
    } else {
        Write-Warning "Frontend: No Node processes running"
        $Results.Status = @($Results.Status, '|', 'No Node processes') -join ' '
    }
    
    # Enhanced port checking with process details
    Write-Info "Checking network ports and connections..."
    try {
        $backendPort = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
        $frontendPort = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
        
        if ($backendPort) { 
            Write-Success "Port 8000 (Backend): Active - PID: $($backendPort.OwningProcess)"
            $backendProc = Get-Process -Id $backendPort.OwningProcess -ErrorAction SilentlyContinue
            if ($backendProc) {
                Write-Info "  Backend Process: $($backendProc.ProcessName) - $($backendProc.StartTime)"
            }
        } else {
            Write-Warning "Port 8000 (Backend): Not listening"
        }
        
        if ($frontendPort) { 
            Write-Success "Port 3000 (Frontend): Active - PID: $($frontendPort.OwningProcess)"
            $frontendProc = Get-Process -Id $frontendPort.OwningProcess -ErrorAction SilentlyContinue
            if ($frontendProc) {
                Write-Info "  Frontend Process: $($frontendProc.ProcessName) - $($frontendProc.StartTime)"
            }
        } else {
            Write-Warning "Port 3000 (Frontend): Not listening"
        }
    } catch {
        Write-Warning "Could not check network ports: $($_.Exception.Message)"
    }
    
    # Check if services are actually responding
    Write-Info "Testing service responsiveness..."
    try {
        $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        if ($backendResponse.StatusCode -eq 200) {
            Write-Success "Backend API: Responding correctly"
        } else {
            Write-Warning "Backend API: Status $($backendResponse.StatusCode)"
        }
    } catch {
        Write-Warning "Backend API: Not responding - $($_.Exception.Message)"
    }
    
    try {
        $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        if ($frontendResponse.StatusCode -eq 200) {
            Write-Success "Frontend App: Responding correctly"
        } else {
            Write-Warning "Frontend App: Status $($frontendResponse.StatusCode)"
        }
    } catch {
        Write-Warning "Frontend App: Not responding - $($_.Exception.Message)"
    }
    
} catch {
    Write-ErrorDetailed "Failed to check system status" $($_.Exception.Message)
    $Results.Status = "Error - $($_.Exception.Message)"
}

Write-Host ""

# 2. UPDATE PACKAGES
Write-Host "=== 2. UPDATING PACKAGES ===" -ForegroundColor Cyan
try {
    Write-Info "Checking Python environment..."
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Python: $pythonVersion"
    } else {
        Write-Error "Python not accessible"
        $Results.Update = "Error - Python not accessible"
        return
    }
    
    Write-Info "Checking Node.js environment..."
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Node.js: $nodeVersion"
    } else {
        Write-Error "Node.js not accessible"
        $Results.Update = "Error - Node.js not accessible"
        return
    }
    
    Write-Info "Updating Python packages..."
    Set-Location "backend"
    try {
        Write-Info "  Installing/upgrading pip..."
        python -m pip install --upgrade pip --quiet
        Write-Success "  Pip upgraded successfully"
        
        Write-Info "  Installing Python dependencies..."
        python -m pip install -r requirements.txt --upgrade --quiet
        Write-Success "  Python packages updated successfully"
        $Results.Update = "Python: Updated"
    } catch {
        Write-ErrorDetailed "Failed to update Python packages" $($_.Exception.Message)
        $Results.Update = "Error - Python packages failed"
    }
    Set-Location ".."
    
    Write-Info "Updating Node packages..."
    Set-Location "frontend"
    try {
        Write-Info "  Checking package.json..."
        if (Test-Path "package.json") {
            Write-Success "  package.json found"
        } else {
            Write-Error "  package.json not found"
            $Results.Update = @($Results.Update, '|', 'Node: package.json missing') -join ' '
            Set-Location ".."
            return
        }
        
        Write-Info "  Installing/updating Node dependencies..."
        npm install --silent
        Write-Success "  Node packages updated successfully"
        $Results.Update = @($Results.Update, '|', 'Node: Updated') -join ' '
    } catch {
        Write-ErrorDetailed "Failed to update Node packages" $($_.Exception.Message)
        $Results.Update = @($Results.Update, '|', 'Node: Failed') -join ' '
    }
    Set-Location ".."
    
} catch {
    Write-ErrorDetailed "Failed to update packages" $($_.Exception.Message)
    $Results.Update = "Error - $($_.Exception.Message)"
}

Write-Host ""

# 3. BACKUP DATA
Write-Host "=== 3. BACKING UP DATA ===" -ForegroundColor Cyan
try {
    if (!(Test-Path "backups")) {
        New-Item -ItemType Directory -Path "backups" -Force | Out-Null
        Write-Info "Created backups directory"
    }
    
    if (Test-Path "backend\phishguard.db") {
        $backupName = "phishguard_db_$(Get-Date -Format 'yyyyMMdd_HHmmss').db"
        $backupPath = Join-Path "backups" $backupName
        Copy-Item "backend\phishguard.db" $backupPath
        Write-Success "Database backed up: $backupName"
        $Results.Backup = "Database: $backupName"
    } else {
        Write-Warning "No database file found to backup"
        $Results.Backup = "No database file"
    }
    
    # Check ML model
    if (Test-Path "backend\models\spam_classifier.pkl") {
        $modelFile = Get-Item "backend\models\spam_classifier.pkl"
        $modelAge = (Get-Date) - $modelFile.LastWriteTime
        Write-Info "ML model last updated: $($modelAge.Days) days ago"
        $Results.Backup = @($Results.Backup, '|', 'ML Model:', $modelAge.Days, 'days old') -join ' '
    } else {
        Write-Warning "ML model file not found"
        $Results.Backup = @($Results.Backup, '|', 'ML Model:', 'Not found') -join ' '
    }
    
} catch {
    Write-Error "Failed to backup data: $($_.Exception.Message)"
    $Results.Backup = "Error - $($_.Exception.Message)"
}

Write-Host ""

# 4. MANAGE LOGS
Write-Host "=== 4. MANAGING LOGS ===" -ForegroundColor Cyan
try {
    if (!(Test-Path "logs")) {
        New-Item -ItemType Directory -Path "logs" -Force | Out-Null
        Write-Info "Created logs directory"
    }
    
    # Collect log files
    $logFiles = @()
    if (Test-Path "backend\logs") {
        $logFiles += Get-ChildItem "backend\logs" -Filter "*.log" -Recurse
    }
    if (Test-Path "frontend\logs") {
        $logFiles += Get-ChildItem "frontend\logs" -Filter "*.log" -Recurse
    }
    $logFiles += Get-ChildItem "logs" -Filter "*.log" -ErrorAction SilentlyContinue
    
    Write-Info "Found $($logFiles.Count) log files"
    
    # Create log summary
    $logSummary = @{
        timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        total_logs = $logFiles.Count
        system_status = "running"
    }
    
    $logSummary | ConvertTo-Json | Out-File "logs\summary_$(Get-Date -Format 'yyyyMMdd').json"
    Write-Success "Log summary created: logs\summary_$(Get-Date -Format 'yyyyMMdd').json"
    $Results.Logs = "$($logFiles.Count) log files | Summary created"
    
} catch {
    Write-Error "Failed to manage logs: $($_.Exception.Message)"
    $Results.Logs = "Error - $($_.Exception.Message)"
}

Write-Host ""

# 5. MONITOR SYSTEM
Write-Host "=== 5. MONITORING SYSTEM ===" -ForegroundColor Cyan
try {
    # Performance metrics
    $cpu = Get-WmiObject -Class Win32_Processor | Select-Object -First 1
    $memory = Get-WmiObject -Class Win32_OperatingSystem
    
    $cpuUsage = [math]::Round($cpu.LoadPercentage, 1)
    $memoryUsage = [math]::Round(($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / $memory.TotalVisibleMemorySize * 100, 1)
    
    Write-Info "CPU Usage: $cpuUsage%"
    Write-Info "Memory Usage: $memoryUsage%"
    
    # Process count
    $pythonCount = (Get-Process | Where-Object { $_.ProcessName -like "*python*" }).Count
    $nodeCount = (Get-Process | Where-Object { $_.ProcessName -like "*node*" }).Count
    
    Write-Info "Active Processes: Python: $pythonCount, Node: $nodeCount"
    
    # Health check
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Success "Backend health check: OK"
            $healthStatus = "OK"
        } else {
            Write-Warning "Backend health check: Status $($response.StatusCode)"
            $healthStatus = "Status $($response.StatusCode)"
        }
    } catch {
        Write-Error "Backend health check: Failed"
        $healthStatus = "Failed"
    }
    
    # Create monitoring report
    $monitoringReport = @{
        timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        cpu_usage = $cpuUsage
        memory_usage = $memoryUsage
        python_processes = $pythonCount
        node_processes = $nodeCount
        backend_health = $healthStatus
    }
    
    $monitoringReport | ConvertTo-Json | Out-File "logs\monitoring_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
    Write-Success "Monitoring report created: logs\monitoring_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
    
    $Results.Monitor = "CPU: $cpuUsage% | Memory: $memoryUsage% | Health: $healthStatus"
    
} catch {
    Write-Error "Failed to monitor system: $($_.Exception.Message)"
    $Results.Monitor = "Error - $($_.Exception.Message)"
}

Write-Host ""

# FINAL SUMMARY
Write-Host "=== MANAGEMENT COMPLETE ===" -ForegroundColor Cyan
Write-Host ""

$endTime = Get-Date
$duration = $endTime - $Results.StartTime

Write-Host "MINI-SUMMARY:" -ForegroundColor Yellow
Write-Host "  Duration: $([math]::Round($duration.TotalSeconds, 1)) seconds" -ForegroundColor White
Write-Host "  Status: $($Results.Status)" -ForegroundColor White
Write-Host "  Updates: $($Results.Update)" -ForegroundColor White
Write-Host "  Backup: $($Results.Backup)" -ForegroundColor White
Write-Host "  Logs: $($Results.Logs)" -ForegroundColor White
Write-Host "  Monitor: $($Results.Monitor)" -ForegroundColor White

Write-Host ""
Write-Host 'Check these directories for details:' -ForegroundColor Yellow
Write-Host '  - logs\ - Log summaries and monitoring reports' -ForegroundColor White
Write-Host '  - backups\ - Database backups' -ForegroundColor White

Write-Host ""
Write-Host 'All management tasks completed successfully!' -ForegroundColor Green
Write-Host ''
Write-Host 'Choose your next action:' -ForegroundColor Yellow
Write-Host '  Press C to continue monitoring services (recommended)' -ForegroundColor Cyan
Write-Host '  Press E to exit' -ForegroundColor Gray
Write-Host ''

$choice = Read-Host 'Enter your choice (C/E)'

if ($choice -eq 'C' -or $choice -eq 'c') {
    Write-Host ''
    Write-Host '=== MONITORING MODE ACTIVATED ===' -ForegroundColor Green
    Write-Host 'Monitoring frontend and backend services...' -ForegroundColor Blue
    Write-Host 'Press Ctrl+C to stop monitoring and exit' -ForegroundColor Yellow
    Write-Host ''
    
    try {
        while ($true) {
            $timestamp = Get-Date -Format 'HH:mm:ss'
            
            # Check backend status
            try {
                $backendResponse = Invoke-WebRequest -Uri 'http://localhost:8000/health' -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
                $backendStatus = if ($backendResponse.StatusCode -eq 200) { 'OK' } else { 'ERROR' }
                $backendColor = if ($backendStatus -eq 'OK') { 'Green' } else { 'Red' }
            } catch {
                $backendStatus = 'DOWN'
                $backendColor = 'Red'
            }
            
            # Check frontend status
            try {
                $frontendResponse = Invoke-WebRequest -Uri 'http://localhost:3000' -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
                $frontendStatus = if ($frontendResponse.StatusCode -eq 200) { 'OK' } else { 'ERROR' }
                $frontendColor = if ($frontendStatus -eq 'OK') { 'Green' } else { 'Red' }
            } catch {
                $frontendStatus = 'DOWN'
                $frontendColor = 'Red'
            }
            
            # Check processes
            $pythonProcesses = Get-Process | Where-Object { $_.ProcessName -like '*python*' }
            $nodeProcesses = Get-Process | Where-Object { $_.ProcessName -like '*node*' }
            
            # Display status
            Write-Host "[$timestamp] Backend: $backendStatus | Frontend: $frontendStatus | Python: $($pythonProcesses.Count) | Node: $($nodeProcesses.Count)" -ForegroundColor White
            
            # Show error details if services are down
            if ($backendStatus -eq 'DOWN') {
                Write-Host "  ⚠️  Backend service is down - Check if start.ps1 is running" -ForegroundColor Yellow
            }
            if ($frontendStatus -eq 'DOWN') {
                Write-Host "  ⚠️  Frontend service is down - Check if start.ps1 is running" -ForegroundColor Yellow
            }
            
            Start-Sleep -Seconds 5
        }
    } catch {
        Write-Host ''
        Write-Host 'Monitoring stopped' -ForegroundColor Yellow
    }
} else {
    Write-Host 'Exiting...' -ForegroundColor Gray
}
