# PhishGuard Project Setup Guide

Complete setup instructions for the PhishGuard AI-Powered Email Security Platform.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **Network**: Internet connection for package installation

### Required Software

#### 1. Python 3.11+
```bash
# Check Python version
python --version
# or
python3 --version

# Install Python 3.11+ if not available
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# macOS (using Homebrew)
brew install python@3.11

# Windows
# Download from https://www.python.org/downloads/
```

#### 2. Node.js 18.0+
```bash
# Check Node.js version
node --version
npm --version

# Install Node.js 18+
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS (using Homebrew)
brew install node@18

# Windows
# Download from https://nodejs.org/en/download/
```

#### 3. PostgreSQL 15+ (Optional - SQLite is default)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql@15

# Windows
# Download from https://www.postgresql.org/download/windows/
```

#### 4. Redis (Optional)
```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis

# Windows
# Download from https://github.com/microsoftarchive/redis/releases
```

#### 5. Docker & Docker Compose (Recommended)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# macOS
brew install docker docker-compose

# Windows
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
```

#### 6. Git
```bash
# Ubuntu/Debian
sudo apt install git

# macOS
brew install git

# Windows
# Download from https://git-scm.com/download/win
```

## 🚀 Quick Start (Docker - Recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/phishguard.git
cd phishguard
```

### 2. Start with Docker Compose
```bash
# Start all services (backend, frontend, database, redis)
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Database Admin**: http://localhost:5050 (pgAdmin)

### 4. Demo Login
- **Email**: `admin@phishguard.com`
- **Password**: `demo123`

## 🛠️ Manual Development Setup

### Backend Setup

#### 1. Navigate to Backend Directory
```bash
cd backend
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install minimal dependencies for demo
pip install -r requirements_demo.txt
```

#### 4. Environment Configuration
```bash
# Create environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Example .env file:**
```env
# Application
ENVIRONMENT=development
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=true

# Database (SQLite for development)
DATABASE_URL=sqlite:///./phishguard.db
DATABASE_URL_ASYNC=sqlite+aiosqlite:///./phishguard.db

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
REDIS_ENABLED=false

# Security
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
VIRUSTOTAL_API_KEY=your-virustotal-api-key
```

#### 5. Database Setup
```bash
# For SQLite (default - no setup needed)
# Database will be created automatically

# For PostgreSQL (if using)
createdb phishguard
```

#### 6. Run Database Migrations
```bash
# Install alembic if not already installed
pip install alembic

# Initialize database
alembic upgrade head
```

#### 7. Run Backend Server
```bash
# Development server
python run_demo.py

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Production server
python run_production.py
```

### Frontend Setup

#### 1. Navigate to Frontend Directory
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Environment Configuration
```bash
# Create environment file
cp .env.example .env.local

# Edit .env.local with your settings
nano .env.local
```

**Example .env.local file:**
```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8001/api

# Application settings
NEXT_PUBLIC_APP_NAME=PhishGuard
NEXT_PUBLIC_APP_VERSION=1.0.0

# Features
NEXT_PUBLIC_WEBSOCKET_ENABLED=true
NEXT_PUBLIC_ANALYTICS_ENABLED=true
```

#### 4. Run Frontend Development Server
```bash
npm run dev
```

#### 5. Build for Production
```bash
npm run build
npm run start
```

## 🐳 Docker Setup (Detailed)

### 1. Backend Docker Setup
```bash
cd backend

# Build backend image
docker build -t phishguard-backend .

# Run backend container
docker run -d \
  --name phishguard-backend \
  -p 8001:8001 \
  -e DATABASE_URL=sqlite:///./phishguard.db \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/data:/app/data \
  phishguard-backend
```

### 2. Frontend Docker Setup
```bash
cd frontend

# Build frontend image
docker build -t phishguard-frontend .

# Run frontend container
docker run -d \
  --name phishguard-frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000/api \
  phishguard-frontend
```

### 3. Full Stack Docker Compose
```bash
# From project root
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build --force-recreate
```

## 🗄️ Database Setup Options

### Option 1: SQLite (Default - No Setup)
```bash
# SQLite database is created automatically
# No additional setup required
```

### Option 2: PostgreSQL
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE phishguard;
CREATE USER phishguard WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE phishguard TO phishguard;
\q

# Update backend .env
DATABASE_URL=postgresql://phishguard:password@localhost:5432/phishguard
DATABASE_URL_ASYNC=postgresql+asyncpg://phishguard:password@localhost:5432/phishguard
```

### Option 3: PostgreSQL with Docker
```bash
# Run PostgreSQL in Docker
docker run -d \
  --name phishguard-postgres \
  -e POSTGRES_DB=phishguard \
  -e POSTGRES_USER=phishguard \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15-alpine
```

## 🧪 Testing Setup

### Backend Testing
```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

### Frontend Testing
```bash
cd frontend

# Install test dependencies (already in package.json)
npm install

# Run unit tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run end-to-end tests
npm run test:e2e
```

## 🔧 Development Tools Setup

### Code Quality Tools
```bash
# Backend
cd backend
pip install black isort flake8 mypy

# Format code
black app/
isort app/

# Lint code
flake8 app/
mypy app/

# Frontend
cd frontend
npm install

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Type check
npm run type-check
```

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files
```

## 🔑 API Keys & External Services

### VirusTotal API Key
```bash
# Get free API key from https://www.virustotal.com/gui/join-us
# Add to backend .env
VIRUSTOTAL_API_KEY=your-api-key-here
```

### Optional Services
- **Slack Integration**: Get webhook URL from Slack
- **Discord Integration**: Get webhook URL from Discord
- **Email SMTP**: Configure SMTP settings for notifications

## 🚀 Production Deployment

### Environment Preparation
```bash
# Create production environment file
cp .env.example .env.production

# Edit with production settings
nano .env.production
```

**Production .env example:**
```env
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-production-secret-key-32-chars-minimum
DATABASE_URL=postgresql://user:pass@db:5432/phishguard
REDIS_URL=redis://redis:6379/0
ALLOWED_ORIGINS=https://your-domain.com
```

### Docker Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Run production stack
docker-compose -f docker-compose.prod.yml up -d

# Set up SSL/TLS (with Let's Encrypt)
docker run -d \
  --name nginx-proxy \
  -p 80:80 -p 443:443 \
  -v /var/run/docker.sock:/tmp/docker.sock:ro \
  jwilder/nginx-proxy

# Set up automatic SSL
docker run -d \
  --name nginx-proxy-letsencrypt \
  --volumes-from nginx-proxy \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  jrcs/letsencrypt-nginx-proxy-companion
```

### Manual Production Setup
```bash
# Backend production setup
cd backend
pip install -r requirements.txt
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

# Frontend production setup
cd frontend
npm run build
npm start

# Or with PM2
npm install -g pm2
pm2 start ecosystem.config.js
```

## 📊 System Monitoring

### Health Checks
```bash
# Backend health check
curl http://localhost:8001/health

# Frontend health check
curl http://localhost:3000/api/health
```

### Log Monitoring
```bash
# Backend logs
tail -f backend/logs/app.log

# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# System logs
journalctl -u phishguard-backend -f
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 8001
lsof -i :8001

# Kill process
kill -9 $(lsof -t -i:8001)

# Or use different port
uvicorn app.main:app --port 8002
```

#### 2. Database Connection Issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
psql -U phishguard -d phishguard -h localhost

# Reset database
dropdb phishguard
createdb phishguard
```

#### 3. Permission Issues
```bash
# Fix file permissions
chmod +x scripts/*.sh

# Fix Docker permissions
sudo chown -R $USER:$USER .
sudo chmod -R 755 .
```

#### 4. Python Package Issues
```bash
# Clear pip cache
pip cache purge

# Reinstall packages
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

#### 5. Node.js Package Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Debug Mode
```bash
# Backend debug mode
export DEBUG=true
python run_demo.py

# Frontend debug mode
export NODE_ENV=development
npm run dev

# Docker debug mode
docker-compose -f docker-compose.debug.yml up
```

## 📚 Additional Resources

### Documentation
- **API Documentation**: http://localhost:8001/docs
- **Frontend Components**: http://localhost:3000/storybook
- **Database Schema**: Check `backend/models/` directory

### Useful Commands
```bash
# Database management
alembic revision --autogenerate -m "Description"
alembic upgrade head
alembic downgrade -1

# Docker management
docker system prune -a
docker volume prune
docker network prune

# Process management
pm2 list
pm2 restart phishguard
pm2 logs phishguard

# System monitoring
htop
df -h
free -h
```

## 🔒 Security Considerations

### Development Security
- Never commit API keys or secrets
- Use environment variables for sensitive data
- Regular dependency updates
- Enable HTTPS in production

### Production Security
- Use strong passwords and API keys
- Enable firewall rules
- Regular security updates
- Monitor access logs
- Implement proper backup strategies

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Check GitHub issues for similar problems
4. Create a new issue with detailed error information

## 🎯 Next Steps

After successful setup:
1. Configure external API keys (VirusTotal, etc.)
2. Set up monitoring and alerting
3. Configure backup strategies
4. Review security settings
5. Train your team on the platform
6. Set up CI/CD pipeline for deployments

---

**Happy PhishGuarding! 🛡️** 