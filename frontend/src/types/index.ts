// Email related types
export interface Email {
  id: number
  from: string
  to?: string
  subject: string
  body: string
  receivedAt: Date
  threatLevel: number
  threatType: string | null
  status: 'delivered' | 'quarantined' | 'blocked'
  attachments: number
  headers?: Record<string, string>
  analysis?: AnalysisResult
}

// Threat analysis types
export interface AnalysisResult {
  id: string
  emailId: number
  overallScore: number
  nlpScore: number
  urlScore: number
  headerScore: number
  anomalyScore: number
  confidence: number
  threats: ThreatDetail[]
  createdAt: Date
}

export interface ThreatDetail {
  type: 'phishing' | 'malware' | 'social_engineering' | 'credential_harvesting' | 'spam'
  score: number
  description: string
  indicators: string[]
  severity: 'low' | 'medium' | 'high' | 'critical'
}

// Dashboard statistics - matching backend DashboardStats
export interface DashboardStats {
  total_emails: number
  emails_processed: number
  threats_detected: number
  blocked_emails: number
  quarantined_emails: number
  accuracy_percentage: number
  false_positives: number
  period_days: number
}

// User and authentication types
export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'analyst' | 'viewer'
  permissions: string[]
  lastLogin?: Date
  isActive: boolean
}

// WebSocket message types
export interface WebSocketMessage {
  type: 'threat_detected' | 'email_processed' | 'system_update' | 'user_action'
  data: any
  timestamp: string
}

// API response types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

// Filter and search types
export interface EmailFilters {
  status?: string[]
  threatLevel?: {
    min: number
    max: number
  }
  dateRange?: {
    start: Date
    end: Date
  }
  sender?: string
  threatTypes?: string[]
}

// Backend API types - matching schema responses
export interface ThreatTimelineItem {
  timeline_date: string
  threat_level: string
  count: number
}

export interface EmailActivityItem {
  timestamp: string
  email_count: number
  threat_count: number
}

export interface ThreatDistribution {
  threat_type: string
  count: number
  percentage: number
  avg_risk_score: number
}

export interface RecentActivity {
  type: string
  description: string
  severity: string
  timestamp: string
  details: Record<string, any>
}

// Chart data types
export interface ChartDataPoint {
  time: string
  threats: number
  blocked: number
  quarantined: number
  delivered: number
}

// System configuration types
export interface SystemConfig {
  thresholds: {
    phishing: number
    malware: number
    socialEngineering: number
    credentialHarvesting: number
  }
  actions: {
    blockThreshold: number
    quarantineThreshold: number
  }
  notifications: {
    emailAlerts: boolean
    webhookUrl?: string
  }
} 