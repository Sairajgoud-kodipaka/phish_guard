/**
 * PhishGuard Backend API Client
 * Simplified client for connecting to the FastAPI backend
 */

import { DashboardStats, ThreatTimelineItem, RecentActivity } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

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
      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (!response.ok) {
        const errorText = await response.text()
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
    return this.request('/emails/analyze-text', {
      method: 'POST',
      body: JSON.stringify({ content: emailContent }),
    })
  }

  async analyzeEmailFile(file: File) {
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
    return this.request(`/emails?limit=${limit}&days=${days}`)
  }

  async getEmailStats(days: number = 30) {
    return this.request(`/emails/stats/summary?days=${days}`)
  }

  async getEmail(emailId: number) {
    return this.request(`/emails/${emailId}`)
  }

  // Health check
  async healthCheck() {
    return this.request('/health')
  }
}

// Export singleton instance
export const backendApi = new BackendApiClient() 