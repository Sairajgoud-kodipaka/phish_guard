# PhishGuard Backend

**AI-Powered Email Security Platform - Backend API**

A comprehensive FastAPI-based backend service for email threat detection and analysis.

## 🚀 Features

- **Advanced Threat Detection**: AI/ML-powered phishing and malware detection
- **Real-time Analysis**: Fast email processing with <2 second analysis time
- **RESTful API**: Comprehensive REST API with automatic documentation
- **Authentication & Authorization**: JWT-based auth with role-based access control
- **Database Integration**: PostgreSQL with async SQLAlchemy
- **Caching Layer**: Redis for performance optimization
- **Security Hardened**: Enterprise-grade security features
- **Monitoring Ready**: Structured logging and health checks
- **Scalable Architecture**: Microservices-ready design

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 15+ with async SQLAlchemy
- **Cache/Queue**: Redis 7+
- **Authentication**: JWT with python-jose
- **ML/AI**: scikit-learn, spaCy, NLTK
- **Validation**: Pydantic v2
- **Testing**: pytest with async support
- **Logging**: structlog for structured logging
- **Deployment**: Docker & Docker Compose

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (recommended)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone and navigate to backend**:
```bash
cd backend
```

2. **Start all services**:
```bash
docker-compose up --build
```

3. **Access the API**:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- pgAdmin: http://localhost:5050 (admin@phishguard.com / admin)
- Redis Commander: http://localhost:8081

### Manual Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up PostgreSQL database**:
```sql
CREATE DATABASE phishguard;
CREATE USER phishguard WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE phishguard TO phishguard;
```

3. **Start Redis**:
```bash
redis-server
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the application**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

### Authentication

**Login**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@phishguard.com&password=demo123"
```

**Get Current User**:
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Dashboard

**Get Statistics**:
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/stats" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Threat Timeline**:
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/threat-timeline" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Interactive Documentation

Visit http://localhost:8000/docs for Swagger UI with interactive API documentation.

## 🗃️ Database Schema

### Core Models

- **Organization**: Multi-tenant organization management
- **User**: User accounts with role-based permissions
- **Email**: Email storage and metadata
- **Threat**: Detailed threat analysis and tracking

### Key Features

- **Multi-tenancy**: Organization-based data isolation
- **Audit Trail**: Complete action logging
- **Flexible Permissions**: Role and permission-based access
- **Threat Intelligence**: MITRE ATT&CK framework integration

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt with salt rounds
- **Rate Limiting**: Request rate limiting per IP/user
- **Security Headers**: Comprehensive security headers
- **Input Validation**: Pydantic-based request validation
- **SQL Injection Protection**: SQLAlchemy ORM protection
- **CORS Configuration**: Configurable CORS policies

## 🧪 Testing

### Run Tests
```bash
pytest
```

### Test Coverage
```bash
pytest --cov=app --cov-report=html
```

### Load Testing
```bash
# Install artillery for load testing
npm install -g artillery

# Run load tests
artillery run tests/load/api-load-test.yml
```

## 📊 Monitoring & Logging

### Structured Logging

The application uses `structlog` for structured, searchable logs:

```python
logger.info("Email processed", 
           email_id=email.id, 
           threat_level=email.threat_level,
           processing_time=duration)
```

### Health Checks

- **API Health**: `GET /health`
- **Database Health**: `GET /api/v1/dashboard/system-health`
- **Service Dependencies**: Automated dependency checks

### Metrics

Key performance indicators:
- Email processing time
- Threat detection accuracy
- API response times
- Database query performance

## 🔧 Configuration

### Environment Variables

Create `.env` file with:

```env
# Application
ENVIRONMENT=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/phishguard
DATABASE_URL_ASYNC=postgresql+asyncpg://user:pass@localhost:5432/phishguard

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
ALLOWED_ORIGINS=http://localhost:3000
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
VIRUSTOTAL_API_KEY=your-api-key
```

### Configuration Classes

- `DevelopmentConfig`: Development settings
- `ProductionConfig`: Production-optimized settings
- `TestingConfig`: Testing environment settings

## 🐳 Docker Deployment

### Development
```bash
docker-compose up --build
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Services Included

- **Backend API**: FastAPI application
- **PostgreSQL**: Primary database
- **Redis**: Caching and task queue
- **pgAdmin**: Database administration
- **Redis Commander**: Redis management

## 🤖 ML/AI Components

### Email Analysis Pipeline

1. **Content Extraction**: Parse email headers, body, attachments
2. **Feature Engineering**: Extract linguistic and metadata features
3. **NLP Analysis**: Sentiment, urgency, and social engineering detection
4. **URL Reputation**: Check URLs against threat databases
5. **Ensemble Scoring**: Combine multiple models for final decision

### Models Included

- **Phishing Detection**: Email content analysis
- **Spam Classification**: Bayesian and ML-based filtering
- **Malware Detection**: Attachment and URL scanning
- **Anomaly Detection**: Behavioral analysis

## 📈 Performance Optimization

### Database Optimization

- Connection pooling
- Query optimization with indexes
- Async database operations
- Read replicas for scaling

### Caching Strategy

- Redis for API response caching
- Model prediction caching
- Session data caching
- Background task queuing

### API Optimization

- Response compression
- Request/response validation
- Async request handling
- Database connection pooling

## 🔄 Development Workflow

### Code Quality

```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/
mypy app/

# Run tests
pytest --cov=app
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## 🚀 Production Deployment

### Environment Preparation

1. **Secure Secrets**: Use proper secret management
2. **Database Migrations**: Run with Alembic
3. **SSL/TLS**: Configure HTTPS certificates
4. **Load Balancing**: Set up reverse proxy
5. **Monitoring**: Configure application monitoring

### Scaling Considerations

- **Horizontal Scaling**: Multiple API instances
- **Database Scaling**: Read replicas and sharding
- **Caching Layer**: Redis cluster
- **Background Tasks**: Celery workers

## 🆘 Troubleshooting

### Common Issues

**Database Connection Error**:
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Check connection string
psql postgresql://phishguard:password@localhost:5432/phishguard
```

**Redis Connection Error**:
```bash
# Check Redis is running
redis-cli ping

# Check Redis connection
redis-cli -h localhost -p 6379
```

**Import Errors**:
```bash
# Check Python path
export PYTHONPATH=/path/to/backend
```

### Logs and Debugging

- **Application Logs**: Check structured logs in JSON format
- **Database Logs**: PostgreSQL query logs
- **API Logs**: Request/response logging with correlation IDs

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

- **Documentation**: `/docs` endpoint
- **Issues**: GitHub Issues
- **Email**: support@phishguard.com

---

**PhishGuard Backend** - Enterprise-grade email security powered by AI 🛡️ 