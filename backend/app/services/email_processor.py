"""
Email Processing Service
Handles email parsing, content extraction, and preprocessing for threat analysis
"""

import email
import email.policy
import re
import json
import mimetypes
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from email.message import EmailMessage
from urllib.parse import urlparse
import structlog

from bs4 import BeautifulSoup

# Try to import magic, use fallback if not available
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False
    print("Warning: python-magic not available, using fallback file type detection")

logger = structlog.get_logger(__name__)


class EmailProcessor:
    """Email processing and content extraction service"""
    
    def __init__(self):
        self.logger = logger.bind(service="email_processor")
        
        # Common phishing keywords for basic detection
        self.phishing_keywords = [
            "urgent", "immediate", "verify", "suspended", "expired", "click here",
            "update", "confirm", "account", "security", "billing", "payment",
            "winner", "congratulations", "prize", "lottery", "inheritance",
            "bitcoin", "cryptocurrency", "investment", "opportunity"
        ]
        
        # Suspicious URL patterns
        self.suspicious_patterns = [
            r'bit\.ly', r'tinyurl', r'goo\.gl', r't\.co',  # URL shorteners
            r'\d+\.\d+\.\d+\.\d+',  # IP addresses
            r'[a-z0-9]+-[a-z0-9]+-[a-z0-9]+\.',  # Suspicious domains
        ]
        
    async def process_email(self, email_content: str, message_id: str = None) -> Dict:
        """
        Process raw email content and extract all relevant information
        
        Args:
            email_content: Raw email content (RFC 2822 format)
            message_id: Optional message ID for tracking
            
        Returns:
            Dict containing extracted email information
        """
        try:
            self.logger.info("Processing email", message_id=message_id)
            
            # Parse email
            msg = email.message_from_string(email_content, policy=email.policy.default)
            
            # Extract basic information
            result = {
                "message_id": message_id or msg.get("Message-ID", ""),
                "subject": msg.get("Subject", ""),
                "sender_email": self._extract_email(msg.get("From", "")),
                "sender_name": self._extract_name(msg.get("From", "")),
                "recipient_email": self._extract_email(msg.get("To", "")),
                "recipient_name": self._extract_name(msg.get("To", "")),
                "date_sent": self._parse_date(msg.get("Date")),
                "headers": self._extract_headers(msg),
                "body_text": "",
                "body_html": "",
                "urls": [],
                "attachments": [],
                "email_size": len(email_content),
                "spf_result": self._extract_spf(msg),
                "dkim_result": self._extract_dkim(msg),
                "dmarc_result": self._extract_dmarc(msg),
            }
            
            # Extract email body content
            text_content, html_content = self._extract_body_content(msg)
            result["body_text"] = text_content
            result["body_html"] = html_content
            
            # Extract URLs from content
            result["urls"] = self._extract_urls(text_content, html_content)
            
            # Extract attachments
            result["attachments"] = self._extract_attachments(msg)
            
            # Basic content analysis
            result["content_analysis"] = self._analyze_content(text_content, result["subject"])
            
            self.logger.info("Email processed successfully", 
                           message_id=message_id,
                           urls_found=len(result["urls"]),
                           attachments=len(result["attachments"]))
            
            return result
            
        except Exception as e:
            self.logger.error("Email processing failed", 
                            message_id=message_id, 
                            error=str(e))
            raise
    
    def _extract_email(self, header_value: str) -> str:
        """Extract email address from header value"""
        if not header_value:
            return ""
        
        # Use regex to find email address
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, header_value)
        return matches[0] if matches else ""
    
    def _extract_name(self, header_value: str) -> str:
        """Extract display name from header value"""
        if not header_value:
            return ""
        
        # Extract name before email address
        if "<" in header_value:
            name = header_value.split("<")[0].strip()
            return name.strip('"').strip()
        return ""
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse email date header"""
        if not date_str:
            return None
        
        try:
            # Parse RFC 2822 date format
            parsed = email.utils.parsedate_to_datetime(date_str)
            return parsed
        except Exception:
            return None
    
    def _extract_headers(self, msg: EmailMessage) -> Dict:
        """Extract important email headers"""
        headers = {}
        
        important_headers = [
            "Message-ID", "Date", "From", "To", "Cc", "Bcc", "Subject",
            "Return-Path", "Reply-To", "Received", "X-Originating-IP",
            "X-Mailer", "User-Agent", "Authentication-Results",
            "Received-SPF", "DKIM-Signature", "ARC-Authentication-Results"
        ]
        
        for header in important_headers:
            value = msg.get(header)
            if value:
                headers[header] = value
        
        return headers
    
    def _extract_spf(self, msg: EmailMessage) -> Optional[str]:
        """Extract SPF result from headers"""
        received_spf = msg.get("Received-SPF", "")
        if received_spf:
            if "pass" in received_spf.lower():
                return "pass"
            elif "fail" in received_spf.lower():
                return "fail"
            elif "neutral" in received_spf.lower():
                return "neutral"
        return None
    
    def _extract_dkim(self, msg: EmailMessage) -> Optional[str]:
        """Extract DKIM result from headers"""
        auth_results = msg.get("Authentication-Results", "")
        if auth_results and "dkim=" in auth_results.lower():
            if "dkim=pass" in auth_results.lower():
                return "pass"
            elif "dkim=fail" in auth_results.lower():
                return "fail"
        return None
    
    def _extract_dmarc(self, msg: EmailMessage) -> Optional[str]:
        """Extract DMARC result from headers"""
        auth_results = msg.get("Authentication-Results", "")
        if auth_results and "dmarc=" in auth_results.lower():
            if "dmarc=pass" in auth_results.lower():
                return "pass"
            elif "dmarc=fail" in auth_results.lower():
                return "fail"
        return None
    
    def _extract_body_content(self, msg: EmailMessage) -> Tuple[str, str]:
        """Extract text and HTML body content"""
        text_content = ""
        html_content = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    text_content += part.get_content()
                elif content_type == "text/html":
                    html_content += part.get_content()
        else:
            content_type = msg.get_content_type()
            content = msg.get_content()
            if content_type == "text/plain":
                text_content = content
            elif content_type == "text/html":
                html_content = content
        
        # If we only have HTML, extract text from it
        if html_content and not text_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text()
        
        return text_content.strip(), html_content.strip()
    
    def _extract_urls(self, text_content: str, html_content: str) -> List[Dict]:
        """Extract URLs from email content"""
        urls = []
        seen_urls = set()
        
        # URL regex pattern
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        
        # Extract from text content
        text_urls = re.findall(url_pattern, text_content)
        for url in text_urls:
            if url not in seen_urls:
                urls.append(self._analyze_url(url, "text"))
                seen_urls.add(url)
        
        # Extract from HTML content
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            for link in soup.find_all('a', href=True):
                url = link['href']
                if url.startswith(('http://', 'https://')) and url not in seen_urls:
                    urls.append(self._analyze_url(url, "html", link.get_text()))
                    seen_urls.add(url)
        
        return urls
    
    def _analyze_url(self, url: str, source: str, link_text: str = "") -> Dict:
        """Analyze individual URL for suspicious characteristics"""
        parsed = urlparse(url)
        
        # Check for suspicious patterns
        is_suspicious = any(re.search(pattern, url) for pattern in self.suspicious_patterns)
        
        # Check for URL shorteners
        is_shortener = any(shortener in parsed.netloc for shortener in 
                          ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly'])
        
        # Check for mismatched link text (basic check)
        is_misleading = False
        if link_text and parsed.netloc not in link_text:
            is_misleading = True
        
        return {
            "url": url,
            "domain": parsed.netloc,
            "path": parsed.path,
            "source": source,
            "link_text": link_text,
            "is_suspicious": is_suspicious,
            "is_shortener": is_shortener,
            "is_misleading": is_misleading,
            "risk_score": self._calculate_url_risk_score(
                is_suspicious, is_shortener, is_misleading
            )
        }
    
    def _calculate_url_risk_score(self, is_suspicious: bool, is_shortener: bool, is_misleading: bool) -> float:
        """Calculate risk score for URL"""
        score = 0.0
        if is_suspicious:
            score += 0.3
        if is_shortener:
            score += 0.2
        if is_misleading:
            score += 0.4
        return min(score, 1.0)
    
    def _extract_attachments(self, msg: EmailMessage) -> List[Dict]:
        """Extract attachment information"""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()
                    if filename:
                        content = part.get_content()
                        file_size = len(content) if content else 0
                        
                        # Detect file type
                        if HAS_MAGIC and content:
                            try:
                                file_type = magic.from_buffer(content[:1024])
                            except Exception:
                                file_type = self._detect_file_type_fallback(filename)
                        else:
                            file_type = self._detect_file_type_fallback(filename)
                        
                        # Check for suspicious file types
                        suspicious_extensions = ['.exe', '.scr', '.bat', '.cmd', '.com', '.pif', '.vbs', '.js']
                        is_suspicious = any(filename.lower().endswith(ext) for ext in suspicious_extensions)
                        
                        attachments.append({
                            "filename": filename,
                            "size": file_size,
                            "type": file_type,
                            "is_suspicious": is_suspicious,
                            "risk_score": 0.8 if is_suspicious else 0.1
                        })
        
        return attachments
    
    def _detect_file_type_fallback(self, filename: str) -> str:
        """Fallback file type detection using filename extension"""
        if not filename:
            return "unknown"
        
        # Try mimetypes first
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type:
            return mime_type
        
        # Fallback to extension-based detection
        ext = filename.lower().split('.')[-1] if '.' in filename else ""
        
        extension_map = {
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'ppt': 'application/vnd.ms-powerpoint',
            'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'txt': 'text/plain',
            'csv': 'text/csv',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'zip': 'application/zip',
            'rar': 'application/x-rar-compressed',
            'exe': 'application/x-msdownload',
            'bat': 'application/x-bat',
            'cmd': 'application/x-bat',
            'scr': 'application/x-msdownload',
            'vbs': 'text/vbscript',
            'js': 'application/javascript'
        }
        
        return extension_map.get(ext, f"application/octet-stream (*.{ext})")
    
    def _analyze_content(self, text_content: str, subject: str) -> Dict:
        """Perform basic content analysis for phishing indicators"""
        combined_text = f"{subject} {text_content}".lower()
        
        # Count phishing keywords
        keyword_matches = []
        for keyword in self.phishing_keywords:
            if keyword in combined_text:
                keyword_matches.append(keyword)
        
        # Analyze urgency indicators
        urgency_words = ["urgent", "immediate", "asap", "expires", "deadline", "hurry"]
        urgency_count = sum(1 for word in urgency_words if word in combined_text)
        
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in text_content if c.isupper()) / max(len(text_content), 1)
        
        # Check for excessive punctuation
        punct_ratio = sum(1 for c in text_content if c in "!?") / max(len(text_content), 1)
        
        # Calculate content risk score
        content_risk = 0.0
        content_risk += min(len(keyword_matches) * 0.1, 0.4)  # Max 0.4 for keywords
        content_risk += min(urgency_count * 0.1, 0.3)        # Max 0.3 for urgency
        content_risk += min(caps_ratio * 0.5, 0.2)           # Max 0.2 for caps
        content_risk += min(punct_ratio * 0.8, 0.1)          # Max 0.1 for punctuation
        
        return {
            "phishing_keywords": keyword_matches,
            "urgency_indicators": urgency_count,
            "caps_ratio": round(caps_ratio, 3),
            "punctuation_ratio": round(punct_ratio, 3),
            "content_risk_score": round(min(content_risk, 1.0), 3),
            "text_length": len(text_content),
            "word_count": len(text_content.split())
        } 