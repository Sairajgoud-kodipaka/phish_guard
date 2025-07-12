"""
Sample Data Generator
Creates demo emails and threats for testing and demonstration
"""

import asyncio
import random
from datetime import datetime, timedelta
from typing import List, Dict
import structlog

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, create_sample_data
from app.models.email import Email
from app.models.threat import Threat
from app.models.organization import Organization
from app.models.user import User
from app.services.email_processor import EmailProcessor
from app.services.threat_analyzer import ThreatAnalyzer

logger = structlog.get_logger(__name__)


class SampleDataGenerator:
    """Generate sample data for demo purposes"""
    
    def __init__(self):
        self.logger = logger.bind(service="sample_data")
        self.email_processor = EmailProcessor()
        self.threat_analyzer = ThreatAnalyzer()
        
        # Sample email templates
        self.sample_emails = [
            # Legitimate emails
            {
                "subject": "Your monthly statement is ready",
                "sender_email": "noreply@bank.com",
                "sender_name": "National Bank",
                "body_text": "Dear Customer, Your monthly statement for November 2024 is now available. Please log in to your account to view.",
                "threat_level": "clean",
                "is_phishing": False,
                "is_spam": False
            },
            {
                "subject": "Meeting reminder: Project sync at 2 PM",
                "sender_email": "sarah.johnson@company.com",
                "sender_name": "Sarah Johnson",
                "body_text": "Hi team, Just a reminder that we have our weekly project sync meeting at 2 PM today in conference room B.",
                "threat_level": "clean",
                "is_phishing": False,
                "is_spam": False
            },
            {
                "subject": "Welcome to our newsletter!",
                "sender_email": "newsletter@techblog.com",
                "sender_name": "TechBlog Weekly",
                "body_text": "Thank you for subscribing to our newsletter. Here are this week's top tech stories and insights.",
                "threat_level": "clean",
                "is_phishing": False,
                "is_spam": False
            },
            
            # Phishing emails
            {
                "subject": "URGENT: Your account will be suspended!",
                "sender_email": "security@fake-bank.net",
                "sender_name": "Security Team",
                "body_text": "Your account shows suspicious activity. Click here immediately to verify your identity or your account will be suspended within 24 hours. http://fake-bank-verify.suspicious.com/login",
                "threat_level": "high",
                "is_phishing": True,
                "is_spam": False,
                "urls": ["http://fake-bank-verify.suspicious.com/login"]
            },
            {
                "subject": "Re: Invoice Payment Required",
                "sender_email": "billing@amaz0n-security.com",
                "sender_name": "Amazon Billing",
                "body_text": "Dear customer, Your payment method failed. Please update your billing information immediately to avoid service interruption. Login here: http://amazon-billing.suspicious.net/update",
                "threat_level": "critical",
                "is_phishing": True,
                "is_spam": False,
                "urls": ["http://amazon-billing.suspicious.net/update"]
            },
            {
                "subject": "Security Alert: Unusual sign-in activity",
                "sender_email": "no-reply@micr0soft-security.org",
                "sender_name": "Microsoft Security",
                "body_text": "We detected unusual sign-in activity on your account. If this wasn't you, please verify your identity here: http://microsoft-verify.malicious.com/signin",
                "threat_level": "high",
                "is_phishing": True,
                "is_spam": False,
                "urls": ["http://microsoft-verify.malicious.com/signin"]
            },
            
            # Spam emails
            {
                "subject": "🎉 CONGRATULATIONS! You've WON $10,000!!!",
                "sender_email": "winner@lottery-scam.biz",
                "sender_name": "Lottery Department",
                "body_text": "CONGRATULATIONS!!! You have been selected as our GRAND PRIZE WINNER! Claim your $10,000 prize now! Act fast - limited time offer!",
                "threat_level": "medium",
                "is_phishing": False,
                "is_spam": True
            },
            {
                "subject": "Lose 30 pounds in 30 days - GUARANTEED!",
                "sender_email": "sales@diet-pills.spam",
                "sender_name": "Weight Loss Experts",
                "body_text": "Amazing new weight loss pill helps you lose 30 pounds in just 30 days! No diet, no exercise required. Order now for special discount!",
                "threat_level": "low",
                "is_phishing": False,
                "is_spam": True
            },
            {
                "subject": "Work from home - Make $5000/week!",
                "sender_email": "opportunity@work-home-scam.com",
                "sender_name": "Business Opportunity",
                "body_text": "Make $5000 per week working from home! No experience required. Join thousands of successful people. Click here to start now!",
                "threat_level": "medium",
                "is_phishing": False,
                "is_spam": True
            },
            
            # Malware/suspicious emails
            {
                "subject": "Invoice #12345 - Payment Due",
                "sender_email": "invoices@suspicious-company.evil",
                "sender_name": "Accounting Department",
                "body_text": "Please find attached invoice for recent services. Payment is due within 7 days. Open the attached file for details.",
                "threat_level": "high",
                "is_phishing": False,
                "is_spam": False,
                "attachments": [{"filename": "invoice_12345.exe", "size": 2048000, "type": "executable", "is_suspicious": True}]
            },
            {
                "subject": "Document shared with you",
                "sender_email": "shared@file-share.malware",
                "sender_name": "File Sharing Service",
                "body_text": "A document has been shared with you. Please download and review the attached file.",
                "threat_level": "critical",
                "is_phishing": False,
                "is_spam": False,
                "attachments": [{"filename": "document.pdf.exe", "size": 1024000, "type": "executable", "is_suspicious": True}]
            }
        ]
        
        # Sample threat categories
        self.threat_categories = [
            "credential_theft",
            "business_email_compromise", 
            "malware_distribution",
            "social_engineering",
            "advance_fee_fraud",
            "tech_support_scam",
            "romance_scam",
            "fake_invoice",
            "account_verification",
            "prize_notification"
        ]
        
    async def generate_sample_data(self, org_id: int, num_emails: int = 50) -> Dict:
        """Generate sample emails and threats for an organization"""
        try:
            self.logger.info("Starting sample data generation", 
                           organization_id=org_id, 
                           num_emails=num_emails)
            
            async with AsyncSessionLocal() as db:
                generated_emails = []
                generated_threats = []
                
                # Generate emails over the past 30 days
                start_date = datetime.utcnow() - timedelta(days=30)
                
                for i in range(num_emails):
                    # Select random email template
                    template = random.choice(self.sample_emails)
                    
                    # Generate random timestamp within the past 30 days
                    random_offset = random.randint(0, 30 * 24 * 60 * 60)  # 30 days in seconds
                    email_date = start_date + timedelta(seconds=random_offset)
                    
                    # Create email record
                    email = Email(
                        message_id=f"sample_{org_id}_{i}_{int(email_date.timestamp())}",
                        subject=template["subject"],
                        sender_email=template["sender_email"],
                        sender_name=template["sender_name"],
                        recipient_email="demo@phishguard.com",
                        recipient_name="Demo User",
                        date_sent=email_date - timedelta(minutes=random.randint(1, 60)),
                        date_received=email_date,
                        email_size=len(template["body_text"]) + random.randint(500, 2000),
                        body_text=template["body_text"],
                        body_html=f"<html><body><p>{template['body_text']}</p></body></html>",
                        headers=self._generate_sample_headers(template),
                        urls=template.get("urls", []),
                        attachments=template.get("attachments", []),
                        spf_result=random.choice(["pass", "fail", "neutral"]) if template["is_phishing"] else "pass",
                        dkim_result=random.choice(["pass", "fail"]) if template["is_phishing"] else "pass",
                        dmarc_result=random.choice(["pass", "fail"]) if template["is_phishing"] else "pass",
                        threat_score=self._calculate_threat_score(template),
                        threat_level=template["threat_level"],
                        is_phishing=template["is_phishing"],
                        is_spam=template["is_spam"],
                        is_malware=bool(template.get("attachments")),
                        confidence_score=random.uniform(0.7, 0.95),
                        status="completed",
                        processed_at=email_date + timedelta(seconds=random.randint(1, 30)),
                        processing_time=random.uniform(0.5, 3.0),
                        action_taken=self._determine_action(template["threat_level"]),
                        quarantined=template["threat_level"] in ["high", "critical"],
                        organization_id=org_id
                    )
                    
                    db.add(email)
                    await db.flush()  # Get email ID
                    generated_emails.append(email)
                    
                    # Create threat if email is malicious
                    if template["is_phishing"] or template["is_spam"] or template.get("attachments"):
                        threat = Threat(
                            threat_type=self._determine_threat_type(template),
                            threat_category=random.choice(self.threat_categories),
                            severity=template["threat_level"],
                            title=f"Threat detected: {template['subject'][:50]}...",
                            description=self._generate_threat_description(template),
                            indicators=self._generate_threat_indicators(template),
                            tactics=self._generate_mitre_tactics(template),
                            techniques=self._generate_mitre_techniques(template),
                            detection_method="ml_model",
                            confidence_score=email.confidence_score,
                            risk_score=email.threat_score,
                            analysis_details={"sample_data": True, "template_type": template.get("type", "unknown")},
                            ml_model_results={"phishing_probability": email.threat_score if template["is_phishing"] else 0.1},
                            status=random.choice(["detected", "investigating", "confirmed", "resolved"]),
                            action_required=template["threat_level"] in ["high", "critical"],
                            resolved=random.choice([True, False]) if template["threat_level"] == "low" else False,
                            false_positive=random.choice([True, False]) if random.random() < 0.05 else False,
                            email_id=email.id
                        )
                        
                        # Add some investigation details for resolved threats
                        if threat.resolved:
                            threat.resolved_by = "security.analyst@phishguard.com"
                            threat.resolved_at = email_date + timedelta(hours=random.randint(1, 48))
                            threat.resolution_notes = "Threat confirmed and mitigated. User notified."
                        
                        db.add(threat)
                        generated_threats.append(threat)
                
                await db.commit()
                
                self.logger.info("Sample data generation completed",
                               emails_created=len(generated_emails),
                               threats_created=len(generated_threats))
                
                return {
                    "emails_created": len(generated_emails),
                    "threats_created": len(generated_threats),
                    "organization_id": org_id,
                    "generated_at": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            self.logger.error("Sample data generation failed", error=str(e))
            raise
    
    def _generate_sample_headers(self, template: Dict) -> Dict:
        """Generate realistic email headers"""
        headers = {
            "From": f"{template['sender_name']} <{template['sender_email']}>",
            "To": "demo@phishguard.com",
            "Subject": template["subject"],
            "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000"),
            "Message-ID": f"<{random.randint(1000000, 9999999)}@{template['sender_email'].split('@')[1]}>",
            "X-Mailer": random.choice(["Outlook 16.0", "Gmail", "Thunderbird 102.0", "Apple Mail"]),
        }
        
        if template["is_phishing"]:
            # Add suspicious headers for phishing emails
            headers["Return-Path"] = f"<bounces@{random.choice(['suspicious.com', 'fake-domain.org', 'phish.net'])}>"
            headers["X-Originating-IP"] = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        return headers
    
    def _calculate_threat_score(self, template: Dict) -> float:
        """Calculate threat score based on template"""
        if template["threat_level"] == "critical":
            return random.uniform(0.85, 0.98)
        elif template["threat_level"] == "high":
            return random.uniform(0.65, 0.84)
        elif template["threat_level"] == "medium":
            return random.uniform(0.35, 0.64)
        elif template["threat_level"] == "low":
            return random.uniform(0.15, 0.34)
        else:  # clean
            return random.uniform(0.0, 0.14)
    
    def _determine_action(self, threat_level: str) -> str:
        """Determine action taken based on threat level"""
        if threat_level in ["critical", "high"]:
            return random.choice(["quarantine", "block"])
        elif threat_level == "medium":
            return random.choice(["flag", "quarantine"])
        else:
            return "allow"
    
    def _determine_threat_type(self, template: Dict) -> str:
        """Determine threat type from template"""
        if template["is_phishing"]:
            return "phishing"
        elif template["is_spam"]:
            return "spam"
        elif template.get("attachments"):
            return "malware"
        else:
            return "suspicious"
    
    def _generate_threat_description(self, template: Dict) -> str:
        """Generate threat description"""
        if template["is_phishing"]:
            return f"Phishing email attempting to steal credentials. Sender: {template['sender_email']}"
        elif template["is_spam"]:
            return f"Spam email with promotional content. Category: unsolicited marketing"
        elif template.get("attachments"):
            return f"Email with suspicious attachment: {template['attachments'][0]['filename']}"
        else:
            return "Suspicious email content detected by AI analysis"
    
    def _generate_threat_indicators(self, template: Dict) -> List[str]:
        """Generate threat indicators"""
        indicators = []
        
        if template["is_phishing"]:
            indicators.extend(["phishing_keywords", "urgency_language", "suspicious_urls"])
        if template["is_spam"]:
            indicators.extend(["spam_keywords", "promotional_content"])
        if template.get("attachments"):
            indicators.extend(["suspicious_attachment", "executable_file"])
        if "urgent" in template["subject"].lower():
            indicators.append("urgency_indicators")
        if any(domain in template["sender_email"] for domain in ["suspicious", "fake", "scam"]):
            indicators.append("suspicious_domain")
        
        return indicators
    
    def _generate_mitre_tactics(self, template: Dict) -> List[str]:
        """Generate MITRE ATT&CK tactics"""
        tactics = []
        
        if template["is_phishing"]:
            tactics.extend(["TA0001", "TA0006"])  # Initial Access, Credential Access
        if template["is_spam"]:
            tactics.append("TA0001")  # Initial Access
        if template.get("attachments"):
            tactics.extend(["TA0001", "TA0002"])  # Initial Access, Execution
        
        return tactics
    
    def _generate_mitre_techniques(self, template: Dict) -> List[str]:
        """Generate MITRE ATT&CK techniques"""
        techniques = []
        
        if template["is_phishing"]:
            techniques.extend(["T1566.002", "T1056.003"])  # Phishing: Spearphishing Link, Keylogging
        if template.get("attachments"):
            techniques.append("T1566.001")  # Phishing: Spearphishing Attachment
        if template["is_spam"]:
            techniques.append("T1566")  # Phishing
        
        return techniques


async def create_demo_organization() -> int:
    """Create a demo organization with sample data"""
    async with AsyncSessionLocal() as db:
        # Check if demo org already exists
        existing_org = await db.execute(
            select(Organization).where(Organization.domain == "demo.phishguard.com")
        )
        org = existing_org.scalar_one_or_none()
        
        if not org:
            # Create demo organization
            org = Organization(
                name="PhishGuard Demo Company",
                domain="demo.phishguard.com",
                description="Demo organization for PhishGuard testing",
                is_active=True,
                max_users=100,
                max_emails_per_day=10000,
                threat_threshold="medium",
                auto_quarantine=True,
                send_alerts=True
            )
            db.add(org)
            await db.commit()
            await db.refresh(org)
        
        return org.id


async def main():
    """Main function to generate sample data"""
    try:
        # Create demo organization
        org_id = await create_demo_organization()
        print(f"Demo organization ID: {org_id}")
        
        # Generate sample data
        generator = SampleDataGenerator()
        result = await generator.generate_sample_data(org_id, num_emails=100)
        
        print("Sample data generation completed:")
        print(f"- Emails created: {result['emails_created']}")
        print(f"- Threats created: {result['threats_created']}")
        print(f"- Organization ID: {result['organization_id']}")
        
    except Exception as e:
        print(f"Error generating sample data: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 