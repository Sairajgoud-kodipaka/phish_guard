# PhishGuard - Windows Startup Scripts

## 🚀 **THREE SCRIPTS FOR WINDOWS**

**Choose the right script for your needs:**

### **Option 1: Single Terminal (Recommended)**
```
.\start_simple.bat
```
- **Runs everything in SAME terminal**
- **No new windows opened**
- **Perfect for cmd.exe users**

### **Option 2: PowerShell with Background Jobs**
```
.\start.ps1
```
- **Runs everything in SAME PowerShell terminal**
- **Uses background jobs**
- **Shows real-time status**

### **Option 3: Separate Windows (Original)**
```
.\start.bat
```
- **Opens new terminal windows**
- **Good for debugging**
- **Traditional approach**

## 📋 **Requirements (One-time setup):**
- **Python 3.8+** from [python.org](https://www.python.org/downloads/)
- **Node.js 16.0+** from [nodejs.org](https://nodejs.org/)

## 🎯 **How to Use:**

### **In Command Prompt (cmd.exe):**
1. Open **Command Prompt**
2. Navigate to project folder: `cd K:\Master\phish_guard`
3. Run: `.\start_simple.bat` (recommended)

### **In PowerShell:**
1. Open **PowerShell**
2. Navigate to project folder: `cd K:\Master\phish_guard`
3. Run: `.\start.ps1`

### **Right-click Method (Anywhere):**
1. **Right-click** on any `.bat` file
2. **Select** "Run as administrator"
3. **Wait** for completion
4. **Done!** App opens automatically

## 🌐 **Access:**
- **App**: http://localhost:3000
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

## 🏆 **WORA Certified:**
**Write Once, Run Anywhere** - Works on ALL Windows systems!

**Your teammate can now run PhishGuard with ZERO setup errors!** 🚀

## 🔧 **What Each Script Does:**
1. **Checks** Python and Node.js
2. **Installs** all dependencies automatically
3. **Starts** backend service (port 8000)
4. **Starts** frontend service (port 3000)
5. **Opens** browser automatically
6. **Ready** to use!

## 🆕 **NEW: Single Terminal Mode**
- **`start_simple.bat`** - Everything runs in ONE terminal
- **No new windows** - keeps it simple
- **Background processes** - services keep running
- **Easy to stop** - just close the terminal

## ❌ **Troubleshooting:**
- **"Python not found"**: Install Python from python.org
- **"Node.js not found"**: Install Node.js from nodejs.org
- **Port conflicts**: Script automatically stops existing services
- **Permission errors**: Run as administrator
- **Services not starting**: Check if ports 8000/3000 are free
