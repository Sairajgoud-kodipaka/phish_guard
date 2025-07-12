'use client'

import { create } from 'zustand'
import { subscribeWithSelector } from 'zustand/middleware'

interface DashboardStats {
  totalEmails: number
  threatsDetected: number
  falsePositives: number
  detectionAccuracy: number
  change: {
    totalEmails: string
    threatsDetected: string
    falsePositives: string
    detectionAccuracy: string
  }
}

interface ThreatData {
  id: number
  email: string
  threat: string
  level: number
  time: string
  status: 'blocked' | 'quarantined' | 'delivered'
  description?: string
  indicators?: string[]
}

interface ActivityData {
  id: number
  action: string
  details: string
  time: string
  type: 'success' | 'warning' | 'info' | 'error'
  user?: string
}

interface DashboardState {
  // Data
  stats: DashboardStats
  recentThreats: ThreatData[]
  recentActivity: ActivityData[]
  isLoading: boolean
  error: string | null
  
  // Real-time updates
  lastUpdate: Date | null
  isConnected: boolean
  
  // Actions
  updateStats: (stats: Partial<DashboardStats>) => void
  addThreat: (threat: ThreatData) => void
  addActivity: (activity: ActivityData) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  setConnectionStatus: (connected: boolean) => void
  refreshDashboard: () => Promise<void>
  
  // Real-time simulation
  startSimulation: () => void
  stopSimulation: () => void
}

export const useDashboardStore = create<DashboardState>()(
  subscribeWithSelector((set, get) => ({
    // Initial state
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
    recentThreats: [
      {
        id: 1,
        email: 'urgent-payment@fake-bank.com',
        threat: 'Phishing',
        level: 89,
        time: '2 minutes ago',
        status: 'blocked',
        description: 'Suspicious payment request with fraudulent links',
        indicators: ['Suspicious sender', 'Malicious URLs', 'Social engineering'],
      },
      {
        id: 2,
        email: 'invoice-update@suspicious-domain.net',
        threat: 'Social Engineering',
        level: 76,
        time: '15 minutes ago',
        status: 'quarantined',
        description: 'Fake invoice with credential harvesting attempt',
        indicators: ['Unknown sender', 'Suspicious attachment', 'Urgency tactics'],
      },
    ],
    recentActivity: [
      {
        id: 1,
        action: 'Email Analysis Completed',
        details: 'Batch of 150 emails processed successfully',
        time: '5 minutes ago',
        type: 'success',
        user: 'System',
      },
      {
        id: 2,
        action: 'Threat Detection Alert',
        details: 'High-risk phishing attempt blocked',
        time: '12 minutes ago',
        type: 'warning',
        user: 'AI Engine',
      },
    ],
    isLoading: false,
    error: null,
    lastUpdate: new Date(),
    isConnected: false,

    // Actions
    updateStats: (newStats) =>
      set((state) => ({
        stats: { ...state.stats, ...newStats },
        lastUpdate: new Date(),
      })),

    addThreat: (threat) =>
      set((state) => ({
        recentThreats: [threat, ...state.recentThreats.slice(0, 9)], // Keep last 10
        stats: {
          ...state.stats,
          threatsDetected: state.stats.threatsDetected + 1,
        },
        lastUpdate: new Date(),
      })),

    addActivity: (activity) =>
      set((state) => ({
        recentActivity: [activity, ...state.recentActivity.slice(0, 19)], // Keep last 20
        lastUpdate: new Date(),
      })),

    setLoading: (loading) => set({ isLoading: loading }),
    setError: (error) => set({ error }),
    setConnectionStatus: (connected) => set({ isConnected: connected }),

    refreshDashboard: async () => {
      set({ isLoading: true, error: null })
      try {
        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 1000))
        
        // Simulate updated data
        set((state) => ({
          stats: {
            ...state.stats,
            totalEmails: state.stats.totalEmails + Math.floor(Math.random() * 10),
            threatsDetected: state.stats.threatsDetected + Math.floor(Math.random() * 3),
          },
          isLoading: false,
          lastUpdate: new Date(),
        }))
      } catch (error) {
        set({ error: 'Failed to refresh dashboard', isLoading: false })
      }
    },

    startSimulation: () => {
      const { addThreat, addActivity } = get()
      
      const interval = setInterval(() => {
        const mockThreats = [
          {
            email: 'suspicious@example.com',
            threat: 'Phishing',
            level: Math.floor(Math.random() * 40) + 60,
            status: 'blocked' as const,
          },
          {
            email: 'malware@fake-site.org',
            threat: 'Malware',
            level: Math.floor(Math.random() * 30) + 70,
            status: 'quarantined' as const,
          },
        ]

        const mockActivities = [
          {
            action: 'Email Processed',
            details: 'New email analyzed and classified',
            type: 'success' as const,
          },
          {
            action: 'System Update',
            details: 'Threat database updated with new patterns',
            type: 'info' as const,
          },
        ]

        // Add random threat (30% chance)
        if (Math.random() < 0.3) {
          const threat = mockThreats[Math.floor(Math.random() * mockThreats.length)]
          addThreat({
            id: Date.now(),
            ...threat,
            time: 'Just now',
            description: 'Automatically detected threat',
            indicators: ['AI Detection', 'Pattern Matching'],
          })
        }

        // Add random activity (70% chance)
        if (Math.random() < 0.7) {
          const activity = mockActivities[Math.floor(Math.random() * mockActivities.length)]
          addActivity({
            id: Date.now(),
            ...activity,
            time: 'Just now',
            user: 'System',
          })
        }
      }, 15000) // Every 15 seconds

      // Store interval for cleanup
      ;(window as any).__dashboardInterval = interval
    },

    stopSimulation: () => {
      const interval = (window as any).__dashboardInterval
      if (interval) {
        clearInterval(interval)
        delete (window as any).__dashboardInterval
      }
    },
  }))
) 