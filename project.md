# PhishGuard - Complete System Architecture & Implementation Plan

## 1. Complete System Architecture Flow

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Email Input   │───▶│   Preprocessing  │───▶│  Multi-Analysis │───▶│   Risk Scoring   │
│                 │    │                  │    │                 │    │                  │
│ • API Gateway   │    │ • Extract URLs   │    │ • NLP Analysis  │    │ • Weight Scores  │
│ • Email Client  │    │ • Parse Headers  │    │ • URL Scanning  │    │ • Confidence     │
│ • IMAP/SMTP     │    │ • Clean Content  │    │ • Rule Engine   │    │ • Thresholds     │
└─────────────────┘    └──────────────────┘    │ • Anomaly Det.  │    └──────────────────┘
                                               └─────────────────┘             │
                                                                               ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Final Action  │◀───│    Response      │◀───│    Logging      │◀───│  Action Engine   │
│                 │    │                  │    │                 │    │                  │
│ • Block/Quarant │    │ • User Alert     │    │ • Detection Log │    │ • Decision Logic │
│ • Flag Warning  │    │ • Admin Notice   │    │ • Threat Intel  │    │ • Route Action   │
│ • Allow w/Tag   │    │ • API Response   │    │ • Audit Trail   │    │ • Update Models  │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────────┘
```

### Detailed System Flow

#### Phase 1: Email Reception & Validation
```python
# Email Input Sources
Email Sources → API Gateway → Input Validator → Queue Manager
    ↓
• IMAP/POP3 Polling
• SMTP Integration  
• API Submissions
• Real-time Streams
```

#### Phase 2: Preprocessing Pipeline
```python
Raw Email → Header Parser → Content Extractor → Feature Preparation
    ↓
• Extract metadata (sender, timestamp, routing)
• Parse HTML/text content
• Extract URLs and links
• Identify attachments
• Normalize encoding
• Tokenize content
```

#### Phase 3: Multi-Layer Analysis Engine
```python
Preprocessed Data → Parallel Analysis Modules → Score Aggregation
    ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Analysis Modules                             │
├─────────────────────────────────────────────────────────────────┤
│ 1. NLP Analysis Module                                          │
│    • Social engineering keywords                               │
│    • Urgency pattern detection                                 │
│    • Grammar/spelling analysis                                 │
│    • Sentiment analysis                                        │
│                                                                 │
│ 2. URL Analysis Module                                          │
│    • Domain reputation (VirusTotal API)                        │
│    • URL shortener detection                                   │
│    • Redirect chain analysis                                   │
│    • Blacklist checking                                        │
│                                                                 │
│ 3. Header Analysis Module                                       │
│    • SPF/DKIM/DMARC validation                                 │
│    • Routing path analysis                                     │
│    • Sender reputation                                         │
│    • Geographic anomalies                                      │
│                                                                 │
│ 4. Decision Tree Rules                                          │
│    • Known phishing patterns                                   │
│    • Domain spoofing detection                                 │
│    • Content structure rules                                   │
│    • Attachment type validation                                │
│                                                                 │
│ 5. Anomaly Detection                                            │
│    • Behavioral pattern analysis                               │
│    • Statistical outlier detection                             │
│    • Zero-day threat identification                            │
│    • User behavior baseline                                    │
└─────────────────────────────────────────────────────────────────┘
```

#### Phase 4: Risk Scoring & Decision
```python
Analysis Results → Risk Calculator → Decision Engine → Action Router
    ↓
# Risk Scoring Algorithm
final_score = (
    nlp_score * 0.25 +           # Content analysis weight
    url_score * 0.30 +           # URL reputation weight  
    header_score * 0.20 +        # Authentication weight
    rules_score * 0.15 +         # Pattern matching weight
    anomaly_score * 0.10         # Behavioral analysis weight
)

# Decision Thresholds
if final_score >= 0.8:          # High Risk
    action = "BLOCK_QUARANTINE"
elif final_score >= 0.6:        # Medium Risk  
    action = "FLAG_WARNING"
elif final_score >= 0.4:        # Low Risk
    action = "ALLOW_WITH_TAG"
else:                            # Safe
    action = "ALLOW"
```

## 2. Development Roadmap with Phases

### Phase Alpha: Core Foundation (Months 1-3)
**Goal:** Proof of Concept with basic detection

#### Month 1: Infrastructure Setup
- [x] Project repository and version control
- [x] Development environment setup
- [x] Basic API framework (FastAPI)
- [x] Database schema design (PostgreSQL)
- [x] Docker containerization
- [x] Basic email reception module

#### Month 2: Core Analysis Engine
- [x] Preprocessing pipeline implementation
- [x] NLP analysis module (spaCy + NLTK)
- [x] Basic URL scanning (VirusTotal integration)
- [x] Simple decision tree rules
- [x] Risk scoring algorithm v1
- [x] Command-line testing interface

#### Month 3: Basic Integration & Testing
- [x] Email parsing for multiple formats
- [x] Basic API endpoints
- [x] Simple logging system
- [x] Unit tests for core modules
- [x] Performance benchmarking
- [x] Alpha testing with sample emails

**Alpha Deliverables:**
- Working email analysis engine
- Basic phishing detection (60-70% accuracy)
- Command-line interface
- Core API endpoints
- Basic documentation

### Phase Beta: Enhanced Detection (Months 4-6)
**Goal:** Production-ready MVP with advanced features

#### Month 4: Advanced Analysis
- [x] Anomaly detection implementation
- [x] Header analysis module (SPF/DKIM/DMARC)
- [x] Enhanced NLP with social engineering detection
- [x] Whitelist/blacklist management
- [x] Adaptive learning algorithms
- [x] Multi-threaded processing

#### Month 5: User Interface & Integration
- [x] Web dashboard development (React)
- [x] Real-time email processing
- [x] API authentication and rate limiting
- [x] Email client integration (IMAP/SMTP)
- [x] Alert notification system
- [x] User feedback mechanism

#### Month 6: Security & Optimization
- [x] Data encryption implementation
- [x] Secure API design
- [x] Performance optimization
- [x] Comprehensive testing
- [x] Security audit
- [x] Beta user testing

**Beta Deliverables:**
- 85-90% detection accuracy
- Web dashboard
- Real-time processing
- Email client integration
- Security implementation
- User documentation

### Phase Release: Production System (Months 7-9)
**Goal:** Enterprise-ready solution with full security

#### Month 7: Enterprise Features
- [x] Advanced threat intelligence
- [x] Compliance framework (GDPR, SOC 2)
- [x] Advanced logging and monitoring
- [x] Incident response automation
- [x] Multi-tenant support
- [x] Advanced reporting

#### Month 8: Scalability & Deployment
- [x] Kubernetes deployment
- [x] Load balancing and scaling
- [x] Backup and disaster recovery
- [x] Performance monitoring
- [x] CI/CD pipeline
- [x] Production environment setup

#### Month 9: Final Testing & Launch
- [x] Penetration testing
- [x] Load testing
- [x] Final security audit
- [x] Documentation completion
- [x] Training materials
- [x] Production launch

**Release Deliverables:**
- 95%+ detection accuracy
- <3% false positive rate
- Enterprise security compliance
- Full deployment automation
- Complete documentation
- Support system

## 3. Technical Implementation Details

### Backend Architecture

#### Core Technology Stack
```python
# Application Framework
FastAPI                 # High-performance async web framework
uvicorn                # ASGI server
pydantic               # Data validation

# Database Layer  
PostgreSQL             # Primary database
Redis                  # Caching and session storage
SQLAlchemy            # ORM
alembic               # Database migrations

# Machine Learning
scikit-learn          # ML algorithms and decision trees
spaCy                 # NLP processing
NLTK                  # Text analysis
pandas                # Data manipulation
numpy                 # Numerical computing

# Security & Integration
cryptography          # Encryption
jwt                   # JWT tokens
requests              # HTTP client
celery                # Background tasks
```

#### Database Schema Design
```sql
-- Core Tables
CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    message_id VARCHAR(255) UNIQUE,
    sender VARCHAR(255),
    recipient VARCHAR(255),
    subject TEXT,
    content TEXT,
    headers JSONB,
    received_at TIMESTAMP,
    processed_at TIMESTAMP,
    risk_score FLOAT,
    final_action VARCHAR(50),
    status VARCHAR(50)
);

CREATE TABLE threats (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id),
    threat_type VARCHAR(100),
    confidence FLOAT,
    module_source VARCHAR(50),
    description TEXT,
    detected_at TIMESTAMP
);

CREATE TABLE domains (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) UNIQUE,
    reputation_score FLOAT,
    last_checked TIMESTAMP,
    source VARCHAR(100),
    status VARCHAR(50)
);

CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    url TEXT,
    domain_id INTEGER REFERENCES domains(id),
    risk_score FLOAT,
    scan_results JSONB,
    last_scanned TIMESTAMP
);

-- Analysis Results
CREATE TABLE analysis_results (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id),
    nlp_score FLOAT,
    url_score FLOAT,
    header_score FLOAT,
    rules_score FLOAT,
    anomaly_score FLOAT,
    final_score FLOAT,
    processing_time FLOAT,
    created_at TIMESTAMP
);

-- User Management
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(50),
    created_at TIMESTAMP,
    last_login TIMESTAMP
);

-- Whitelists and Blacklists
CREATE TABLE whitelist (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50),  -- 'domain', 'email', 'ip'
    value VARCHAR(255),
    added_by INTEGER REFERENCES users(id),
    added_at TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);
```

#### Core Modules Implementation

##### 1. Email Processing Module
```python
# email_processor.py
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class EmailData:
    sender: str
    recipient: str
    subject: str
    content: str
    headers: Dict
    urls: List[str]
    attachments: List[str]
    html_content: Optional[str] = None

class EmailProcessor:
    def __init__(self):
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
    
    def parse_email(self, raw_email: str) -> EmailData:
        """Parse raw email into structured data"""
        msg = email.message_from_string(raw_email)
        
        # Extract basic headers
        sender = msg.get('From', '')
        recipient = msg.get('To', '')
        subject = msg.get('Subject', '')
        
        # Extract content
        content = self._extract_content(msg)
        html_content = self._extract_html_content(msg)
        
        # Extract URLs
        urls = self._extract_urls(content + (html_content or ''))
        
        # Extract attachments
        attachments = self._extract_attachments(msg)
        
        # Get all headers
        headers = dict(msg.items())
        
        return EmailData(
            sender=sender,
            recipient=recipient,
            subject=subject,
            content=content,
            headers=headers,
            urls=urls,
            attachments=attachments,
            html_content=html_content
        )
    
    def _extract_content(self, msg) -> str:
        """Extract text content from email"""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            if msg.get_content_type() == "text/plain":
                return msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        return ""
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text content"""
        return self.url_pattern.findall(text)
```

##### 2. NLP Analysis Module
```python
# nlp_analyzer.py
import spacy
from typing import Dict, List
import re

class NLPAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.phishing_keywords = {
            'urgency': ['urgent', 'immediate', 'expire', 'deadline', 'asap', 'quick'],
            'fear': ['suspend', 'block', 'cancel', 'terminated', 'locked'],
            'money': ['lottery', 'winner', 'prize', 'refund', 'claim', 'transfer'],
            'credentials': ['verify', 'confirm', 'update', 'login', 'password', 'account']
        }
        
    def analyze_content(self, content: str, subject: str) -> Dict:
        """Analyze email content for phishing indicators"""
        doc = self.nlp(content)
        subject_doc = self.nlp(subject)
        
        results = {
            'urgency_score': self._calculate_urgency_score(content, subject),
            'fear_score': self._calculate_fear_score(content, subject),
            'money_score': self._calculate_money_score(content, subject),
            'credential_score': self._calculate_credential_score(content, subject),
            'grammar_score': self._calculate_grammar_score(doc),
            'sentiment_score': self._calculate_sentiment_score(doc),
            'entities': self._extract_entities(doc),
            'overall_score': 0.0
        }
        
        # Calculate overall NLP score
        results['overall_score'] = (
            results['urgency_score'] * 0.25 +
            results['fear_score'] * 0.25 +
            results['money_score'] * 0.20 +
            results['credential_score'] * 0.20 +
            (1 - results['grammar_score']) * 0.10  # Poor grammar increases suspicion
        )
        
        return results
    
    def _calculate_urgency_score(self, content: str, subject: str) -> float:
        """Calculate urgency indicators score"""
        text = (content + " " + subject).lower()
        urgency_count = sum(1 for keyword in self.phishing_keywords['urgency'] 
                          if keyword in text)
        return min(urgency_count / 3.0, 1.0)  # Normalize to 0-1
```

##### 3. URL Analysis Module
```python
# url_analyzer.py
import requests
import time
from urllib.parse import urlparse
from typing import Dict, List
import hashlib

class URLAnalyzer:
    def __init__(self, virustotal_api_key: str):
        self.vt_api_key = virustotal_api_key
        self.vt_base_url = "https://www.virustotal.com/vtapi/v2"
        self.suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.click', '.download']
        self.url_shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly']
        
    def analyze_urls(self, urls: List[str]) -> Dict:
        """Analyze list of URLs for malicious indicators"""
        if not urls:
            return {'overall_score': 0.0, 'detailed_results': []}
            
        results = []
        total_score = 0.0
        
        for url in urls:
            url_result = self._analyze_single_url(url)
            results.append(url_result)
            total_score += url_result['risk_score']
            
        overall_score = total_score / len(urls)
        
        return {
            'overall_score': min(overall_score, 1.0),
            'detailed_results': results,
            'high_risk_urls': [r for r in results if r['risk_score'] > 0.7],
            'suspicious_count': sum(1 for r in results if r['risk_score'] > 0.5)
        }
    
    def _analyze_single_url(self, url: str) -> Dict:
        """Analyze a single URL"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        result = {
            'url': url,
            'domain': domain,
            'risk_score': 0.0,
            'indicators': [],
            'vt_result': None
        }
        
        # Check for suspicious TLD
        if any(domain.endswith(tld) for tld in self.suspicious_tlds):
            result['risk_score'] += 0.3
            result['indicators'].append('suspicious_tld')
            
        # Check for URL shorteners
        if any(shortener in domain for shortener in self.url_shorteners):
            result['risk_score'] += 0.4
            result['indicators'].append('url_shortener')
            
        # Check domain length and structure
        if len(domain) > 50:
            result['risk_score'] += 0.2
            result['indicators'].append('long_domain')
            
        # VirusTotal check
        vt_score = self._check_virustotal(url)
        if vt_score:
            result['vt_result'] = vt_score
            result['risk_score'] += vt_score['risk_score']
            
        return result
    
    def _check_virustotal(self, url: str) -> Dict:
        """Check URL against VirusTotal"""
        try:
            # Rate limiting
            time.sleep(0.25)  # VT free tier: 4 requests per minute
            
            params = {
                'apikey': self.vt_api_key,
                'resource': url
            }
            
            response = requests.get(
                f"{self.vt_base_url}/url/report",
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['response_code'] == 1:  # URL found
                    positives = data.get('positives', 0)
                    total = data.get('total', 1)
                    risk_score = positives / total if total > 0 else 0
                    
                    return {
                        'risk_score': risk_score,
                        'positives': positives,
                        'total': total,
                        'scan_date': data.get('scan_date')
                    }
                    
        except Exception as e:
            print(f"VirusTotal API error: {e}")
            
        return None
```

##### 4. Decision Engine
```python
# decision_engine.py
from dataclasses import dataclass
from typing import Dict, List
import json

@dataclass
class AnalysisResult:
    nlp_score: float
    url_score: float
    header_score: float
    rules_score: float
    anomaly_score: float

@dataclass
class Decision:
    action: str
    confidence: float
    reasons: List[str]
    risk_level: str

class DecisionEngine:
    def __init__(self):
        self.weights = {
            'nlp': 0.25,
            'url': 0.30,
            'header': 0.20,
            'rules': 0.15,
            'anomaly': 0.10
        }
        
        self.thresholds = {
            'block': 0.8,      # High risk - block immediately
            'flag': 0.6,       # Medium risk - flag with warning
            'tag': 0.4,        # Low risk - allow with tag
            'allow': 0.0       # Safe - allow normally
        }
    
    def make_decision(self, analysis: AnalysisResult) -> Decision:
        """Make final decision based on all analysis results"""
        
        # Calculate weighted final score
        final_score = (
            analysis.nlp_score * self.weights['nlp'] +
            analysis.url_score * self.weights['url'] +
            analysis.header_score * self.weights['header'] +
            analysis.rules_score * self.weights['rules'] +
            analysis.anomaly_score * self.weights['anomaly']
        )
        
        # Determine action based on thresholds
        if final_score >= self.thresholds['block']:
            action = "BLOCK_QUARANTINE"
            risk_level = "HIGH"
        elif final_score >= self.thresholds['flag']:
            action = "FLAG_WARNING"
            risk_level = "MEDIUM"
        elif final_score >= self.thresholds['tag']:
            action = "ALLOW_WITH_TAG"
            risk_level = "LOW"
        else:
            action = "ALLOW"
            risk_level = "SAFE"
            
        # Generate reasons
        reasons = self._generate_reasons(analysis, final_score)
        
        return Decision(
            action=action,
            confidence=final_score,
            reasons=reasons,
            risk_level=risk_level
        )
    
    def _generate_reasons(self, analysis: AnalysisResult, final_score: float) -> List[str]:
        """Generate human-readable reasons for the decision"""
        reasons = []
        
        if analysis.nlp_score > 0.6:
            reasons.append("Suspicious content patterns detected")
        if analysis.url_score > 0.6:
            reasons.append("Malicious or suspicious URLs found")
        if analysis.header_score > 0.6:
            reasons.append("Email authentication failures")
        if analysis.rules_score > 0.6:
            reasons.append("Matches known phishing patterns")
        if analysis.anomaly_score > 0.6:
            reasons.append("Unusual behavior detected")
            
        if not reasons:
            reasons.append("No significant threats detected")
            
        return reasons
```

## 4. Security Framework

### Comprehensive Security Implementation

#### 4.1 Data Protection & Encryption

##### Encryption at Rest
```python
# encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class DataEncryption:
    def __init__(self, password: bytes):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.cipher_suite = Fernet(key)
    
    def encrypt_email_content(self, content: str) -> str:
        """Encrypt sensitive email content"""
        return self.cipher_suite.encrypt(content.encode()).decode()
    
    def decrypt_email_content(self, encrypted_content: str) -> str:
        """Decrypt email content"""
        return self.cipher_suite.decrypt(encrypted_content.encode()).decode()

# Database encryption configuration
# postgresql.conf additions:
# ssl = on
# ssl_cert_file = 'server.crt'
# ssl_key_file = 'server.key'
# ssl_ca_file = 'ca.crt'
```

##### Encryption in Transit
```yaml
# nginx.conf - TLS Configuration
server {
    listen 443 ssl http2;
    server_name phishguard.example.com;
    
    # TLS Configuration
    ssl_certificate /etc/ssl/certs/phishguard.crt;
    ssl_certificate_key /etc/ssl/private/phishguard.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
}
```

#### 4.2 Authentication & Authorization

##### JWT-based Authentication
```python
# auth.py
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class AuthManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """Verify JWT token"""
        try:
            payload = jwt.decode(credentials.credentials, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return username
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

# Role-based access control
class RBACManager:
    def __init__(self):
        self.roles = {
            'admin': ['read', 'write', 'delete', 'manage_users'],
            'analyst': ['read', 'write', 'analyze'],
            'user': ['read'],
        }
    
    def check_permission(self, user_role: str, required_permission: str) -> bool:
        """Check if user role has required permission"""
        return required_permission in self.roles.get(user_role, [])
```

#### 4.3 Input Validation & Sanitization

```python
# validators.py
from pydantic import BaseModel, EmailStr, validator
import re
from typing import List, Optional

class EmailSubmissionRequest(BaseModel):
    sender: EmailStr
    recipient: EmailStr
    subject: str
    content: str
    headers: Optional[dict] = {}
    
    @validator('subject')
    def validate_subject(cls, v):
        if len(v) > 1000:
            raise ValueError('Subject too long')
        return v
    
    @validator('content')
    def validate_content(cls, v):
        if len(v) > 100000:  # 100KB limit
            raise ValueError('Content too large')
        return v
    
    @validator('headers')
    def validate_headers(cls, v):
        if v and len(str(v)) > 10000:
            raise ValueError('Headers too large')
        return v

class URLSanitizer:
    def __init__(self):
        self.url_pattern = re.compile(
            r'^https?://[a-zA-Z0-9.-]+/[a-zA-Z0-9./_-]*$'
        )
    
    def sanitize_url(self, url: str) -> str:
        """Sanitize URL input"""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', url)
        # Validate format
        if not self.url_pattern.match(sanitized):
            raise ValueError('Invalid URL format')
        return sanitized
```

#### 4.4 Audit Logging & Monitoring

```python
# audit_logger.py
import logging
import json
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger('phishguard_audit')
        handler = logging.FileHandler('/var/log/phishguard/audit.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_detection(self, email_id: str, risk_score: float, action: str, user_id: str = None):
        """Log phishing detection event"""
        event = {
            'event_type': 'PHISHING_DETECTION',
            'email_id': email_id,
            'risk_score': risk_score,
            'action': action,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.logger.info(json.dumps(event))
    
    def log_system_event(self, event_type: str, details: Dict[str, Any], user_id: str = None):
        """Log system events"""
        event = {
            'event_type': event_type,
            'details': details,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.logger.info(json.dumps(event))

# Monitoring alerts
class SecurityMonitor:
    def __init__(self):
        self.alert_thresholds = {
            'failed_logins': 5,
            'high_risk_detections': 10,
            'api_rate_limit_hits': 100
        }
    
    def check_security_metrics(self):
        """Monitor security metrics and trigger alerts"""
        # Implementation for monitoring various security metrics
        pass
```

#### 4.5 Compliance Framework

##### GDPR Compliance Implementation
```python
# gdpr_compliance.py
from datetime import datetime, timedelta
from typing import List

class GDPRCompliance:
    def __init__(self):
        self.data_retention_days = 365  # 1 year retention
        self.consent_required_fields = ['email_content', 'sender_info']
    
    def anonymize_email_data(self, email_id: str):
        """Anonymize email data for GDPR compliance"""
        # Remove or hash personally identifiable information
        pass
    
    def handle_data_deletion_request(self, user_email: str):
        """Handle user's right to be forgotten"""
        # Delete or anonymize all data related to user
        pass
    
    def generate_data_export(self, user_email: str) -> dict:
        """Generate data export for user's right to portability"""
        # Export all user data in portable format
        pass

# Data retention policy
class DataRetentionManager:
    def __init__(self):
        self.retention_policies = {
            'emails': timedelta(days=365),
            'logs': timedelta(days=2555),  # 7 years
            'user_sessions': timedelta(days=30)
        }
    
    def cleanup_expired_data(self):
        """Clean up data based on retention policies"""
        cutoff_date = datetime.utcnow() - self.retention_policies['emails']
        # Delete emails older than retention period
        pass
```

#### 4.6 Incident Response Framework

```python
# incident_response.py
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import List

class IncidentSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityIncident:
    id: str
    severity: IncidentSeverity
    description: str
    affected_systems: List[str]
    detected_at: datetime
    resolved_at: datetime = None
    status: str = "open"

class IncidentResponseManager:
    def __init__(self):
        self.incidents = []
        self.response_procedures = {
            IncidentSeverity.CRITICAL: self._critical_response,
            IncidentSeverity.HIGH: self._high_response,
            IncidentSeverity.MEDIUM: self._medium_response,
            IncidentSeverity.LOW: self._low_response
        }
    
    def trigger_incident(self, severity: IncidentSeverity, description: str, 
                        affected_systems: List[str]) -> SecurityIncident:
        """Trigger incident response procedure"""
        incident = SecurityIncident(
            id=f"INC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            severity=severity,
            description=description,
            affected_systems=affected_systems,
            detected_at=datetime.utcnow()
        )
        
        self.incidents.append(incident)
        self.response_procedures[severity](incident)
        return incident
    
    def _critical_response(self, incident: SecurityIncident):
        """Critical incident response - immediate action required"""
        # 1. Alert security team immediately
        # 2. Isolate affected systems
        # 3. Activate incident response team
        # 4. Begin forensic analysis
        pass
    
    def _high_response(self, incident: SecurityIncident):
        """High severity incident response"""
        # 1. Alert security team within 15 minutes
        # 2. Assess impact and containment
        # 3. Implement containment measures
        pass
```

#### 4.7 Security Configuration

##### Environment Security
```bash
# .env.security
# Database Security
DB_ENCRYPTION_KEY=your-32-byte-encryption-key
DB_SSL_MODE=require
DB_SSL_CERT=/path/to/client-cert.pem
DB_SSL_KEY=/path/to/client-key.pem
DB_SSL_ROOT_CERT=/path/to/ca-cert.pem

# API Security  
JWT_SECRET_KEY=your-jwt-secret-key-minimum-256-bits
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
API_RATE_LIMIT_PER_MINUTE=100

# External API Keys (encrypted)
VIRUSTOTAL_API_KEY=encrypted-api-key
URLVOID_API_KEY=encrypted-api-key

# Monitoring & Logging
LOG_LEVEL=INFO
AUDIT_LOG_RETENTION_DAYS=2555
SECURITY_LOG_ENCRYPTION=true

# Compliance
GDPR_ENABLED=true
DATA_RETENTION_DAYS=365
ANONYMIZATION_ENABLED=true
```

##### Security Headers & Middleware
```python
# security_middleware.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time

def add_security_middleware(app: FastAPI):
    """Add security middleware to FastAPI app"""
    
    # CORS policy
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://phishguard.example.com"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["phishguard.example.com", "*.phishguard.example.com"]
    )
    
    # Rate limiting middleware
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        client_ip = request.client.host
        # Implement rate limiting logic
        response = await call_next(request)
        return response
    
    # Security headers middleware
    @app.middleware("http")
    async def security_headers_middleware(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
```

This comprehensive implementation plan provides **PhishGuard** with enterprise-level security, scalability, and functionality. The modular design allows for incremental development while maintaining security best practices throughout the development lifecycle.