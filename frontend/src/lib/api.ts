import { 
  Email, 
  ThreatDetail, 
  DashboardStats, 
  ThreatTimelineItem, 
  EmailActivityItem, 
  ThreatDistribution, 
  RecentActivity 
} from '@/types'

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'
const API_VERSION = 'v1'

// API Response Types
export interface ApiResponse<T = any> {
  data: T
  message?: string
  status: 'success' | 'error'
  pagination?: {
    page: number
    size: number
    total: number
    pages: number
  }
}

export interface ApiError {
  message: string
  code: string
  details?: any
}

// API Client Class
class ApiClient {
  private baseURL: string
  private token: string | null = null

  constructor(baseURL: string) {
    this.baseURL = `${baseURL}/${API_VERSION}`
  }

  setAuthToken(token: string) {
    this.token = token
  }

  clearAuthToken() {
    this.token = null
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || `HTTP ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      throw new Error(error instanceof Error ? error.message : 'Network error')
    }
  }

  // Authentication endpoints
  async login(email: string, password: string): Promise<ApiResponse<{ token: string; user: any }>> {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
  }

  async logout(): Promise<ApiResponse> {
    return this.request('/auth/logout', {
      method: 'POST',
    })
  }

  async refreshToken(): Promise<ApiResponse<{ token: string }>> {
    return this.request('/auth/refresh', {
      method: 'POST',
    })
  }

  // Dashboard endpoints - Updated for backend integration
  async getDashboardStats(): Promise<ApiResponse<DashboardStats>> {
    return this.request('/dashboard/stats')
  }

  async getThreatTimeline(days: number = 7): Promise<ApiResponse<ThreatTimelineItem[]>> {
    return this.request(`/dashboard/threat-timeline?days=${days}`)
  }

  async getEmailActivity(hours: number = 24): Promise<ApiResponse<EmailActivityItem[]>> {
    return this.request(`/dashboard/email-activity?hours=${hours}`)
  }

  async getThreatDistribution(days: number = 30): Promise<ApiResponse<ThreatDistribution[]>> {
    return this.request(`/dashboard/threat-distribution?days=${days}`)
  }

  async getRecentActivity(limit: number = 10): Promise<ApiResponse<RecentActivity[]>> {
    return this.request(`/dashboard/recent-activity?limit=${limit}`)
  }

  // Email endpoints
  async getEmails(params: {
    page?: number
    size?: number
    search?: string
    status?: string
    threatLevel?: string
    sortBy?: string
    sortOrder?: 'asc' | 'desc'
  } = {}): Promise<ApiResponse<Email[]>> {
    const queryString = new URLSearchParams(
      Object.entries(params).filter(([_, value]) => value !== undefined)
    ).toString()
    
    return this.request(`/emails?${queryString}`)
  }

  async getEmailById(id: string): Promise<ApiResponse<Email>> {
    return this.request(`/emails/${id}`)
  }

  async analyzeEmail(emailData: {
    to: string
    from: string
    subject: string
    body: string
    headers?: Record<string, string>
  }): Promise<ApiResponse<{ analysisId: string }>> {
    return this.request('/emails/analyze', {
      method: 'POST',
      body: JSON.stringify(emailData),
    })
  }

  async getAnalysisResult(analysisId: string): Promise<ApiResponse<any>> {
    return this.request(`/emails/analysis/${analysisId}`)
  }

  async updateEmailStatus(id: string, status: string): Promise<ApiResponse> {
    return this.request(`/emails/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    })
  }

  // Threats endpoints
  async getThreats(params: {
    page?: number
    size?: number
    status?: string
    threatType?: string
    minRiskLevel?: number
    dateFrom?: string
    dateTo?: string
  } = {}): Promise<ApiResponse<ThreatData[]>> {
    const queryString = new URLSearchParams(
      Object.entries(params).filter(([_, value]) => value !== undefined)
    ).toString()
    
    return this.request(`/threats?${queryString}`)
  }

  async getThreatById(id: string): Promise<ApiResponse<ThreatData>> {
    return this.request(`/threats/${id}`)
  }

  async updateThreatStatus(id: string, status: string): Promise<ApiResponse> {
    return this.request(`/threats/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    })
  }

  // Reports endpoints
  async generateReport(reportType: string, params: {
    dateFrom?: string
    dateTo?: string
    format?: 'pdf' | 'excel' | 'csv' | 'json'
    includeCharts?: boolean
    includeRawData?: boolean
  }): Promise<ApiResponse<{ reportId: string }>> {
    return this.request('/reports/generate', {
      method: 'POST',
      body: JSON.stringify({ reportType, ...params }),
    })
  }

  async getReportStatus(reportId: string): Promise<ApiResponse<{
    status: 'pending' | 'processing' | 'completed' | 'failed'
    progress?: number
    downloadUrl?: string
  }>> {
    return this.request(`/reports/${reportId}/status`)
  }

  async downloadReport(reportId: string): Promise<Blob> {
    const response = await fetch(`${this.baseURL}/reports/${reportId}/download`, {
      headers: this.token ? { Authorization: `Bearer ${this.token}` } : {},
    })
    
    if (!response.ok) {
      throw new Error('Failed to download report')
    }
    
    return response.blob()
  }

  // Settings endpoints
  async getSettings(): Promise<ApiResponse<any>> {
    return this.request('/settings')
  }

  async updateSettings(settings: any): Promise<ApiResponse> {
    return this.request('/settings', {
      method: 'PUT',
      body: JSON.stringify(settings),
    })
  }

  async getUsers(): Promise<ApiResponse<any[]>> {
    return this.request('/users')
  }

  async createUser(userData: any): Promise<ApiResponse<any>> {
    return this.request('/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    })
  }

  async updateUser(id: string, userData: any): Promise<ApiResponse> {
    return this.request(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    })
  }

  async deleteUser(id: string): Promise<ApiResponse> {
    return this.request(`/users/${id}`, {
      method: 'DELETE',
    })
  }

  // Analytics endpoints
  async getThreatTimeline(params: {
    dateFrom: string
    dateTo: string
    granularity?: 'hour' | 'day' | 'week' | 'month'
  }): Promise<ApiResponse<any[]>> {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/analytics/threat-timeline?${queryString}`)
  }

  async getThreatDistribution(): Promise<ApiResponse<any[]>> {
    return this.request('/analytics/threat-distribution')
  }

  async getPerformanceMetrics(): Promise<ApiResponse<any>> {
    return this.request('/analytics/performance')
  }

  // File upload endpoints
  async uploadFile(file: File, type: 'email' | 'attachment'): Promise<ApiResponse<{ fileId: string }>> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('type', type)

    return this.request('/files/upload', {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set content-type for FormData
    })
  }

  // Health check
  async healthCheck(): Promise<ApiResponse<{ status: string; timestamp: string }>> {
    return this.request('/health')
  }
}

// Create API client instance
export const apiClient = new ApiClient(API_BASE_URL)

// Utility functions for common operations
export const api = {
  // Authentication helpers
  login: (email: string, password: string) => apiClient.login(email, password),
  logout: () => apiClient.logout(),
  
  // Dashboard data
  getDashboard: async () => {
    const [stats, threats, activity] = await Promise.all([
      apiClient.getDashboardStats(),
      apiClient.getRecentThreats(),
      apiClient.getRecentActivity(),
    ])
    
    return {
      stats: stats.data,
      threats: threats.data,
      activity: activity.data,
    }
  },
  
  // Email operations
  getEmails: (params?: any) => apiClient.getEmails(params),
  analyzeEmail: (emailData: any) => apiClient.analyzeEmail(emailData),
  
  // Threat operations
  getThreats: (params?: any) => apiClient.getThreats(params),
  
  // Report operations
  generateReport: (type: string, params?: any) => apiClient.generateReport(type, params),
  
  // Settings
  getSettings: () => apiClient.getSettings(),
  updateSettings: (settings: any) => apiClient.updateSettings(settings),
}

// Error handling helper
export const handleApiError = (error: any): string => {
  if (error instanceof Error) {
    return error.message
  }
  
  if (typeof error === 'string') {
    return error
  }
  
  return 'An unexpected error occurred'
}

// Mock data flag - remove in production
export const USE_MOCK_DATA = process.env.NODE_ENV === 'development' && !process.env.NEXT_PUBLIC_API_URL

// Mock API implementation for development
export const mockApi = {
  login: async (email: string, password: string) => {
    await new Promise(resolve => setTimeout(resolve, 1000))
    if (email === 'admin@phishguard.com' && password === 'demo123') {
      return {
        data: {
          token: 'mock-jwt-token',
          user: { id: 1, email, name: 'Demo User', role: 'Administrator' }
        },
        status: 'success' as const
      }
    }
    throw new Error('Invalid credentials')
  },
  
  getDashboard: async () => {
    await new Promise(resolve => setTimeout(resolve, 500))
    return {
      stats: {
        totalEmails: 12847,
        threatsDetected: 324,
        falsePositives: 23,
        detectionAccuracy: 97.2,
        change: {
          totalEmails: '+12%',
          threatsDetected: '-8%',
          falsePositives: '+2%',
          detectionAccuracy: '+0.3%',
        },
      },
      threats: [],
      activity: [],
    }
  },
}

export default apiClient 