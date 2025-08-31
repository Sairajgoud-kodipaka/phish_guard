# 🚀 PhishGuard Startup Guide

## 🎯 One-Click Application Startup

PhishGuard is now equipped with **single-script startup** that automatically:
- ✅ Checks system requirements
- ✅ Installs all dependencies
- ✅ Starts both backend and frontend services
- ✅ Opens the application in your browser
- ✅ Tests ML functionality
- ✅ Provides real-time status monitoring

---

## 🖥️ **Windows Users (Recommended)**

### **Option 1: PowerShell Script (Best for Windows 10/11)**
1. **Right-click** `start_phishguard.ps1`
2. **Select** "Run with PowerShell"
3. **Wait** for the automatic setup (5-10 minutes)
4. **Enjoy** your running PhishGuard application!

### **Option 2: Batch File (Classic Windows)**
1. **Double-click** `start_phishguard.bat`
2. **Wait** for the automatic setup (5-10 minutes)
3. **Enjoy** your running PhishGuard application!

### **Option 3: Command Line**
```cmd
# PowerShell (recommended)
powershell -ExecutionPolicy Bypass -File start_phishguard.ps1

# Batch file
start_phishguard.bat
```

---

## 🐧 **Linux/Mac Users**

### **Option 1: Shell Script**
```bash
./start_phishguard.sh
```

### **Option 2: Make Executable First**
```bash
chmod +x start_phishguard.sh
./start_phishguard.sh
```

---

## 🐍 **Python Users (Cross-Platform)**

### **Run Python Script**
```bash
python start_phishguard.py
```

---

## 📋 **What Happens Automatically**

### **1. System Check** 🔍
- ✅ Python 3.8+ verification
- ✅ Node.js verification  
- ✅ npm verification
- ✅ Directory structure check

### **2. Dependency Installation** 📦
- ✅ Backend Python packages
- ✅ Frontend npm packages
- ✅ ML/AI libraries
- ✅ Database drivers

### **3. Service Startup** 🚀
- ✅ FastAPI backend (port 8000)
- ✅ Next.js frontend (port 3000)
- ✅ Automatic service monitoring
- ✅ Health check verification

### **4. Application Ready** 🎯
- ✅ Browser automatically opens
- ✅ Frontend dashboard accessible
- ✅ API documentation available
- ✅ ML endpoints functional

---

## 🌐 **Access Your Application**

Once the startup script completes:

- **🎨 Frontend Dashboard**: http://localhost:3000
- **🔒 Backend API**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs
- **🤖 ML Endpoints**: Available via API

---

## 🛑 **Stopping the Application**

### **Windows (Batch File)**
- Close the command windows that opened
- Or press `Ctrl+C` in the launcher

### **Windows (PowerShell)**
- Close the command windows that opened
- Or press `Enter` in the launcher

### **Linux/Mac (Shell Script)**
- Press `Ctrl+C` in the terminal

### **Python Script**
- Press `Ctrl+C` in the terminal

---

## 🔧 **Manual Startup (Alternative)**

If you prefer manual control:

### **Backend Service**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Frontend Service**
```bash
cd frontend
npm run dev
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Port Already in Use**
```bash
# Check what's using the ports
netstat -an | findstr ":8000\|:3000"  # Windows
lsof -i :8000,3000                     # Linux/Mac
```

#### **2. Dependencies Failed**
```bash
# Reinstall backend dependencies
cd backend
pip install -r requirements.txt

# Reinstall frontend dependencies  
cd frontend
npm install
```

#### **3. Services Not Starting**
- Check if Python and Node.js are properly installed
- Ensure you have sufficient permissions
- Check firewall settings

#### **4. ML Model Issues**
```bash
# Test ML functionality
cd backend
python test_with_sample_data.py
```

#### **5. PowerShell Execution Policy (Windows)**
If you get execution policy errors:
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 **System Requirements**

### **Minimum Requirements**
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space

### **Recommended Requirements**
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.9 or higher
- **Node.js**: 18.0 or higher
- **RAM**: 8GB or higher
- **Storage**: 5GB free space

---

## 🎉 **Success Indicators**

When PhishGuard starts successfully, you'll see:

```
===============================================================
PHISHGUARD STATUS
===============================================================
Backend: RUNNING (http://localhost:8000)
Frontend: RUNNING (http://localhost:3000)

Your PhishGuard application is ready!
Access your application at: http://localhost:3000
API documentation at: http://localhost:8000/docs
===============================================================
```

---

## 🔍 **Verification Commands**

### **Check Backend Status**
```bash
curl http://localhost:8000/docs
```

### **Check Frontend Status**
```bash
curl http://localhost:3000
```

### **Check ML Endpoints**
```bash
curl http://localhost:8000/api/v1/threats/ml-model-info
```

---

## 💡 **Pro Tips**

1. **First Run**: The initial startup may take 5-10 minutes for dependency installation
2. **Subsequent Runs**: Much faster as dependencies are already installed
3. **Development Mode**: Both services run with auto-reload enabled
4. **Browser**: The script automatically opens your default browser
5. **Background**: Services continue running even if you close the launcher
6. **Windows Users**: PowerShell script provides better error handling and colored output

---

## 🆘 **Need Help?**

If you encounter issues:

1. **Check the error messages** in the terminal
2. **Verify system requirements** are met
3. **Try manual startup** as an alternative
4. **Check the troubleshooting section** above
5. **Review the logs** in the service windows

---

## 🎯 **Ready to Go!**

Your PhishGuard application is now equipped with **one-click startup** that handles everything automatically. Just run the appropriate script for your operating system and enjoy your AI-powered email security platform!

**🚀 Happy PhishGuarding! 🚀** 