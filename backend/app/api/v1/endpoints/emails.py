
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

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, func
from sqlalchemy.orm import selectinload

from app.core.database import get_async_db
from app.core.security import get_current_user_from_token
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

@router.get("/stats/summary")
async def get_email_stats(
    days: int = Query(default=30, ge=1, le=365, description="Number of days for statistics"),
    db: AsyncSession = Depends(get_async_db)
):
    """Get email statistics summary"""
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get total emails in period
        total_emails_query = select(func.count(Email.id)).where(
            Email.created_at >= start_date
        )
        total_emails = await db.scalar(total_emails_query) or 0
        
        # Get threat distribution
        threat_dist_query = select(
            Email.threat_level,
            func.count(Email.id)
        ).where(
            Email.created_at >= start_date
        ).group_by(Email.threat_level)
        
        threat_dist_result = await db.execute(threat_dist_query)
        threat_distribution = {
            "clean": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
            "critical": 0
        }
        
        for level, count in threat_dist_result:
            if level in threat_distribution:
                threat_distribution[level] = count
        
        # Get action distribution
        action_dist_query = select(
            Email.action_taken,
            func.count(Email.id)
        ).where(
            Email.created_at >= start_date
        ).group_by(Email.action_taken)
        
        action_dist_result = await db.execute(action_dist_query)
        action_distribution = {
            "allow": 0,
            "quarantine": 0,
            "block": 0
        }
        
        for action, count in action_dist_result:
            if action in action_distribution:
                action_distribution[action] = count
        
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

@router.get("/recent")
async def get_recent_emails(
    limit: int = Query(default=10, ge=1, le=100, description="Number of emails to return"),
    days: int = Query(default=30, ge=1, le=100, description="Number of days to look back"),
    db: AsyncSession = Depends(get_async_db)
):
    """Get recent emails with optional filtering"""
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get recent emails
        recent_emails_query = select(Email).where(
            Email.created_at >= start_date
        ).order_by(desc(Email.created_at)).limit(limit)
        
        recent_emails_result = await db.execute(recent_emails_query)
        recent_emails = recent_emails_result.scalars().all()
        
        # Convert to response format
        emails_response = []
        for email in recent_emails:
            emails_response.append({
                "id": email.id,
                "message_id": email.message_id,
                "subject": email.subject,
                "sender_email": email.sender_email,
                "sender_name": email.sender_name,
                "recipient_email": email.recipient_email,
                "recipient_name": email.recipient_name,
                "date_sent": email.date_sent,
                "email_size": email.email_size,
                "body_text": email.body_text,
                "body_html": email.body_html,
                "threat_score": email.threat_score,
                "threat_level": email.threat_level,
                "is_phishing": email.is_phishing,
                "is_spam": email.is_spam,
                "is_malware": email.is_malware,
                "confidence_score": email.confidence_score,
                "action_taken": email.action_taken,
                "processing_time": email.processing_time,
                "created_at": email.created_at,
                "updated_at": email.updated_at
            })
        
        return emails_response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recent emails: {str(e)}"
        )

@router.post("/analyze-text")
async def analyze_email_text(
    request: EmailTextAnalysisRequest = Body(..., embed=False),
    current_user: dict = None,
    db: AsyncSession = Depends(get_async_db)
):
    """Analyze email text content for threats"""
    try:
        print(f"🔍 TEXT ANALYSIS: Starting analysis for content length: {len(request.content)}")
        from app.services.enhanced_threat_analyzer import enhanced_analyzer
        
        # Analyze the email using ML model
        analysis_result = await enhanced_threat_analyzer.analyze_email(request.content)
        print(f"🤖 TEXT ANALYSIS: ML analysis result: {analysis_result}")
        
        # Get or create default organization
        from app.models.organization import Organization
        
        # Check if default organization exists
        org_query = select(Organization).where(Organization.domain == "default.local")
        org_result = await db.execute(org_query)
        default_org = org_result.scalar_one_or_none()
        
        if not default_org:
            # Create default organization
            default_org = Organization(
                name="Default Organization",
                domain="default.local",
                description="Default organization for testing",
                contact_email="admin@default.local",
                is_active=True
            )
            db.add(default_org)
            await db.commit()
            await db.refresh(default_org)
        
        # Create email record in database
        email_record_data = {
            "message_id": f"text_{hashlib.md5(request.content.encode()).hexdigest()}",
            "subject": "Text Analysis",
            "sender_email": "unknown@text.analysis",
            "sender_name": "Text Analysis",
            "recipient_email": "user@system",
            "recipient_name": "User",
            "date_sent": datetime.utcnow(),
            "date_received": datetime.utcnow(),  # Required field
            "email_size": len(request.content),
            "body_text": request.content,
            "body_html": "",
            "urls": [],  # Required field
            "attachments": [],  # Required field
            "status": "completed",  # Required field
            "threat_score": 0.8 if analysis_result.get('is_spam') else 0.1,
            "threat_level": analysis_result.get('threat_level', 'unknown'),
            "is_phishing": analysis_result.get('is_spam', False),
            "is_spam": analysis_result.get('is_spam', False),
            "is_malware": False,
            "analysis_results": {},  # Required field
            "ml_predictions": {},  # Required field
            "confidence_score": analysis_result.get('confidence', 0.0),
            "action_taken": "quarantine" if analysis_result.get('is_spam') else "allow",
            "quarantined": False,  # Required field
            "user_reported": False,  # Required field
            "false_positive": False,  # Required field
            "organization_id": default_org.id,  # Required field
            "processing_time": 0.1,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Save to database - TEXT ANALYSIS ENDPOINT
        email_record = Email(**email_record_data)
        db.add(email_record)
        await db.commit()
        await db.refresh(email_record)
        
        # Transform the result to match frontend expectations
        email_analysis_result = {
            "email_id": email_record.id,
            "threat_score": email_record.threat_score,
            "threat_level": email_record.threat_level,
            "is_phishing": email_record.is_phishing,
            "is_spam": email_record.is_spam,
            "is_malware": email_record.is_malware,
            "confidence_score": email_record.confidence_score,
            "recommended_action": email_record.action_taken,
            "threat_indicators": ["ML classification"] if email_record.is_spam else [],
            "analysis_summary": analysis_result,
            "processing_time": email_record.processing_time
        }
        
        print(f"🎯 TEXT ANALYSIS: Returning result with email_id: {email_record.id}")
        return email_analysis_result
        
    except Exception as e:
        print(f"❌ TEXT ANALYSIS: General error: {e}")
        import traceback
        print(f"❌ TEXT ANALYSIS: Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze email text: {str(e)}"
        )

@router.post("/analyze")
async def analyze_email_file(
    file: UploadFile = File(..., description="Email file to analyze"),
    current_user: dict = None,
    db: AsyncSession = Depends(get_async_db)
):
    """Analyze uploaded email file for threats"""
    try:
        from app.services.enhanced_threat_analyzer import enhanced_analyzer
        
        # Read file content
        file_content = await file.read()
        
        # Try to decode as text first
        try:
            email_text = file_content.decode('utf-8')
        except UnicodeDecodeError:
            email_text = file_content.decode('latin-1', errors='ignore')
        
        # Analyze the email using ML model
        analysis_result = await enhanced_analyzer.analyze_email(email_text)
        
        # Get or create default organization
        from app.models.organization import Organization
        
        # Check if default organization exists
        org_query = select(Organization).where(Organization.domain == "default.local")
        org_result = await db.execute(org_query)
        default_org = org_result.scalar_one_or_none()
        
        if not default_org:
            # Create default organization
            default_org = Organization(
                name="Default Organization",
                domain="default.local",
                description="Default organization for testing",
                contact_email="admin@default.local",
                is_active=True
            )
            db.add(default_org)
            await db.commit()
            await db.refresh(default_org)
        
        # Create email record in database
        email_data = {
            "message_id": f"file_{hashlib.md5(file_content).hexdigest()}",
            "subject": f"File Analysis: {file.filename}",
            "sender_email": "unknown@file.analysis",
            "sender_name": "File Analysis",
            "recipient_email": "user@system",
            "recipient_name": "User",
            "date_sent": datetime.utcnow(),
            "date_received": datetime.utcnow(),  # Required field
            "email_size": len(email_text),
            "body_text": email_text,
            "body_html": "",
            "urls": [],  # Required field
            "attachments": [],  # Required field
            "status": "completed",  # Required field
            "threat_score": 0.8 if analysis_result.get('is_spam') else 0.1,
            "threat_level": analysis_result.get('threat_level', 'unknown'),
            "is_phishing": analysis_result.get('is_spam', False),
            "is_spam": analysis_result.get('is_spam', False),
            "is_malware": False,
            "analysis_results": {},  # Required field
            "ml_predictions": {},  # Required field
            "confidence_score": analysis_result.get('confidence', 0.0),
            "action_taken": "quarantine" if analysis_result.get('is_spam') else "allow",
            "quarantined": False,  # Required field
            "user_reported": False,  # Required field
            "false_positive": False,  # Required field
            "organization_id": default_org.id,  # Required field
            "processing_time": 0.1,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Save to database
        email_record = Email(**email_data)
        db.add(email_record)
        await db.commit()
        await db.refresh(email_record)
        
        # Transform the result to match frontend expectations
        email_analysis_result = {
            "email_id": email_record.id,
            "threat_score": email_record.threat_score,
            "threat_level": email_record.threat_level,
            "is_phishing": email_record.is_phishing,
            "is_spam": email_record.is_spam,
            "is_malware": email_record.is_malware,
            "confidence_score": email_record.confidence_score,
            "recommended_action": email_record.action_taken,
            "threat_indicators": ["ML classification"] if email_record.is_spam else [],
            "analysis_summary": analysis_result,
            "processing_time": email_record.processing_time
        }
        
        return email_analysis_result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze email file: {str(e)}"
        ) 