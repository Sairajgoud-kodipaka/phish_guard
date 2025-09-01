/**
 * PhishGuard Backend API Client
 * Simplified client for connecting to the FastAPI backend
 */

import { DashboardStats, ThreatTimelineItem, RecentActivity } from '@/types'

const API_BASE_URL = 'http://localhost:8000'

class BackendApiClient {
  private baseURL: string
  private token: string | null = null

  constructor() {
    this.baseURL = `${API_BASE_URL}/api/v1`
  }

  setAuthToken(token: string) {
    this.token = token
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    const headers: Record<string, string> = {}

    // Only set Content-Type for non-FormData requests
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json'
    }

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`
    }

    if (options.headers) {
      Object.assign(headers, options.headers)
    }

    try {
      console.log('🔍 Frontend: Making request to:', url)
      console.log('🔍 Frontend: Request method:', options.method || 'GET')
      console.log('🔍 Frontend: Request headers:', headers)
      console.log('🔍 Frontend: Request body:', options.body)

      const response = await fetch(url, {
        ...options,
        headers,
      })

      console.log('🔍 Frontend: Response status:', response.status)

      if (!response.ok) {
        const errorText = await response.text()
        console.error('🔍 Frontend: API error response:', errorText)
        throw new Error(`API Error: ${response.status} - ${errorText}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API request failed: ${url}`, error)
      throw error
    }
  }

  // Authentication
  async login(email: string, password: string) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
  }

  // Dashboard APIs
  async getDashboardStats(days: number = 30): Promise<DashboardStats> {
    return this.request(`/dashboard/stats?days=${days}`)
  }

  async getThreatTimeline(days: number = 7): Promise<ThreatTimelineItem[]> {
    return this.request(`/dashboard/threat-timeline?days=${days}`)
  }

  async getRecentActivity(limit: number = 10): Promise<RecentActivity[]> {
    return this.request(`/dashboard/recent-activity?limit=${limit}`)
  }

  // Email Analysis APIs
  async analyzeEmail(emailContent: string) {
    if (!emailContent.trim()) {
      throw new Error('Email content cannot be empty')
    }
    
    const requestBody = { content: emailContent }
    console.log('🔍 Frontend: Sending request to /emails/analyze-text with body:', requestBody)
    
    return this.request('/emails/analyze-text', {
      method: 'POST',
      body: JSON.stringify(requestBody),
    })
  }

  async analyzeEmailFile(file: File) {
    if (!file) {
      throw new Error('No file provided')
    }
    
    if (file.size === 0) {
      throw new Error('File is empty')
    }
    
    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      throw new Error('File too large (max 10MB)')
    }
    
    const formData = new FormData()
    formData.append('file', file)

    return this.request('/emails/analyze', {
      method: 'POST',
      body: formData,
      headers: {}, // Let fetch set the content-type for FormData
    })
  }

  // Real Email Data APIs
  async getRecentEmails(limit: number = 10, days: number = 30) {
    return this.request(`/emails/recent?limit=${limit}&days=${days}`)
  }

  async getEmailStats(days: number = 30) {
    return this.request(`/emails/stats/summary?days=${days}`)
  }

  async getEmail(emailId: number) {
    return this.request(`/emails/${emailId}`)
  }

  // Health check - uses root endpoint, not API versioned one
  async healthCheck() {
    console.log('Performing health check...')
    try {
      const result = await fetch(`${API_BASE_URL}/health`)
      if (!result.ok) {
        throw new Error(`Health check failed: ${result.status}`)
      }
      const data = await result.json()
      console.log('Health check successful:', data)
      return data
    } catch (error) {
      console.error('Health check failed:', error)
      throw error
    }
  }
  
  // Test connection to backend
  async testConnection() {
    console.log('Testing backend connection...')
    try {
      const result = await this.healthCheck()
      console.log('Backend connection test successful')
      return { success: true, data: result }
    } catch (error) {
      console.error('Backend connection test failed:', error)
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error',
        details: error
      }
    }
  }
}

// Export singleton instance
export const backendApi = new BackendApiClient() 