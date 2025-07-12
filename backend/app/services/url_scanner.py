"""
URL Scanning Service
Analyzes URLs for reputation, malicious content, and threat indicators
"""

import re
import json
import asyncio
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin
import structlog

import httpx
from app.core.config import settings

logger = structlog.get_logger(__name__)


class URLScanner:
    """URL reputation and malicious content scanner"""
    
    def __init__(self):
        self.logger = logger.bind(service="url_scanner")
        self.client = httpx.AsyncClient(timeout=10.0)
        
        # Known malicious patterns
        self.malicious_patterns = [
            r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',  # IP addresses
            r'[a-z0-9]+-[a-z0-9]+-[a-z0-9]+\.',  # Suspicious subdomains
            r'\.tk$|\.ml$|\.ga$|\.cf$',  # Suspicious TLDs
            r'bit\.ly|tinyurl|goo\.gl|t\.co',  # URL shorteners
            r'[0-9]{10,}',  # Long number sequences in domain
        ]
        
        # Known safe domains
        self.safe_domains = {
            'google.com', 'microsoft.com', 'apple.com', 'amazon.com',
            'facebook.com', 'linkedin.com', 'twitter.com', 'github.com',
            'stackoverflow.com', 'wikipedia.org', 'youtube.com'
        }
        
        # Known shortener domains
        self.shortener_domains = {
            'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly',
            'short.link', 'tiny.cc', 'is.gd', 'v.gd'
        }
        
        # Suspicious keywords in URLs
        self.suspicious_keywords = [
            'login', 'signin', 'verify', 'account', 'security',
            'update', 'confirm', 'suspended', 'blocked', 'urgent'
        ]
    
    async def scan_urls(self, urls: List[Dict]) -> Dict:
        """
        Scan multiple URLs for threats and reputation
        
        Args:
            urls: List of URL dictionaries from email processing
            
        Returns:
            Dict containing scan results for all URLs
        """
        if not urls:
            return {"total_urls": 0, "scan_results": [], "overall_risk": 0.0}
        
        self.logger.info("Starting URL scan", total_urls=len(urls))
        
        scan_results = []
        total_risk = 0.0
        
        # Scan each URL
        for url_data in urls:
            try:
                result = await self.scan_single_url(url_data)
                scan_results.append(result)
                total_risk += result.get("risk_score", 0.0)
            except Exception as e:
                self.logger.error("URL scan failed", 
                                url=url_data.get("url"), 
                                error=str(e))
                scan_results.append({
                    "url": url_data.get("url"),
                    "status": "error",
                    "risk_score": 0.5,  # Default moderate risk for errors
                    "error": str(e)
                })
        
        overall_risk = total_risk / len(urls) if urls else 0.0
        
        return {
            "total_urls": len(urls),
            "scan_results": scan_results,
            "overall_risk": overall_risk,
            "high_risk_count": sum(1 for r in scan_results if r.get("risk_score", 0) > 0.7),
            "medium_risk_count": sum(1 for r in scan_results if 0.3 < r.get("risk_score", 0) <= 0.7),
            "scan_timestamp": asyncio.get_event_loop().time()
        }
    
    async def scan_single_url(self, url_data: Dict) -> Dict:
        """
        Scan a single URL for threats
        
        Args:
            url_data: URL data dictionary from email processing
            
        Returns:
            Dict containing scan results for the URL
        """
        url = url_data.get("url", "")
        self.logger.debug("Scanning URL", url=url)
        
        result = {
            "url": url,
            "domain": url_data.get("domain", ""),
            "status": "scanned",
            "risk_score": 0.0,
            "threat_types": [],
            "indicators": [],
            "reputation": "unknown",
            "analysis": {}
        }
        
        try:
            # Parse URL
            parsed = urlparse(url)
            
            # Perform different analysis types
            pattern_analysis = await self._analyze_url_patterns(url, parsed)
            domain_analysis = await self._analyze_domain_reputation(parsed.netloc)
            content_analysis = await self._analyze_url_content(url)
            redirect_analysis = await self._analyze_redirects(url)
            
            # Combine results
            result["analysis"] = {
                "pattern_analysis": pattern_analysis,
                "domain_analysis": domain_analysis,
                "content_analysis": content_analysis,
                "redirect_analysis": redirect_analysis
            }
            
            # Calculate overall risk score
            risk_score = self._calculate_url_risk(
                pattern_analysis, domain_analysis, content_analysis, redirect_analysis
            )
            result["risk_score"] = risk_score
            
            # Determine threat types and reputation
            result.update(self._classify_url_threat(risk_score, result["analysis"]))
            
            self.logger.debug("URL scan completed", 
                            url=url, 
                            risk_score=risk_score,
                            reputation=result["reputation"])
            
        except Exception as e:
            self.logger.error("URL scan error", url=url, error=str(e))
            result["status"] = "error"
            result["error"] = str(e)
            result["risk_score"] = 0.5  # Default moderate risk
        
        return result
    
    async def _analyze_url_patterns(self, url: str, parsed: urlparse) -> Dict:
        """Analyze URL for malicious patterns"""
        analysis = {
            "pattern_matches": [],
            "suspicious_elements": [],
            "risk_factors": []
        }
        
        # Check for malicious patterns
        for pattern in self.malicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                analysis["pattern_matches"].append(pattern)
        
        # Check domain characteristics
        domain = parsed.netloc.lower()
        
        # IP address instead of domain
        if re.match(r'^\d+\.\d+\.\d+\.\d+', domain):
            analysis["suspicious_elements"].append("ip_address_domain")
        
        # Suspicious subdomains
        subdomains = domain.split('.')
        if len(subdomains) > 3:
            analysis["suspicious_elements"].append("excessive_subdomains")
        
        # Check for suspicious keywords in path
        path = parsed.path.lower()
        for keyword in self.suspicious_keywords:
            if keyword in path:
                analysis["risk_factors"].append(f"suspicious_keyword_{keyword}")
        
        # Check for URL shorteners
        if domain in self.shortener_domains:
            analysis["suspicious_elements"].append("url_shortener")
        
        # Check for homograph attacks (basic)
        if any(ord(c) > 127 for c in domain):
            analysis["suspicious_elements"].append("non_ascii_characters")
        
        # Long query strings (potential data exfiltration)
        if len(parsed.query) > 200:
            analysis["risk_factors"].append("long_query_string")
        
        return analysis
    
    async def _analyze_domain_reputation(self, domain: str) -> Dict:
        """Analyze domain reputation and characteristics"""
        analysis = {
            "is_known_safe": False,
            "is_shortener": False,
            "age_indicators": [],
            "reputation_score": 0.5  # Default neutral
        }
        
        domain = domain.lower().strip()
        
        # Check if it's a known safe domain
        if any(safe in domain for safe in self.safe_domains):
            analysis["is_known_safe"] = True
            analysis["reputation_score"] = 0.9
        
        # Check if it's a known shortener
        if domain in self.shortener_domains:
            analysis["is_shortener"] = True
            analysis["reputation_score"] = 0.3  # Shorteners are inherently risky
        
        # Basic domain analysis
        if domain.count('-') > 2:
            analysis["age_indicators"].append("excessive_hyphens")
            analysis["reputation_score"] -= 0.1
        
        if len(domain) > 50:
            analysis["age_indicators"].append("unusually_long_domain")
            analysis["reputation_score"] -= 0.1
        
        # Check for recently registered domain indicators
        if any(char.isdigit() for char in domain.replace('.', '')):
            if sum(char.isdigit() for char in domain) > 3:
                analysis["age_indicators"].append("many_numbers_in_domain")
                analysis["reputation_score"] -= 0.1
        
        # If we have VirusTotal API key, check reputation
        if settings.VIRUSTOTAL_API_KEY:
            try:
                vt_result = await self._check_virustotal_domain(domain)
                analysis["virustotal"] = vt_result
                if vt_result.get("malicious_count", 0) > 0:
                    analysis["reputation_score"] = 0.1
            except Exception as e:
                self.logger.debug("VirusTotal check failed", domain=domain, error=str(e))
        
        analysis["reputation_score"] = max(0.0, min(1.0, analysis["reputation_score"]))
        return analysis
    
    async def _analyze_url_content(self, url: str) -> Dict:
        """Analyze URL content for threats (basic check)"""
        analysis = {
            "accessible": False,
            "status_code": None,
            "content_type": None,
            "redirect_count": 0,
            "suspicious_indicators": []
        }
        
        try:
            # Make a HEAD request to check basic properties
            response = await self.client.head(url, follow_redirects=True)
            analysis["accessible"] = True
            analysis["status_code"] = response.status_code
            analysis["content_type"] = response.headers.get("content-type", "")
            analysis["redirect_count"] = len(response.history)
            
            # Check for suspicious content types
            content_type = analysis["content_type"].lower()
            if "application/octet-stream" in content_type:
                analysis["suspicious_indicators"].append("binary_download")
            elif "application/zip" in content_type:
                analysis["suspicious_indicators"].append("archive_download")
            elif "application/exe" in content_type:
                analysis["suspicious_indicators"].append("executable_download")
            
            # Check for excessive redirects
            if analysis["redirect_count"] > 3:
                analysis["suspicious_indicators"].append("excessive_redirects")
            
        except Exception as e:
            self.logger.debug("URL content analysis failed", url=url, error=str(e))
            analysis["error"] = str(e)
        
        return analysis
    
    async def _analyze_redirects(self, url: str) -> Dict:
        """Analyze URL redirect chain for suspicious behavior"""
        analysis = {
            "redirect_chain": [],
            "suspicious_redirects": [],
            "final_domain": None
        }
        
        try:
            response = await self.client.get(url, follow_redirects=True)
            
            # Build redirect chain
            current_url = url
            for redirect in response.history:
                analysis["redirect_chain"].append({
                    "from": current_url,
                    "to": str(redirect.url),
                    "status": redirect.status_code
                })
                current_url = str(redirect.url)
            
            if response.history:
                final_parsed = urlparse(str(response.url))
                analysis["final_domain"] = final_parsed.netloc
                
                # Check if final domain is different from original
                original_domain = urlparse(url).netloc
                if analysis["final_domain"] != original_domain:
                    analysis["suspicious_redirects"].append("domain_change")
                
                # Check for multiple domain changes
                domains = [urlparse(r["to"]).netloc for r in analysis["redirect_chain"]]
                unique_domains = set(domains)
                if len(unique_domains) > 2:
                    analysis["suspicious_redirects"].append("multiple_domain_changes")
        
        except Exception as e:
            self.logger.debug("Redirect analysis failed", url=url, error=str(e))
            analysis["error"] = str(e)
        
        return analysis
    
    async def _check_virustotal_domain(self, domain: str) -> Dict:
        """Check domain reputation with VirusTotal API"""
        if not settings.VIRUSTOTAL_API_KEY:
            return {"error": "No API key configured"}
        
        try:
            url = f"{settings.VIRUSTOTAL_BASE_URL}/domain/report"
            params = {
                "apikey": settings.VIRUSTOTAL_API_KEY,
                "domain": domain
            }
            
            response = await self.client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                
                # Count malicious detections
                positives = data.get("positives", 0)
                total = data.get("total", 0)
                
                return {
                    "malicious_count": positives,
                    "total_scans": total,
                    "reputation": "malicious" if positives > 2 else "clean",
                    "scan_date": data.get("scan_date")
                }
            else:
                return {"error": f"API returned {response.status_code}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_url_risk(self, pattern_analysis: Dict, domain_analysis: Dict,
                           content_analysis: Dict, redirect_analysis: Dict) -> float:
        """Calculate overall URL risk score"""
        risk_score = 0.0
        
        # Pattern analysis contribution (30%)
        pattern_score = 0.0
        pattern_score += len(pattern_analysis.get("pattern_matches", [])) * 0.15
        pattern_score += len(pattern_analysis.get("suspicious_elements", [])) * 0.10
        pattern_score += len(pattern_analysis.get("risk_factors", [])) * 0.05
        risk_score += min(pattern_score, 0.3)
        
        # Domain reputation contribution (40%)
        domain_score = 1.0 - domain_analysis.get("reputation_score", 0.5)
        risk_score += domain_score * 0.4
        
        # Content analysis contribution (20%)
        content_score = 0.0
        if not content_analysis.get("accessible", False):
            content_score += 0.1  # Inaccessible URLs are slightly suspicious
        content_score += len(content_analysis.get("suspicious_indicators", [])) * 0.1
        risk_score += min(content_score, 0.2)
        
        # Redirect analysis contribution (10%)
        redirect_score = 0.0
        redirect_score += len(redirect_analysis.get("suspicious_redirects", [])) * 0.05
        risk_score += min(redirect_score, 0.1)
        
        return min(risk_score, 1.0)
    
    def _classify_url_threat(self, risk_score: float, analysis: Dict) -> Dict:
        """Classify URL threat level and types"""
        result = {
            "reputation": "unknown",
            "threat_types": [],
            "indicators": []
        }
        
        # Determine reputation
        if risk_score >= 0.8:
            result["reputation"] = "malicious"
        elif risk_score >= 0.6:
            result["reputation"] = "suspicious"
        elif risk_score >= 0.3:
            result["reputation"] = "questionable"
        else:
            result["reputation"] = "clean"
        
        # Determine threat types
        domain_analysis = analysis.get("domain_analysis", {})
        pattern_analysis = analysis.get("pattern_analysis", {})
        content_analysis = analysis.get("content_analysis", {})
        
        if domain_analysis.get("is_shortener"):
            result["threat_types"].append("url_shortener")
        
        if "ip_address_domain" in pattern_analysis.get("suspicious_elements", []):
            result["threat_types"].append("suspicious_domain")
        
        if "binary_download" in content_analysis.get("suspicious_indicators", []):
            result["threat_types"].append("malware_download")
        
        if any("suspicious_keyword" in factor for factor in pattern_analysis.get("risk_factors", [])):
            result["threat_types"].append("phishing_indicators")
        
        # Collect all indicators
        indicators = []
        indicators.extend(pattern_analysis.get("pattern_matches", []))
        indicators.extend(pattern_analysis.get("suspicious_elements", []))
        indicators.extend(content_analysis.get("suspicious_indicators", []))
        result["indicators"] = indicators
        
        return result
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose() 