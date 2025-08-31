# Test PhishGuard Connection
Write-Host "Testing PhishGuard connections..." -ForegroundColor Yellow

Write-Host ""
Write-Host "Testing Backend (Port 8000)..." -ForegroundColor Blue
try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 5
    Write-Host "✅ Backend is responding: Status $($backendResponse.StatusCode)" -ForegroundColor Green
    
    # Test specific API endpoint
    $apiResponse = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/emails/stats/summary?days=30" -TimeoutSec 5
    Write-Host "✅ API endpoint is working: Status $($apiResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend connection failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Testing Frontend (Port 3000)..." -ForegroundColor Blue
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5
    Write-Host "✅ Frontend is responding: Status $($frontendResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend connection failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Testing CORS..." -ForegroundColor Blue
try {
    $corsResponse = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/emails/stats/summary?days=30" -Method OPTIONS -TimeoutSec 5
    Write-Host "✅ CORS preflight is working: Status $($corsResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "❌ CORS test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Connection test complete!" -ForegroundColor Yellow
