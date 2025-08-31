#!/usr/bin/env python3
"""
PhishGuard Application Startup Script
Starts both frontend and backend services and makes the application ready
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path
import requests
import webbrowser
import platform

class PhishGuardStarter:
    """Manages the startup of PhishGuard application"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.backend_process = None
        self.frontend_process = None
        self.is_running = False
        
    def print_banner(self):
        """Print the PhishGuard startup banner"""
        print("=" * 70)
        print("🚀 PHISHGUARD - AI-Powered Email Security Platform")
        print("=" * 70)
        print("🔒 Backend: FastAPI + ML Models")
        print("🎨 Frontend: Next.js + React")
        print("🤖 AI: Spam Detection & Threat Analysis")
        print("=" * 70)
        
    def check_requirements(self):
        """Check if all requirements are met"""
        print("🔍 Checking system requirements...")
        
        # Check Python
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            print("❌ Python 3.8+ required. Current version:", sys.version)
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check Node.js
        try:
            node_result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if node_result.returncode == 0:
                print(f"✅ Node.js {node_result.stdout.strip()}")
            else:
                print("❌ Node.js not found")
                return False
        except FileNotFoundError:
            print("❌ Node.js not found")
            return False
        
        # Check npm
        try:
            npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if npm_result.returncode == 0:
                print(f"✅ npm {npm_result.stdout.strip()}")
            else:
                print("❌ npm not found")
                return False
        except FileNotFoundError:
            print("❌ npm not found")
            return False
        
        # Check directories
        if not self.backend_dir.exists():
            print("❌ Backend directory not found")
            return False
        print("✅ Backend directory found")
        
        if not self.frontend_dir.exists():
            print("❌ Frontend directory not found")
            return False
        print("✅ Frontend directory found")
        
        return True
    
    def install_dependencies(self):
        """Install dependencies for both backend and frontend"""
        print("\n📦 Installing dependencies...")
        
        # Install backend dependencies
        print("🔧 Installing backend dependencies...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 
                          str(self.backend_dir / 'requirements.txt')], 
                         cwd=self.backend_dir, check=True)
            print("✅ Backend dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install backend dependencies: {e}")
            return False
        
        # Install frontend dependencies
        print("🔧 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], cwd=self.frontend_dir, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return False
        
        return True
    
    def start_backend(self):
        """Start the backend service"""
        print("🚀 Starting backend service...")
        
        try:
            # Change to backend directory and start the service
            self.backend_process = subprocess.Popen(
                [sys.executable, '-m', 'uvicorn', 'app.main:app', 
                 '--reload', '--host', '0.0.0.0', '--port', '8000'],
                cwd=self.backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit for the service to start
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ Backend service started on port 8000")
                return True
            else:
                print("❌ Backend service failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the frontend service"""
        print("🎨 Starting frontend service...")
        
        try:
            # Change to frontend directory and start the service
            self.frontend_process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=self.frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit for the service to start
            time.sleep(5)
            
            if self.frontend_process.poll() is None:
                print("✅ Frontend service started on port 3000")
                return True
            else:
                print("❌ Frontend service failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
    
    def wait_for_services(self):
        """Wait for services to be ready"""
        print("\n⏳ Waiting for services to be ready...")
        
        backend_ready = False
        frontend_ready = False
        
        for i in range(30):  # Wait up to 30 seconds
            if not backend_ready:
                try:
                    response = requests.get('http://localhost:8000/docs', timeout=2)
                    if response.status_code == 200:
                        backend_ready = True
                        print("✅ Backend service is ready")
                except:
                    pass
            
            if not frontend_ready:
                try:
                    response = requests.get('http://localhost:3000', timeout=2)
                    if response.status_code == 200:
                        frontend_ready = True
                        print("✅ Frontend service is ready")
                except:
                    pass
            
            if backend_ready and frontend_ready:
                break
                
            time.sleep(1)
            print(f"   Waiting... ({i+1}/30)")
        
        return backend_ready and frontend_ready
    
    def test_ml_functionality(self):
        """Test the ML functionality"""
        print("\n🤖 Testing ML functionality...")
        
        try:
            # Test the ML model info endpoint
            response = requests.get('http://localhost:8000/api/v1/threats/ml-model-info', timeout=5)
            if response.status_code == 403:  # Expected for unauthenticated requests
                print("✅ ML API endpoints are working (authentication required)")
            else:
                print(f"⚠️ ML API response: {response.status_code}")
        except Exception as e:
            print(f"⚠️ ML API test: {e}")
    
    def open_application(self):
        """Open the application in the default browser"""
        print("\n🌐 Opening PhishGuard application...")
        
        try:
            # Open frontend
            webbrowser.open('http://localhost:3000')
            print("✅ Frontend opened in browser")
            
            # Open backend API docs
            webbrowser.open('http://localhost:8000/docs')
            print("✅ API documentation opened in browser")
            
        except Exception as e:
            print(f"⚠️ Could not open browser automatically: {e}")
            print("💡 Please manually open:")
            print("   Frontend: http://localhost:3000")
            print("   API Docs: http://localhost:8000/docs")
    
    def show_status(self):
        """Show the current status of services"""
        print("\n" + "=" * 70)
        print("📊 PHISHGUARD STATUS")
        print("=" * 70)
        
        # Check backend
        try:
            response = requests.get('http://localhost:8000/docs', timeout=2)
            if response.status_code == 200:
                print("🔒 Backend: ✅ RUNNING (http://localhost:8000)")
            else:
                print("🔒 Backend: ❌ NOT RESPONDING")
        except:
            print("🔒 Backend: ❌ NOT RESPONDING")
        
        # Check frontend
        try:
            response = requests.get('http://localhost:3000', timeout=2)
            if response.status_code == 200:
                print("🎨 Frontend: ✅ RUNNING (http://localhost:3000)")
            else:
                print("🎨 Frontend: ❌ NOT RESPONDING")
        except:
            print("🎨 Frontend: ❌ NOT RESPONDING")
        
        print("\n🎯 Your PhishGuard application is ready!")
        print("🔍 Access your application at: http://localhost:3000")
        print("📚 API documentation at: http://localhost:8000/docs")
        print("\n💡 Press Ctrl+C to stop all services")
        print("=" * 70)
    
    def cleanup(self):
        """Clean up processes on exit"""
        print("\n🛑 Shutting down PhishGuard services...")
        
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend service stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print("✅ Frontend service stopped")
        
        self.is_running = False
    
    def run(self):
        """Main run method"""
        try:
            self.print_banner()
            
            # Check requirements
            if not self.check_requirements():
                print("❌ System requirements not met. Please fix the issues above.")
                return False
            
            # Install dependencies
            if not self.install_dependencies():
                print("❌ Failed to install dependencies.")
                return False
            
            # Start services
            if not self.start_backend():
                print("❌ Failed to start backend service.")
                return False
            
            if not self.start_frontend():
                print("❌ Failed to start frontend service.")
                return False
            
            # Wait for services to be ready
            if not self.wait_for_services():
                print("❌ Services failed to start properly.")
                return False
            
            # Test ML functionality
            self.test_ml_functionality()
            
            # Open application
            self.open_application()
            
            # Show status
            self.show_status()
            
            # Keep running
            self.is_running = True
            
            # Set up signal handlers for graceful shutdown
            def signal_handler(signum, frame):
                self.cleanup()
                sys.exit(0)
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            # Keep the script running
            while self.is_running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.cleanup()
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.cleanup()
            return False
        
        return True

def main():
    """Main entry point"""
    starter = PhishGuardStarter()
    success = starter.run()
    
    if success:
        print("🎉 PhishGuard started successfully!")
    else:
        print("❌ Failed to start PhishGuard")
        sys.exit(1)

if __name__ == "__main__":
    main()
