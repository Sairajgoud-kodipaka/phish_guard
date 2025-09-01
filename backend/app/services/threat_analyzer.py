"""
Threat Analysis Service
ML-powered threat detection and classification for emails
"""

import re
import json
import pickle
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import structlog

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# spaCy will be imported only when needed
HAS_SPACY = False
spacy = None

logger = structlog.get_logger(__name__)


class ThreatAnalyzer:
    """ML-powered threat analysis and classification"""
    
    def __init__(self):
        self.logger = logger.bind(service="threat_analyzer")
        
        # Initialize models
        self.phishing_model = None
        self.spam_model = None
        self.vectorizer = None
        self.nlp = None
        
        # Threat patterns and keywords
        self.phishing_patterns = [
            r'verify.*account',
            r'suspend.*account',
            r'click.*here.*now',
            r'update.*payment',
            r'confirm.*identity',
            r'security.*alert',
            r'unauthorized.*access',
            r'winner.*lottery',
            r'inherit.*money',
            r'nigerian.*prince',
            r'urgent.*verify',
            r'immediately.*click',
            r'suspended.*hours',
            r'expires.*today'
        ]
        
        # Common domain spoofing patterns (brand name variations)
        self.spoofed_domains = {
            'paypal': ['payp4l', 'payp@l', 'paypaI', 'payp-al', 'paypal-security'],
            'amazon': ['amaz0n', 'amazom', 'amazon-security', 'amzn-security'],
            'microsoft': ['micr0soft', 'microsooft', 'microsoft-support'],
            'apple': ['appl3', 'apple-support', 'apple-security'],
            'google': ['googl3', 'google-security', 'g00gle'],
            'facebook': ['faceb00k', 'facebook-security'],
            'linkedin': ['linkedin-security', 'linkedln'],
            'twitter': ['twitter-security', 'twiter']
        }
        
        self.spam_indicators = [
            'free', 'prize', 'winner', 'lottery', 'casino', 'viagra',
            'cialis', 'weight loss', 'make money', 'work from home',
            'business opportunity', 'debt', 'credit', 'loan'
        ]
        
        self.malware_extensions = [
            '.exe', '.scr', '.bat', '.cmd', '.com', '.pif', '.vbs', 
            '.js', '.jar', '.zip', '.rar'
        ]
        
        # Load or initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models"""
        try:
            self.logger.info("Initializing threat detection models")
            
            # Try to load pre-trained models
            try:
                self._load_models()
            except:
                self.logger.info("Pre-trained models not found, initializing fallback models")
                self._create_fallback_models()
            
            # Initialize spaCy for NLP
            try:
                import spacy
                self.nlp = spacy.load("en_core_web_sm")
                global HAS_SPACY
                HAS_SPACY = True
                self.logger.info("spaCy loaded successfully")
            except Exception as e:
                self.logger.warning(f"spaCy not available ({type(e).__name__}), using basic NLP")
                self.nlp = None
                HAS_SPACY = False
                
            self.logger.info("Threat detection models initialized successfully")
            
        except Exception as e:
            self.logger.error("Failed to initialize models", error=str(e))
            self._create_fallback_models()
    
    def _create_fallback_models(self):
        """Create minimal fallback models if everything else fails"""
        self.phishing_model = None
        self.spam_model = None
        self.vectorizer = None
        self.logger.warning("Using fallback rule-based analysis only")
    
    def _load_models(self):
        """Load pre-trained models from disk"""
        # This would load actual trained models in production
        raise FileNotFoundError("No pre-trained models found")
    
    async def analyze_threat(self, email_data: Dict, content_analysis: Dict) -> Dict:
        """
        Perform comprehensive threat analysis on email
        
        Args:
            email_data: Processed email data from EmailProcessor
            content_analysis: Content analysis results
            
        Returns:
            Dict containing threat analysis results
        """
        try:
            self.logger.info("Starting threat analysis", 
                           message_id=email_data.get("message_id"))
            
            # Initialize results
            analysis_result = {
                "timestamp": datetime.utcnow().isoformat(),
                "threat_score": 0.0,
                "threat_level": "clean",
                "is_phishing": False,
                "is_spam": False,
                "is_malware": False,
                "confidence_score": 0.0,
                "analysis_details": {},
                "ml_predictions": {},
                "threat_indicators": [],
                "recommended_action": "allow"
            }
            
            # Perform different types of analysis
            phishing_result = await self._analyze_phishing(email_data)
            spam_result = await self._analyze_spam(email_data)
            malware_result = await self._analyze_malware(email_data)
            header_result = await self._analyze_headers(email_data)
            url_result = await self._analyze_urls(email_data.get("urls", []))
            
            # Combine results
            analysis_result["analysis_details"] = {
                "phishing_analysis": phishing_result,
                "spam_analysis": spam_result,
                "malware_analysis": malware_result,
                "header_analysis": header_result,
                "url_analysis": url_result,
                "content_analysis": content_analysis
            }
            
            # Calculate overall threat score
            threat_score = self._calculate_threat_score(
                phishing_result, spam_result, malware_result, 
                header_result, url_result, content_analysis
            )
            
            # Determine threat level and flags
            analysis_result.update(self._determine_threat_classification(threat_score))
            analysis_result["threat_score"] = threat_score
            
            # Collect threat indicators
            analysis_result["threat_indicators"] = self._collect_threat_indicators(
                phishing_result, spam_result, malware_result, header_result, url_result
            )
            
            # Store ML predictions
            analysis_result["ml_predictions"] = {
                "phishing_probability": phishing_result.get("ml_probability", 0.0),
                "spam_probability": spam_result.get("ml_probability", 0.0),
                "model_confidence": max(
                    phishing_result.get("confidence", 0.0),
                    spam_result.get("confidence", 0.0)
                )
            }
            
            self.logger.info("Threat analysis completed",
                           message_id=email_data.get("message_id"),
                           threat_score=threat_score,
                           threat_level=analysis_result["threat_level"])
            
            return analysis_result
            
        except Exception as e:
            self.logger.error("Threat analysis failed", 
                            message_id=email_data.get("message_id"),
                            error=str(e))
            # Return safe default
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "threat_score": 0.0,
                "threat_level": "clean",
                "is_phishing": False,
                "is_spam": False,
                "is_malware": False,
                "confidence_score": 0.0,
                "analysis_details": {"error": str(e)},
                "ml_predictions": {},
                "threat_indicators": [],
                "recommended_action": "allow"
            }
    
    async def _analyze_phishing(self, email_data: Dict) -> Dict:
        """Analyze email for phishing indicators"""
        result = {
            "is_phishing": False,
            "confidence": 0.0,
            "ml_probability": 0.0,
            "pattern_matches": [],
            "risk_factors": []
        }
        
        try:
            text_content = f"{email_data.get('subject', '')} {email_data.get('body_text', '')}"
            
            # Pattern matching
            for pattern in self.phishing_patterns:
                if re.search(pattern, text_content, re.IGNORECASE):
                    result["pattern_matches"].append(pattern)
            
            # ML prediction if model available
            if self.phishing_model and self.vectorizer:
                text_vec = self.vectorizer.transform([text_content])
                prediction = self.phishing_model.predict(text_vec)[0]
                probability = self.phishing_model.predict_proba(text_vec)[0][1]
                
                result["ml_probability"] = float(probability)
                result["is_phishing"] = prediction == 1
                result["confidence"] = float(probability)
            
            # Rule-based indicators
            sender_email = email_data.get("sender_email", "").lower()
            
            # Check for domain spoofing
            for brand, spoofed_variants in self.spoofed_domains.items():
                for spoofed in spoofed_variants:
                    if spoofed in sender_email:
                        result["risk_factors"].append(f"domain_spoofing_{brand}")
                        # High-value indicator - add extra weight
                        result["confidence"] = min(result["confidence"] + 0.4, 1.0)
            
            # Check for suspicious sender patterns
            if any(keyword in sender_email for keyword in ["security", "support", "admin", "noreply"]):
                # Check if it's from a suspicious domain (not well-known providers)
                sender_domain = sender_email.split('@')[-1] if '@' in sender_email else ""
                legitimate_domains = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]
                if sender_domain and not any(domain in sender_domain for domain in legitimate_domains):
                    # Check if it's impersonating a real company domain
                    for brand in self.spoofed_domains.keys():
                        if brand in sender_domain and sender_domain != f"{brand}.com":
                            result["risk_factors"].append(f"impersonation_{brand}")
                    if not any(f"impersonation_" in factor for factor in result["risk_factors"]):
                        result["risk_factors"].append("suspicious_sender_domain")
            
            # Enhanced urgency detection
            urgent_combinations = [
                ["urgent", "verify"], ["immediate", "action"], ["suspended", "hours"],
                ["expires", "today"], ["click", "immediately"], ["verify", "now"],
                ["account", "suspended"], ["security", "alert"]
            ]
            
            text_lower = text_content.lower()
            urgency_score = 0
            for combo in urgent_combinations:
                if all(word in text_lower for word in combo):
                    urgency_score += 0.2
                    result["risk_factors"].append(f"urgent_combo_{'_'.join(combo)}")
            
            # Single urgency words (lower weight)
            urgent_words = ["urgent", "immediate", "asap", "expires", "deadline"]
            if any(word in text_lower for word in urgent_words):
                result["risk_factors"].append("urgency_indicators")
            
            # Authentication failures
            if email_data.get("spf_result") == "fail":
                result["risk_factors"].append("spf_failure")
            if email_data.get("dkim_result") == "fail":
                result["risk_factors"].append("dkim_failure")
            if email_data.get("dmarc_result") == "fail":
                result["risk_factors"].append("dmarc_failure")
            
            # Calculate confidence with enhanced scoring
            pattern_score = len(result["pattern_matches"]) * 0.25  # Increased weight
            risk_factor_score = len(result["risk_factors"]) * 0.2   # Increased weight
            urgency_bonus = urgency_score
            
            rule_score = pattern_score + risk_factor_score + urgency_bonus
            ml_score = result["ml_probability"]
            
            # Weighted combination favoring rule-based detection for obvious cases
            if rule_score > 0.5:  # Strong rule-based indicators
                result["confidence"] = min(rule_score * 0.7 + ml_score * 0.3, 1.0)
            else:
                result["confidence"] = min((rule_score + ml_score) / 2, 1.0)
            
        except Exception as e:
            self.logger.error("Phishing analysis failed", error=str(e))
        
        return result
    
    async def _analyze_spam(self, email_data: Dict) -> Dict:
        """Analyze email for spam indicators"""
        result = {
            "is_spam": False,
            "confidence": 0.0,
            "ml_probability": 0.0,
            "spam_indicators": [],
            "score": 0.0
        }
        
        try:
            text_content = f"{email_data.get('subject', '')} {email_data.get('body_text', '')}"
            
            # Check for spam keywords
            for indicator in self.spam_indicators:
                if indicator.lower() in text_content.lower():
                    result["spam_indicators"].append(indicator)
            
            # ML prediction if model available
            if self.spam_model and self.vectorizer:
                text_vec = self.vectorizer.transform([text_content])
                prediction = self.spam_model.predict(text_vec)[0]
                probability = self.spam_model.predict_proba(text_vec)[0][1]
                
                result["ml_probability"] = float(probability)
                result["is_spam"] = prediction == 1
                result["confidence"] = float(probability)
            
            # Rule-based scoring
            spam_score = len(result["spam_indicators"]) * 0.1
            
            # Check for excessive punctuation or caps
            if "!!!" in text_content or "???" in text_content:
                spam_score += 0.2
            
            caps_ratio = sum(1 for c in text_content if c.isupper()) / max(len(text_content), 1)
            if caps_ratio > 0.3:
                spam_score += 0.3
            
            result["score"] = min(spam_score, 1.0)
            
            # Combine rule and ML scores
            combined_score = (result["score"] + result["ml_probability"]) / 2
            result["confidence"] = combined_score
            
        except Exception as e:
            self.logger.error("Spam analysis failed", error=str(e))
        
        return result
    
    async def _analyze_malware(self, email_data: Dict) -> Dict:
        """Analyze email for malware indicators"""
        result = {
            "is_malware": False,
            "confidence": 0.0,
            "suspicious_attachments": [],
            "risk_factors": []
        }
        
        try:
            attachments = email_data.get("attachments", [])
            
            for attachment in attachments:
                filename = attachment.get("filename", "").lower()
                
                # Check for suspicious file extensions
                if any(filename.endswith(ext) for ext in self.malware_extensions):
                    result["suspicious_attachments"].append({
                        "filename": attachment.get("filename"),
                        "reason": "suspicious_extension",
                        "risk_score": 0.8
                    })
                
                # Check for double extensions
                if filename.count('.') > 1:
                    result["risk_factors"].append("double_extension")
                
                # Check for executable disguised as document
                if any(word in filename for word in ["invoice", "receipt", "document"]):
                    if any(filename.endswith(ext) for ext in [".exe", ".scr", ".bat"]):
                        result["risk_factors"].append("disguised_executable")
            
            # Calculate confidence
            if result["suspicious_attachments"] or result["risk_factors"]:
                result["is_malware"] = True
                result["confidence"] = min(
                    len(result["suspicious_attachments"]) * 0.4 + 
                    len(result["risk_factors"]) * 0.3, 1.0
                )
            
        except Exception as e:
            self.logger.error("Malware analysis failed", error=str(e))
        
        return result
    
    async def _analyze_headers(self, email_data: Dict) -> Dict:
        """Analyze email headers for authenticity"""
        result = {
            "authentication_score": 1.0,
            "suspicious_headers": [],
            "missing_headers": []
        }
        
        try:
            headers = email_data.get("headers", {})
            
            # Check SPF/DKIM/DMARC
            spf_result = email_data.get("spf_result")
            dkim_result = email_data.get("dkim_result")
            dmarc_result = email_data.get("dmarc_result")
            
            auth_score = 1.0
            
            if spf_result == "fail":
                auth_score -= 0.3
                result["suspicious_headers"].append("spf_failure")
            elif spf_result is None:
                auth_score -= 0.1
                result["missing_headers"].append("spf_record")
            
            if dkim_result == "fail":
                auth_score -= 0.3
                result["suspicious_headers"].append("dkim_failure")
            elif dkim_result is None:
                auth_score -= 0.1
                result["missing_headers"].append("dkim_signature")
            
            if dmarc_result == "fail":
                auth_score -= 0.4
                result["suspicious_headers"].append("dmarc_failure")
            elif dmarc_result is None:
                auth_score -= 0.1
                result["missing_headers"].append("dmarc_policy")
            
            result["authentication_score"] = max(auth_score, 0.0)
            
        except Exception as e:
            self.logger.error("Header analysis failed", error=str(e))
        
        return result
    
    async def _analyze_urls(self, urls: List[Dict]) -> Dict:
        """Analyze URLs for malicious indicators"""
        result = {
            "suspicious_urls": [],
            "url_risk_score": 0.0,
            "total_urls": len(urls)
        }
        
        try:
            if not urls:
                return result
            
            suspicious_count = 0
            total_risk = 0.0
            
            for url_data in urls:
                url_risk = url_data.get("risk_score", 0.0)
                total_risk += url_risk
                
                # Lower threshold for flagging suspicious URLs
                if url_risk > 0.3:  # Lowered from 0.5
                    suspicious_count += 1
                    result["suspicious_urls"].append({
                        "url": url_data.get("url"),
                        "domain": url_data.get("domain"),
                        "risk_score": url_risk,
                        "reasons": []
                    })
                    
                    if url_data.get("is_shortener"):
                        result["suspicious_urls"][-1]["reasons"].append("url_shortener")
                    if url_data.get("is_suspicious"):
                        result["suspicious_urls"][-1]["reasons"].append("suspicious_pattern")
                    if url_data.get("is_misleading"):
                        result["suspicious_urls"][-1]["reasons"].append("misleading_text")
            
            result["url_risk_score"] = total_risk / len(urls) if urls else 0.0
            
        except Exception as e:
            self.logger.error("URL analysis failed", error=str(e))
        
        return result
    
    def _calculate_threat_score(self, phishing_result: Dict, spam_result: Dict, 
                               malware_result: Dict, header_result: Dict,
                               url_result: Dict, content_analysis: Dict) -> float:
        """Calculate overall threat score using weighted scoring"""
        try:
            # Weight different analysis components - URLs more important for phishing
            weights = {
                "phishing": 0.35,  # Increased slightly
                "spam": 0.15,      # Decreased 
                "malware": 0.20,   # Decreased
                "headers": 0.10,   # Decreased
                "urls": 0.20       # Doubled - URLs critical for phishing detection
            }
            
            # Get individual scores
            phishing_score = phishing_result.get("confidence", 0.0)
            spam_score = spam_result.get("confidence", 0.0)
            malware_score = malware_result.get("confidence", 0.0)
            header_score = 1.0 - header_result.get("authentication_score", 1.0)
            url_score = url_result.get("url_risk_score", 0.0)
            
            # Calculate weighted score
            total_score = (
                phishing_score * weights["phishing"] +
                spam_score * weights["spam"] +
                malware_score * weights["malware"] +
                header_score * weights["headers"] +
                url_score * weights["urls"]
            )
            
            # Add content analysis bonus
            content_risk = content_analysis.get("content_risk_score", 0.0)
            total_score += content_risk * 0.1
            
            return min(total_score, 1.0)
            
        except Exception as e:
            self.logger.error("Score calculation failed", error=str(e))
            return 0.0
    
    def _determine_threat_classification(self, threat_score: float) -> Dict:
        """Determine threat level and classification based on score"""
        result = {
            "threat_level": "clean",
            "is_phishing": False,
            "is_spam": False,
            "is_malware": False,
            "confidence_score": threat_score,
            "recommended_action": "allow"
        }
        
        # More sensitive thresholds for production security
        if threat_score >= 0.7:
            result["threat_level"] = "critical"
            result["recommended_action"] = "block"
        elif threat_score >= 0.5:
            result["threat_level"] = "high"
            result["recommended_action"] = "quarantine"
        elif threat_score >= 0.3:
            result["threat_level"] = "medium"
            result["recommended_action"] = "flag"
        elif threat_score >= 0.15:
            result["threat_level"] = "low"
            result["recommended_action"] = "allow"
        else:
            result["threat_level"] = "clean"
            result["recommended_action"] = "allow"
        
        # More sensitive threat type detection
        if threat_score >= 0.3:  # Lowered from 0.5
            result["is_phishing"] = True
        if threat_score >= 0.25:  # Lowered from 0.3
            result["is_spam"] = True
        
        return result
    
    def _collect_threat_indicators(self, phishing_result: Dict, spam_result: Dict,
                                  malware_result: Dict, header_result: Dict,
                                  url_result: Dict) -> List[str]:
        """Collect all threat indicators found during analysis"""
        indicators = []
        
        # Phishing indicators
        indicators.extend(phishing_result.get("pattern_matches", []))
        indicators.extend(phishing_result.get("risk_factors", []))
        
        # Spam indicators
        if spam_result.get("spam_indicators"):
            indicators.append("spam_keywords")
        
        # Malware indicators
        if malware_result.get("suspicious_attachments"):
            indicators.append("suspicious_attachments")
        indicators.extend(malware_result.get("risk_factors", []))
        
        # Header indicators
        indicators.extend(header_result.get("suspicious_headers", []))
        
        # URL indicators
        if url_result.get("suspicious_urls"):
            indicators.append("suspicious_urls")
        
        return list(set(indicators))  # Remove duplicates 