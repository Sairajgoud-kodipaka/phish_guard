# 🚀 PhishGuard Quick Start

## ⚡ **One-Click Startup - Choose Your Platform**

### **🖥️ Windows Users**
```powershell
# Option 1: PowerShell (Recommended)
Right-click start_phishguard.ps1 → "Run with PowerShell"

# Option 2: Batch File
Double-click start_phishguard.bat

# Option 3: Command Line
powershell -ExecutionPolicy Bypass -File start_phishguard.ps1
```

### **🐧 Linux/Mac Users**
```bash
# Make executable and run
chmod +x start_phishguard.sh
./start_phishguard.sh
```

### **🐍 Cross-Platform (Python)**
```bash
python start_phishguard.py
```

---

## 🎯 **What Happens Automatically**

1. **✅ System Check** - Verifies Python, Node.js, npm
2. **✅ Dependencies** - Installs all required packages
3. **✅ Services Start** - Launches backend (port 8000) + frontend (port 3000)
4. **✅ Health Check** - Waits for services to be ready
5. **✅ Browser Opens** - Application launches automatically
6. **✅ Ready to Use** - Your PhishGuard is fully operational!

---

## 🌐 **Access Your Application**

- **🎨 Frontend**: http://localhost:3000
- **🔒 Backend API**: http://localhost:8000
- **📚 API Docs**: http://localhost:8000/docs

---

## 🛑 **Stopping Services**

- **Windows**: Close the command windows that opened
- **Linux/Mac**: Press `Ctrl+C` in the terminal
- **Python**: Press `Ctrl+C` in the terminal

---

## 🚨 **Troubleshooting**

- **Port in use?** Check what's using ports 8000/3000
- **Dependencies failed?** Run the script again
- **PowerShell errors?** Run as Administrator and set execution policy

---

## 🎉 **You're Ready!**

Your AI-powered email security platform will be running in minutes with **zero configuration required**!

**🚀 Happy PhishGuarding! 🚀**
