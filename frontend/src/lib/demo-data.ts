// Demo data generator for testing email preview modal

export interface DemoEmailPreviewData {
  id: number
  from: string
  to?: string
  subject: string
  body: string
  receivedAt: Date
  threatScore: number
  threatLevel: string
  isPhishing: boolean
  isSpam: boolean
  isMalware: boolean
  actionTaken: string
  processingTime: number
  confidence: number
  
  analysis: {
    nlpScore: number
    urlScore: number
    headerScore: number
    anomalyScore: number
    overallScore: number
    patterns: {
      suspiciousKeywords: string[]
      urls: Array<{
        url: string
        risk: 'low' | 'medium' | 'high' | 'critical'
        category: string
        reputation: number
      }>
      attachments: Array<{
        name: string
        type: string
        size: number
        risk: 'low' | 'medium' | 'high' | 'critical'
        analysis: string
      }>
      senderAnalysis: {
        reputation: number
        domainAge: number
        spfRecord: boolean
        dkimRecord: boolean
        dmarcRecord: boolean
        suspiciousIndicators: string[]
      }
      contentAnalysis: {
        sentiment: 'positive' | 'negative' | 'neutral'
        urgency: 'low' | 'medium' | 'high'
        impersonation: boolean
        socialEngineering: boolean
        financialPressure: boolean
        authorityPressure: boolean
      }
    }
    mlModel: {
      name: string
      version: string
      accuracy: number
      lastUpdated: string
      features: string[]
    }
    threats: Array<{
      type: string
      score: number
      description: string
      indicators: string[]
      severity: 'low' | 'medium' | 'high' | 'critical'
      confidence: number
    }>
  }
}

export const generateDemoEmailData = (): DemoEmailPreviewData => {
  const isPhishing = Math.random() > 0.5
  const threatScore = isPhishing ? Math.floor(Math.random() * 40) + 60 : Math.floor(Math.random() * 30)
  
  return {
    id: Math.floor(Math.random() * 1000) + 1,
    from: isPhishing ? 'urgent-payment@fake-bank.com' : 'invoice@legitimate-company.com',
    to: 'user@company.com',
    subject: isPhishing ? 'URGENT: Verify Your Account Immediately' : 'Monthly Invoice - December 2024',
    body: isPhishing 
      ? `Dear Valued Customer,

We have detected suspicious activity on your account. Your account will be suspended unless you verify your identity immediately.

Please click the link below to verify your account:
https://fake-bank-verify.com/secure-login

This is an urgent matter. Please respond within 24 hours to avoid account suspension.

Best regards,
Security Team
Fake Bank Security`

      : `Dear Customer,

Please find attached your monthly invoice for December 2024.

Invoice Number: INV-2024-0012
Amount Due: $299.99
Due Date: January 15, 2025

If you have any questions, please contact our support team.

Thank you for your business.

Best regards,
Accounting Team
Legitimate Company`,
    
    receivedAt: new Date(Date.now() - Math.random() * 24 * 60 * 60 * 1000),
    threatScore,
    threatLevel: threatScore > 70 ? 'high' : threatScore > 40 ? 'medium' : 'low',
    isPhishing,
    isSpam: Math.random() > 0.7,
    isMalware: Math.random() > 0.8,
    actionTaken: threatScore > 70 ? 'block' : threatScore > 40 ? 'quarantine' : 'allow',
    processingTime: Math.random() * 2 + 0.5,
    confidence: Math.floor(Math.random() * 20) + 75,
    
    analysis: {
      nlpScore: Math.floor(threatScore * 0.9),
      urlScore: Math.floor(threatScore * 0.8),
      headerScore: Math.floor(threatScore * 0.6),
      anomalyScore: Math.floor(threatScore * 0.95),
      overallScore: threatScore,
      patterns: {
        suspiciousKeywords: isPhishing ? [
          'urgent', 'verify', 'account', 'suspended', 'immediately', 'suspicious activity'
        ] : [],
        urls: isPhishing ? [
          {
            url: 'https://fake-bank-verify.com/secure-login',
            risk: 'critical' as const,
            category: 'Phishing',
            reputation: 15
          }
        ] : [],
        attachments: [],
        senderAnalysis: {
          reputation: isPhishing ? 25 : 85,
          domainAge: isPhishing ? 30 : 365,
          spfRecord: !isPhishing,
          dkimRecord: !isPhishing,
          dmarcRecord: !isPhishing,
          suspiciousIndicators: isPhishing ? ['New domain', 'Low reputation', 'Missing security records'] : []
        },
        contentAnalysis: {
          sentiment: isPhishing ? 'negative' : 'neutral',
          urgency: isPhishing ? 'high' : 'low',
          impersonation: isPhishing,
          socialEngineering: isPhishing,
          financialPressure: isPhishing,
          authorityPressure: isPhishing
        }
      },
      mlModel: {
        name: 'PhishGuard ML v2.1',
        version: '2.1.0',
        accuracy: 98.5,
        lastUpdated: '2024-12-31',
        features: ['NLP Analysis', 'URL Scanning', 'Header Analysis', 'Anomaly Detection', 'Behavioral Analysis']
      },
      threats: isPhishing ? [
        {
          type: 'Phishing',
          score: threatScore,
          description: 'Suspicious email content indicating potential phishing attempt with urgent language and suspicious URLs',
          indicators: ['Urgent language', 'Account verification request', 'Suspicious sender domain', 'Malicious URL detected'],
          severity: threatScore > 80 ? 'critical' : threatScore > 60 ? 'high' : 'medium',
          confidence: Math.floor(Math.random() * 20) + 75
        }
      ] : []
    }
  }
}

export const generateMultipleDemoEmails = (count: number): DemoEmailPreviewData[] => {
  return Array.from({ length: count }, () => generateDemoEmailData())
}
