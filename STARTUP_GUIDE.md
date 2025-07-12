# PhishGuard - Quick Start Guide

## 🚀 Get PhishGuard Running in 2 Steps

### Step 1: Start Backend (Port 8001)
```bash
cd backend
python run_production.py
```

You should see:
```
🚀 Starting PhishGuard Production Backend...
📊 Full ML capabilities enabled  
🔒 Advanced threat analysis active
🌐 Server will be available at: http://localhost:8001
```

### Step 2: Start Frontend (Port 3000)
```bash
cd frontend
npm run dev
```

You should see:
```
▲ Next.js 14.0.0
- Local:        http://localhost:3000
- Network:      http://0.0.0.0:3000
```

## ✅ Verify Everything Works

### Test Backend Connection:
```bash
cd backend
python test_connection.py
```

This will test all endpoints and show if everything is working.

### Test Frontend:
1. Open http://localhost:3000/dashboard
2. Click "Analyze Email" 
3. Paste a sample phishing email
4. You should see real threat analysis results

## 🔧 Troubleshooting

### Backend Issues:
- **Port 8001 in use?** Change port in `backend/run_production.py`
- **Database errors?** Delete `backend/phishguard.db` and restart
- **Import errors?** Run `pip install fastapi uvicorn sqlalchemy aiosqlite`

### Frontend Issues:
- **Connection refused?** Make sure backend is running on port 8001
- **CORS errors?** Backend has CORS enabled for all origins
- **Loading forever?** Check browser console for specific error messages

### Connection Test:
```bash
# Test if backend is responding
curl http://localhost:8001/health

# Should return: {"status":"healthy","service":"PhishGuard Backend"...}
```

## 📧 Sample Phishing Email for Testing

Paste this into the email analyzer to see the threat detection in action:

```
From: urgent-payment@fake-bank.com
To: user@example.com  
Subject: URGENT: Verify Your Account Now!

Dear Customer,

Your account has been suspended due to suspicious activity. 
Click here to verify your account immediately: http://fake-bank.com/verify

This is urgent and must be completed within 24 hours.

Thank you,
Security Team
```

Expected result: **High threat score** with phishing indicators detected.

## 🎯 What Should Happen

1. **Backend** analyzes emails using advanced heuristics
2. **Database** stores all analyzed emails with threat details  
3. **Frontend** shows real-time stats and analysis results
4. **Dashboard** updates with actual data from analyzed emails

## 📊 Key Features Working

- ✅ Real email parsing (.eml, .msg, text)
- ✅ Advanced threat analysis (phishing, spam, malware detection)
- ✅ URL scanning and domain reputation
- ✅ Attachment analysis
- ✅ Authentication validation (SPF/DKIM/DMARC)
- ✅ Real database storage
- ✅ Live dashboard with actual statistics
- ✅ Recently analyzed emails display

## 🔗 Endpoints Available

- Frontend: http://localhost:3000
- Backend API: http://localhost:8001/docs
- Health Check: http://localhost:8001/health
- Email Analysis: http://localhost:8001/api/v1/emails/analyze-text

That's it! You now have a fully working AI-powered email security platform. 