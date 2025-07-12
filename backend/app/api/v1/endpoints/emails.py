"""
Email API Endpoints
Email management and analysis endpoints - Working Version
"""

import asyncio
import email
import hashlib
import re
from typing import List, Optional, Any, Dict, Union
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, func
from sqlalchemy.orm import selectinload

from app.core.database import get_async_db
from app.models.email import Email
from app.models.threat import Threat
from app.schemas.email import EmailResponse, EmailAnalysisResponse, EmailTextAnalysisRequest

router = APIRouter()

class EmailProcessor:
    """Email processing and analysis"""
    
    @staticmethod
    def parse_email_content(email_content: bytes, filename: str = None) -> Dict[str, Any]:
        """Parse email content from various formats"""
        try:
            # Decode content
            if isinstance(email_content, bytes):
                try:
                    content_str = email_content.decode('utf-8')
                except UnicodeDecodeError:
                    content_str = email_content.decode('latin-1', errors='ignore')
            else:
                content_str = str(email_content)
            
            # Parse as email message
            msg = email.message_from_string(content_str)
            
            # Extract basic headers
            message_id = msg.get('Message-ID', f"temp_{hashlib.md5(content_str.encode()).hexdigest()}")
            subject = msg.get('Subject', '')
            sender_email = EmailProcessor._extract_email(msg.get('From', ''))
            sender_name = EmailProcessor._extract_name(msg.get('From', ''))
            recipient_email = EmailProcessor._extract_email(msg.get('To', ''))
            recipient_name = EmailProcessor._extract_name(msg.get('To', ''))
            date_sent = EmailProcessor._parse_date(msg.get('Date'))
            
            # Extract body content
            body_text, body_html = EmailProcessor._extract_body(msg)
            
            # Extract URLs
            urls = EmailProcessor._extract_urls(body_text, body_html)
            
            # Extract attachments info
            attachments = EmailProcessor._extract_attachments(msg)
            
            # Get email authentication results
            spf_result = msg.get('Authentication-Results', '').split('spf=')[1].split()[0] if 'spf=' in msg.get('Authentication-Results', '') else 'none'
            dkim_result = msg.get('Authentication-Results', '').split('dkim=')[1].split()[0] if 'dkim=' in msg.get('Authentication-Results', '') else 'none'
            dmarc_result = msg.get('Authentication-Results', '').split('dmarc=')[1].split()[0] if 'dmarc=' in msg.get('Authentication-Results', '') else 'none'
            
            return {
                "message_id": message_id,
                "subject": subject,
                "sender_email": sender_email,
                "sender_name": sender_name,
                "recipient_email": recipient_email,
                "recipient_name": recipient_name,
                "date_sent": date_sent,
                "email_size": len(content_str),
                "body_text": body_text,
                "body_html": body_html,
                "headers": dict(msg.items()),
                "urls": urls,
                "attachments": attachments,
                "spf_result": spf_result,
                "dkim_result": dkim_result,
                "dmarc_result": dmarc_result
            }
            
        except Exception as e:
            # Fallback to simple text parsing
            return EmailProcessor._simple_text_parse(content_str if isinstance(email_content, str) else email_content.decode('utf-8', errors='ignore'))
    
    @staticmethod
    def _extract_email(header_value: str) -> str:
        """Extract email address from header"""
        if not header_value:
            return ""
        
        # Look for email in angle brackets
        email_match = re.search(r'<([^>]+)>', header_value)
        if email_match:
            return email_match.group(1)
        
        # Look for standalone email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', header_value)
        if email_match:
            return email_match.group(0)
        
        return header_value.strip()
    
    @staticmethod
    def _extract_name(header_value: str) -> str:
        """Extract name from header"""
        if not header_value:
            return ""
        
        # Remove email part
        name_part = re.sub(r'<[^>]+>', '', header_value).strip()
        return name_part.strip('"').strip()
    
    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Parse email date"""
        if not date_str:
            return datetime.utcnow()
        
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except:
            return datetime.utcnow()
    
    @staticmethod
    def _extract_body(msg) -> tuple:
        """Extract text and HTML body content"""
        body_text = ""
        body_html = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if "attachment" not in content_disposition:
                    if content_type == "text/plain":
                        body_text += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    elif content_type == "text/html":
                        body_html += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            content_type = msg.get_content_type()
            if content_type == "text/plain":
                body_text = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            elif content_type == "text/html":
                body_html = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        # Extract text from HTML if no plain text and HTML parsing available
        if not body_text and body_html:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(body_html, 'html.parser')
                body_text = soup.get_text()
            except ImportError:
                # Simple HTML tag removal
                body_text = re.sub(r'<[^>]+>', '', body_html)
        
        return body_text, body_html
    
    @staticmethod
    def _extract_urls(body_text: str, body_html: str = "") -> List[Dict[str, str]]:
        """Extract URLs from email content"""
        urls = []
        url_pattern = r'https?://[^\s<>"\{\}|\\^`\[\]]+'
        
        # Extract from text
        text_urls = re.findall(url_pattern, body_text)
        
        # Extract from HTML (simple approach)
        html_urls = []
        if body_html:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(body_html, 'html.parser')
                for link in soup.find_all('a', href=True):
                    html_urls.append(link['href'])
            except ImportError:
                # Simple href extraction
                href_pattern = r'href=["\']([^"\']+)["\']'
                html_urls = re.findall(href_pattern, body_html)
        
        # Combine and deduplicate
        all_urls = list(set(text_urls + html_urls))
        
        for url in all_urls:
            try:
                domain = url.split('/')[2] if len(url.split('/')) > 2 else ""
                urls.append({
                    "url": url,
                    "domain": domain
                })
            except:
                continue
        
        return urls
    
    @staticmethod
    def _extract_attachments(msg) -> List[Dict[str, Any]]:
        """Extract attachment information"""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append({
                            "filename": filename,
                            "content_type": part.get_content_type(),
                            "size": len(part.get_payload(decode=True)) if part.get_payload() else 0
                        })
        
        return attachments
    
    @staticmethod
    def _simple_text_parse(content: str) -> Dict[str, Any]:
        """Simple fallback parsing for plain text"""
        lines = content.strip().split('\n')
        
        subject = ""
        sender_email = ""
        body_lines = []
        in_headers = True
        
        for line in lines:
            if in_headers:
                if line.strip() == "":
                    in_headers = False
                    continue
                if line.startswith("Subject:"):
                    subject = line.replace("Subject:", "").strip()
                elif line.startswith("From:"):
                    sender_email = EmailProcessor._extract_email(line.replace("From:", "").strip())
            else:
                body_lines.append(line)
        
        body_text = '\n'.join(body_lines)
        urls = EmailProcessor._extract_urls(body_text)
        
        return {
            "message_id": f"simple_{hashlib.md5(content.encode()).hexdigest()[:16]}",
            "subject": subject or "No Subject",
            "sender_email": sender_email or "unknown@example.com",
            "sender_name": "",
            "recipient_email": "user@example.com",
            "recipient_name": "",
            "date_sent": datetime.utcnow(),
            "email_size": len(content),
            "body_text": body_text,
            "body_html": "",
            "headers": {},
            "urls": urls,
            "attachments": [],
            "spf_result": "none",
            "dkim_result": "none",
            "dmarc_result": "none"
        }

class ThreatAnalyzer:
    """Advanced threat analysis using heuristics and pattern matching"""
    
    @staticmethod
    async def analyze_threats(email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive threat analysis"""
        
        # Combine all text content for analysis
        text_content = f"{email_data.get('subject', '')} {email_data.get('body_text', '')}"
        
        # Heuristic analysis
        heuristic_results = await ThreatAnalyzer._heuristic_analysis(email_data)
        
        # URL analysis
        url_results = await ThreatAnalyzer._analyze_urls(email_data.get('urls', []))
        
        # Attachment analysis
        attachment_results = await ThreatAnalyzer._analyze_attachments(email_data.get('attachments', []))
        
        # Authentication analysis
        auth_results = ThreatAnalyzer._analyze_authentication(email_data)
        
        # Domain analysis
        domain_results = ThreatAnalyzer._analyze_sender_domain(email_data)
        
        # Combine results
        combined_score = ThreatAnalyzer._combine_threat_scores(
            heuristic_results, url_results, attachment_results, auth_results, domain_results
        )
        
        return combined_score
    
    @staticmethod
    async def _heuristic_analysis(email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Heuristic-based threat detection"""
        threat_score = 0.0
        indicators = []
        
        text_content = f"{email_data.get('subject', '')} {email_data.get('body_text', '')}".lower()
        
        # Phishing keywords with weights
        phishing_keywords = {
            'urgent': 0.15, 'verify': 0.15, 'suspend': 0.2, 'account': 0.1, 'click': 0.1,
            'login': 0.12, 'password': 0.15, 'paypal': 0.2, 'bank': 0.2, 'credit': 0.15,
            'social security': 0.25, 'tax': 0.15, 'refund': 0.15, 'winner': 0.2,
            'prize': 0.2, 'lottery': 0.25, 'inheritance': 0.25, 'congratulations': 0.1,
            'expire': 0.15, 'limited time': 0.15, 'act now': 0.2, 'confirm': 0.12, 'validate': 0.12
        }
        
        keyword_score = 0.0
        matched_keywords = []
        for keyword, weight in phishing_keywords.items():
            if keyword in text_content:
                keyword_score += weight
                matched_keywords.append(keyword)
        
        threat_score += min(keyword_score, 0.6)
        if matched_keywords:
            indicators.append(f"phishing_keywords_{len(matched_keywords)}")
        
        # Urgency detection
        urgency_words = ['urgent', 'immediate', 'expires', 'deadline', 'asap', 'emergency', 'within 24 hours']
        urgency_count = sum(1 for word in urgency_words if word in text_content)
        if urgency_count > 0:
            threat_score += urgency_count * 0.08
            indicators.append("urgency_indicators")
        
        # Money/financial indicators
        money_words = ['money', 'payment', 'transfer', 'wire', 'bitcoin', 'cryptocurrency', '$', '€', '£']
        money_count = sum(1 for word in money_words if word in text_content)
        if money_count > 2:
            threat_score += 0.15
            indicators.append("financial_request")
        
        # Suspicious grammar/spelling
        caps_ratio = sum(1 for c in text_content if c.isupper()) / max(len(text_content), 1)
        if caps_ratio > 0.3:
            threat_score += 0.1
            indicators.append("excessive_caps")
        
        # Multiple exclamation marks
        if text_content.count('!') > 3:
            threat_score += 0.05
            indicators.append("excessive_punctuation")
        
        return {
            "heuristic_score": min(threat_score, 1.0),
            "indicators": indicators,
            "keyword_matches": len(matched_keywords),
            "urgency_level": urgency_count,
            "matched_keywords": matched_keywords
        }
    
    @staticmethod
    async def _analyze_urls(urls: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze URLs for threats"""
        suspicious_score = 0.0
        url_results = []
        
        # Known malicious domains (would be from threat intelligence in production)
        malicious_domains = [
            'malware-site.org', 'phishing-test.com', 'suspicious-domain.net',
            'fake-bank.com', 'credential-harvest.com', 'scam-site.net',
            'phish-example.org', 'malicious-download.com'
        ]
        
        # Suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.click', '.download']
        
        for url_info in urls:
            url = url_info.get('url', '')
            domain = url_info.get('domain', '')
            
            url_risk = 0.0
            url_indicators = []
            
            # Check against known bad domains
            if domain in malicious_domains:
                url_risk += 0.9
                url_indicators.append("known_malicious_domain")
            
            # Check for suspicious TLDs
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                url_risk += 0.3
                url_indicators.append("suspicious_tld")
            
            # Check for URL shorteners
            shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'short.link']
            if any(shortener in domain for shortener in shorteners):
                url_risk += 0.2
                url_indicators.append("url_shortener")
            
            # Check for suspicious patterns
            if re.search(r'\d+\.\d+\.\d+\.\d+', url):  # IP address
                url_risk += 0.4
                url_indicators.append("ip_address_url")
            
            if len(domain.split('.')) > 4:  # Too many subdomains
                url_risk += 0.15
                url_indicators.append("excessive_subdomains")
            
            # Check for homograph attacks (similar looking domains)
            suspicious_chars = ['0', '1', 'l', 'o', 'rn', 'vv']
            if any(char in domain for char in suspicious_chars) and ('bank' in domain or 'paypal' in domain):
                url_risk += 0.3
                url_indicators.append("potential_homograph")
            
            url_results.append({
                "url": url,
                "domain": domain,
                "risk_score": min(url_risk, 1.0),
                "indicators": url_indicators
            })
            
            suspicious_score = max(suspicious_score, url_risk)
        
        return {
            "url_threat_score": min(suspicious_score, 1.0),
            "url_analysis": url_results,
            "total_urls": len(urls)
        }
    
    @staticmethod
    async def _analyze_attachments(attachments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze attachments for threats"""
        attachment_score = 0.0
        attachment_results = []
        
        dangerous_extensions = [
            '.exe', '.scr', '.bat', '.cmd', '.com', '.pif', '.vbs', '.js',
            '.jar', '.zip', '.rar', '.7z', '.msi', '.deb', '.dmg'
        ]
        
        suspicious_extensions = ['.docm', '.xlsm', '.pptm', '.pdf']
        
        for attachment in attachments:
            filename = attachment.get('filename', '').lower()
            content_type = attachment.get('content_type', '')
            
            att_risk = 0.0
            att_indicators = []
            
            # Check file extension
            if any(filename.endswith(ext) for ext in dangerous_extensions):
                att_risk += 0.8
                att_indicators.append("dangerous_file_extension")
            elif any(filename.endswith(ext) for ext in suspicious_extensions):
                att_risk += 0.3
                att_indicators.append("suspicious_file_extension")
            
            # Check for double extensions
            if filename.count('.') > 1:
                att_risk += 0.25
                att_indicators.append("double_extension")
            
            # Check content type mismatch
            if filename.endswith('.pdf') and 'pdf' not in content_type:
                att_risk += 0.4
                att_indicators.append("content_type_mismatch")
            
            # Check for suspicious naming patterns
            suspicious_names = ['invoice', 'receipt', 'statement', 'refund', 'payment']
            if any(name in filename for name in suspicious_names):
                att_risk += 0.2
                att_indicators.append("suspicious_filename")
            
            attachment_results.append({
                "filename": filename,
                "risk_score": min(att_risk, 1.0),
                "indicators": att_indicators
            })
            
            attachment_score = max(attachment_score, att_risk)
        
        return {
            "attachment_threat_score": min(attachment_score, 1.0),
            "attachment_analysis": attachment_results,
            "total_attachments": len(attachments)
        }
    
    @staticmethod
    def _analyze_authentication(email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze email authentication results"""
        auth_score = 0.0
        auth_indicators = []
        
        spf_result = email_data.get('spf_result', 'none').lower()
        dkim_result = email_data.get('dkim_result', 'none').lower()
        dmarc_result = email_data.get('dmarc_result', 'none').lower()
        
        # SPF analysis
        if spf_result in ['fail', 'softfail']:
            auth_score += 0.4
            auth_indicators.append(f"spf_{spf_result}")
        elif spf_result == 'none':
            auth_score += 0.1
            auth_indicators.append("spf_missing")
        
        # DKIM analysis
        if dkim_result == 'fail':
            auth_score += 0.3
            auth_indicators.append("dkim_fail")
        elif dkim_result == 'none':
            auth_score += 0.1
            auth_indicators.append("dkim_missing")
        
        # DMARC analysis
        if dmarc_result == 'fail':
            auth_score += 0.5
            auth_indicators.append("dmarc_fail")
        elif dmarc_result == 'none':
            auth_score += 0.1
            auth_indicators.append("dmarc_missing")
        
        return {
            "auth_threat_score": min(auth_score, 1.0),
            "auth_indicators": auth_indicators,
            "spf_status": spf_result,
            "dkim_status": dkim_result,
            "dmarc_status": dmarc_result
        }
    
    @staticmethod
    def _analyze_sender_domain(email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sender domain reputation"""
        domain_score = 0.0
        domain_indicators = []
        
        sender_email = email_data.get('sender_email', '')
        sender_domain = sender_email.split('@')[-1].lower() if '@' in sender_email else ''
        
        # Suspicious domain patterns
        suspicious_domains = [
            'tempmail.com', '10minutemail.com', 'guerrillamail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org'
        ]
        
        # Check against known suspicious domains
        if sender_domain in suspicious_domains:
            domain_score += 0.4
            domain_indicators.append("temporary_email_domain")
        
        # Check for lookalike domains
        legitimate_domains = ['paypal.com', 'amazon.com', 'microsoft.com', 'google.com', 'apple.com']
        for legit_domain in legitimate_domains:
            if sender_domain != legit_domain and legit_domain.replace('.', '') in sender_domain.replace('.', ''):
                domain_score += 0.6
                domain_indicators.append("domain_spoofing_attempt")
                break
        
        # Check domain age indicators (simple heuristics)
        if re.search(r'\d+', sender_domain):  # Numbers in domain
            domain_score += 0.15
            domain_indicators.append("numbers_in_domain")
        
        if len(sender_domain.split('.')[0]) > 20:  # Very long domain name
            domain_score += 0.1
            domain_indicators.append("unusually_long_domain")
        
        return {
            "domain_threat_score": min(domain_score, 1.0),
            "domain_indicators": domain_indicators,
            "sender_domain": sender_domain
        }
    
    @staticmethod
    def _combine_threat_scores(heuristic_results, url_results, attachment_results, auth_results, domain_results) -> Dict[str, Any]:
        """Combine all threat analysis results"""
        # Weighted combination of scores
        weights = {
            "heuristic": 0.4,
            "url": 0.25,
            "attachment": 0.2,
            "auth": 0.1,
            "domain": 0.25
        }
        
        combined_score = (
            heuristic_results.get("heuristic_score", 0) * weights["heuristic"] +
            url_results.get("url_threat_score", 0) * weights["url"] +
            attachment_results.get("attachment_threat_score", 0) * weights["attachment"] +
            auth_results.get("auth_threat_score", 0) * weights["auth"] +
            domain_results.get("domain_threat_score", 0) * weights["domain"]
        )
        
        # Determine threat level
        if combined_score >= 0.8:
            threat_level = "critical"
        elif combined_score >= 0.6:
            threat_level = "high"
        elif combined_score >= 0.4:
            threat_level = "medium"
        elif combined_score >= 0.2:
            threat_level = "low"
        else:
            threat_level = "clean"
        
        # Determine threat types
        is_phishing = (
            heuristic_results.get("heuristic_score", 0) > 0.4 or
            len(heuristic_results.get("indicators", [])) > 2 or
            url_results.get("url_threat_score", 0) > 0.5
        )
        is_spam = heuristic_results.get("keyword_matches", 0) > 3
        is_malware = attachment_results.get("attachment_threat_score", 0) > 0.6
        
        # Recommended action
        if combined_score >= 0.7:
            recommended_action = "quarantine"
        elif combined_score >= 0.4:
            recommended_action = "flag"
        else:
            recommended_action = "allow"
        
        # Collect all indicators
        all_indicators = (
            heuristic_results.get("indicators", []) +
            auth_results.get("auth_indicators", []) +
            domain_results.get("domain_indicators", []) +
            [item for url_result in url_results.get("url_analysis", []) for item in url_result.get("indicators", [])] +
            [item for att_result in attachment_results.get("attachment_analysis", []) for item in att_result.get("indicators", [])]
        )
        
        # Calculate confidence based on number of indicators and score consistency
        confidence_score = min(0.9, 0.6 + (len(all_indicators) * 0.05) + (combined_score * 0.3))
        
        return {
            "threat_score": float(combined_score),
            "threat_level": threat_level,
            "is_phishing": is_phishing,
            "is_spam": is_spam,
            "is_malware": is_malware,
            "confidence_score": float(confidence_score),
            "recommended_action": recommended_action,
            "threat_indicators": list(set(all_indicators)),
            "analysis_details": {
                "heuristic_analysis": heuristic_results,
                "url_analysis": url_results,
                "attachment_analysis": attachment_results,
                "auth_analysis": auth_results,
                "domain_analysis": domain_results
            },
            "ml_predictions": {
                "phishing_probability": float(combined_score),
                "spam_probability": float(max(0, combined_score - 0.1)),
                "malware_probability": float(attachment_results.get("attachment_threat_score", 0))
            }
        }

@router.get("/", response_model=List[EmailResponse])
async def get_emails(
    db: AsyncSession = Depends(get_async_db),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=50, ge=1, le=100, description="Number of records to return"),
    threat_level: Optional[str] = Query(default=None, description="Filter by threat level"),
    status: Optional[str] = Query(default=None, description="Filter by status"),
    sender: Optional[str] = Query(default=None, description="Filter by sender email"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    quarantined: Optional[bool] = Query(default=None, description="Filter by quarantine status")
):
    """Get emails with filtering and pagination"""
    try:
        organization_id = 1  # Demo organization ID
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Build query
        query = select(Email).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_date
            )
        ).options(selectinload(Email.threats))
        
        # Apply filters
        if threat_level:
            query = query.where(Email.threat_level == threat_level)
        
        if status:
            query = query.where(Email.status == status)
        
        if sender:
            query = query.where(Email.sender_email.ilike(f"%{sender}%"))
        
        if quarantined is not None:
            query = query.where(Email.quarantined == quarantined)
        
        # Add pagination and ordering
        query = query.order_by(desc(Email.date_received)).offset(skip).limit(limit)
        
        result = await db.execute(query)
        emails = result.scalars().all()
        
        return [EmailResponse.from_orm(email) for email in emails]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve emails: {str(e)}"
        )

@router.post("/analyze", response_model=EmailAnalysisResponse)
async def analyze_email(
    file: UploadFile = File(..., description="Email file (.eml format)"),
    db: AsyncSession = Depends(get_async_db)
):
    """Analyze an uploaded email file for threats"""
    return await _analyze_email_content(await file.read(), file.filename, db)

@router.post("/analyze-text", response_model=EmailAnalysisResponse)
async def analyze_email_text(
    request: EmailTextAnalysisRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """Analyze email content directly from text"""
    return await _analyze_email_content(request.content.encode('utf-8'), "text_input.txt", db)

async def _analyze_email_content(
    email_content: bytes,
    filename: str,
    db: AsyncSession
) -> EmailAnalysisResponse:
    """Analyze email content for threats using comprehensive heuristics"""
    try:
        organization_id = 1  # Demo organization ID
        start_time = datetime.utcnow()
        
        # Validate file type
        if not filename.endswith(('.eml', '.msg', '.txt')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only .eml, .msg, and .txt files are supported"
            )
        
        # Parse email content
        processed_email = EmailProcessor.parse_email_content(email_content, filename)
        
        # Perform threat analysis
        threat_result = await ThreatAnalyzer.analyze_threats(processed_email)
        
        # Create email record
        email_record = Email(
            message_id=processed_email["message_id"],
            subject=processed_email["subject"],
            sender_email=processed_email["sender_email"],
            sender_name=processed_email["sender_name"],
            recipient_email=processed_email["recipient_email"],
            recipient_name=processed_email["recipient_name"],
            date_sent=processed_email["date_sent"],
            date_received=datetime.utcnow(),
            email_size=processed_email["email_size"],
            body_text=processed_email["body_text"],
            body_html=processed_email["body_html"],
            headers=processed_email["headers"],
            urls=processed_email["urls"],
            attachments=processed_email["attachments"],
            spf_result=processed_email["spf_result"],
            dkim_result=processed_email["dkim_result"],
            dmarc_result=processed_email["dmarc_result"],
            threat_score=threat_result["threat_score"],
            threat_level=threat_result["threat_level"],
            is_phishing=threat_result["is_phishing"],
            is_spam=threat_result["is_spam"],
            is_malware=threat_result["is_malware"],
            analysis_results=threat_result["analysis_details"],
            ml_predictions=threat_result["ml_predictions"],
            confidence_score=threat_result["confidence_score"],
            status="completed",
            processed_at=datetime.utcnow(),
            organization_id=organization_id
        )
        
        # Determine action based on threat level
        if threat_result["threat_level"] in ["high", "critical"]:
            email_record.action_taken = "quarantine"
            email_record.quarantined = True
        elif threat_result["threat_level"] == "medium":
            email_record.action_taken = "flag"
            email_record.quarantined = False
        else:
            email_record.action_taken = "allow"
            email_record.quarantined = False
        
        db.add(email_record)
        await db.flush()  # Get the email ID
        
        # Create threat records if threats detected
        if threat_result.get("threat_indicators"):
            for indicator in threat_result["threat_indicators"]:
                threat_record = Threat(
                    threat_type="phishing" if threat_result["is_phishing"] else "spam",
                    severity=threat_result["threat_level"],
                    title=f"Threat detected in email: {processed_email['subject'][:100]}",
                    description=f"Advanced threat detection found: {indicator}",
                    indicators=threat_result["threat_indicators"],
                    detection_method="heuristic_analysis",
                    confidence_score=threat_result["confidence_score"],
                    risk_score=threat_result["threat_score"],
                    analysis_details=threat_result["analysis_details"],
                    ml_model_results=threat_result["ml_predictions"],
                    email_id=email_record.id
                )
                db.add(threat_record)
        
        await db.commit()
        
        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        return EmailAnalysisResponse(
            email_id=email_record.id,
            threat_score=threat_result["threat_score"],
            threat_level=threat_result["threat_level"],
            is_phishing=threat_result["is_phishing"],
            is_spam=threat_result["is_spam"],
            is_malware=threat_result["is_malware"],
            confidence_score=threat_result["confidence_score"],
            recommended_action=threat_result["recommended_action"],
            threat_indicators=threat_result["threat_indicators"],
            analysis_summary=threat_result["analysis_details"],
            url_scan_results=threat_result["analysis_details"].get("url_analysis", {}),
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Email analysis failed: {str(e)}"
        )

@router.put("/{email_id}/release")
async def release_email(
    email_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """Release email from quarantine"""
    try:
        organization_id = 1  # Demo organization ID
        
        # Get email
        query = select(Email).where(
            and_(
                Email.id == email_id,
                Email.organization_id == organization_id
            )
        )
        result = await db.execute(query)
        email = result.scalar_one_or_none()
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email not found"
            )
        
        # Release email
        email.release_from_quarantine()
        await db.commit()
        
        return {"message": "Email released from quarantine successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to release email: {str(e)}"
        )

@router.get("/stats/summary")
async def get_email_stats(
    db: AsyncSession = Depends(get_async_db),
    days: int = Query(default=30, ge=1, le=365, description="Number of days for statistics")
):
    """Get email statistics summary"""
    try:
        organization_id = 1  # Demo organization ID
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total emails
        total_query = select(func.count(Email.id)).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_date
            )
        )
        total_result = await db.execute(total_query)
        total_emails = total_result.scalar() or 0
        
        # Threat level distribution
        threat_query = select(
            Email.threat_level,
            func.count(Email.id).label("count")
        ).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_date
            )
        ).group_by(Email.threat_level)
        
        threat_result = await db.execute(threat_query)
        threat_distribution = {row.threat_level: row.count for row in threat_result}
        
        # Action distribution
        action_query = select(
            Email.action_taken,
            func.count(Email.id).label("count")
        ).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_date
            )
        ).group_by(Email.action_taken)
        
        action_result = await db.execute(action_query)
        action_distribution = {row.action_taken: row.count for row in action_result}
        
        return {
            "period_days": days,
            "total_emails": total_emails,
            "threat_distribution": threat_distribution,
            "action_distribution": action_distribution,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get email statistics: {str(e)}"
        ) 