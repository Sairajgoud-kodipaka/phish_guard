# PhishGuard Frontend Architecture - Next.js

## Table of Contents
1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Component Architecture](#component-architecture)
5. [State Management](#state-management)
6. [API Integration](#api-integration)
7. [Routing & Navigation](#routing--navigation)
8. [Authentication Flow](#authentication-flow)
9. [Real-time Features](#real-time-features)
10. [Performance Optimization](#performance-optimization)
11. [Build & Deployment](#build--deployment)
12. [Testing Strategy](#testing-strategy)

## Overview

PhishGuard frontend is a modern, high-performance web application built with **Next.js 14** and **Hero UI (Headless UI)** that provides users with an intuitive interface to monitor, analyze, and manage email security. The application leverages the latest Next.js features including App Router, Server Components, and Server Actions for optimal performance.

### Key Features
- **Real-time Email Monitoring Dashboard**
- **Interactive Threat Analysis Reports**
- **Email Security Configuration Panel**
- **User Management & Role-based Access**
- **Detailed Analytics & Reporting**
- **Mobile-responsive Design**
- **Dark/Light Theme Support**
- **SSR/SSG for SEO and Performance**

## Technology Stack

### Core Framework
```json
{
  "next": "^14.1.0",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "typescript": "^5.3.0"
}
```

### UI Components & Design System
```json
{
  "@headlessui/react": "^1.7.17",
  "@heroicons/react": "^2.0.18",
  "tailwindcss": "^3.4.0",
  "tailwind-merge": "^2.2.0",
  "class-variance-authority": "^0.7.0",
  "clsx": "^2.1.0",
  "next-themes": "^0.2.1",
  "framer-motion": "^10.16.16"
}
```

### State Management & Data Fetching
```json
{
  "zustand": "^4.5.0",
  "@tanstack/react-query": "^5.17.0",
  "axios": "^1.6.0",
  "swr": "^2.2.4"
}
```

### Charts & Visualization
```json
{
  "recharts": "^2.10.0",
  "d3": "^7.8.0",
  "@tremor/react": "^3.14.0"
}
```

### Forms & Validation
```json
{
  "react-hook-form": "^7.49.0",
  "zod": "^3.22.0",
  "@hookform/resolvers": "^3.3.0"
}
```

### Development & Testing
```json
{
  "eslint": "^8.56.0",
  "eslint-config-next": "^14.1.0",
  "prettier": "^3.2.0",
  "vitest": "^1.2.0",
  "@testing-library/react": "^14.1.0",
  "playwright": "^1.41.0"
}
```

## Project Structure

```
phishguard-frontend/
├── app/                          # Next.js 14 App Router
│   ├── (auth)/                   # Auth route group
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── (dashboard)/              # Dashboard route group
│   │   ├── analytics/
│   │   │   └── page.tsx
│   │   ├── emails/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── settings/
│   │   │   └── page.tsx
│   │   ├── threats/
│   │   │   └── page.tsx
│   │   ├── layout.tsx            # Dashboard layout
│   │   └── page.tsx              # Dashboard home
│   ├── api/                      # API routes
│   │   ├── auth/
│   │   │   └── route.ts
│   │   ├── emails/
│   │   │   └── route.ts
│   │   └── websocket/
│   │       └── route.ts
│   ├── globals.css
│   ├── layout.tsx                # Root layout
│   ├── loading.tsx               # Global loading UI
│   ├── not-found.tsx             # 404 page
│   └── page.tsx                  # Home page
├── components/                   # Reusable components
│   ├── ui/                       # Hero UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   ├── table.tsx
│   │   ├── notification.tsx
│   │   └── ...
│   ├── charts/                   # Chart components
│   │   ├── threat-timeline.tsx
│   │   ├── risk-distribution.tsx
│   │   └── email-flow-chart.tsx
│   ├── email/                    # Email-specific components
│   │   ├── email-card.tsx
│   │   ├── email-details.tsx
│   │   ├── threat-indicator.tsx
│   │   └── analysis-results.tsx
│   ├── layout/                   # Layout components
│   │   ├── app-sidebar.tsx
│   │   ├── breadcrumbs.tsx
│   │   ├── header.tsx
│   │   └── navigation.tsx
│   └── providers/                # Context providers
│       ├── auth-provider.tsx
│       ├── query-provider.tsx
│       └── theme-provider.tsx
├── hooks/                        # Custom React hooks
│   ├── use-auth.ts
│   ├── use-email-data.ts
│   ├── use-real-time.ts
│   ├── use-websocket.ts
│   └── use-theme.ts
├── lib/                          # Utility libraries
│   ├── api.ts                    # API client
│   ├── auth.ts                   # Auth utilities
│   ├── utils.ts                  # General utilities
│   ├── validations.ts            # Zod schemas
│   └── websocket.ts              # WebSocket client
├── stores/                       # Zustand stores
│   ├── auth-store.ts
│   ├── email-store.ts
│   ├── ui-store.ts
│   └── settings-store.ts
├── types/                        # TypeScript definitions
│   ├── api.ts
│   ├── auth.ts
│   ├── email.ts
│   └── globals.ts
├── public/                       # Static assets
│   ├── icons/
│   ├── images/
│   └── favicon.ico
├── next.config.js               # Next.js config
├── tailwind.config.js           # Tailwind config
├── tsconfig.json               # TypeScript config
└── package.json
```

## Component Architecture

### 1. Hero UI (Headless UI) Components Setup

#### Installation & Configuration
```bash
# Install Hero UI and related packages
npm install @headlessui/react @heroicons/react
npm install framer-motion clsx tailwind-merge
npm install class-variance-authority

# Additional utilities for styling
npm install next-themes
```

#### Core UI Components
```tsx
// components/ui/button.tsx (using Hero UI styling with CVA)
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { clsx } from "clsx"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
        secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500",
        danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
        success: "bg-green-600 text-white hover:bg-green-700 focus:ring-green-500",
        outline: "border border-gray-300 bg-transparent hover:bg-gray-50 focus:ring-gray-500",
        ghost: "bg-transparent hover:bg-gray-100 focus:ring-gray-500",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4 py-2",
        lg: "h-12 px-6 text-base",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={clsx(buttonVariants({ variant, size }), className)}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
```

### 2. Dashboard Components

#### Main Dashboard Layout
```tsx
// app/(dashboard)/layout.tsx
import { AppSidebar } from "@/components/layout/app-sidebar"
import { Header } from "@/components/layout/header"
import { Breadcrumbs } from "@/components/layout/breadcrumbs"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen bg-background">
      <AppSidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <div className="flex-1 overflow-auto">
          <div className="container mx-auto px-6 py-8">
            <Breadcrumbs />
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}
```

#### Dashboard Home Page
```tsx
// app/(dashboard)/page.tsx
import { Suspense } from 'react'
import { StatsCards } from '@/components/dashboard/stats-cards'
import { ThreatChart } from '@/components/charts/threat-timeline'
import { RecentEmails } from '@/components/email/recent-emails'
import { ThreatAlerts } from '@/components/dashboard/threat-alerts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">PhishGuard Dashboard</h2>
        <p className="text-muted-foreground">
          Monitor your email security and threat detection in real-time.
        </p>
      </div>

      <Suspense fallback={<div>Loading stats...</div>}>
        <StatsCards />
      </Suspense>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Threat Timeline</CardTitle>
            <CardDescription>
              Real-time phishing detection over the last 24 hours
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Suspense fallback={<div>Loading chart...</div>}>
              <ThreatChart />
            </Suspense>
          </CardContent>
        </Card>
        
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Active Threats</CardTitle>
          </CardHeader>
          <CardContent>
            <Suspense fallback={<div>Loading alerts...</div>}>
              <ThreatAlerts />
            </Suspense>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="recent" className="space-y-4">
        <TabsList>
          <TabsTrigger value="recent">Recent Emails</TabsTrigger>
          <TabsTrigger value="blocked">Blocked</TabsTrigger>
          <TabsTrigger value="flagged">Flagged</TabsTrigger>
        </TabsList>
        <TabsContent value="recent" className="space-y-4">
          <Suspense fallback={<div>Loading emails...</div>}>
            <RecentEmails />
          </Suspense>
        </TabsContent>
        <TabsContent value="blocked" className="space-y-4">
          <Suspense fallback={<div>Loading blocked emails...</div>}>
            <RecentEmails filter="blocked" />
          </Suspense>
        </TabsContent>
        <TabsContent value="flagged" className="space-y-4">
          <Suspense fallback={<div>Loading flagged emails...</div>}>
            <RecentEmails filter="flagged" />
          </Suspense>
        </TabsContent>
      </Tabs>
    </div>
  )
}
```

#### Stats Cards Component
```tsx
// components/dashboard/stats-cards.tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Shield, Mail, AlertTriangle, CheckCircle } from 'lucide-react'
import { useEmailStats } from '@/hooks/use-email-data'

export function StatsCards() {
  const { data: stats, isLoading } = useEmailStats()

  if (isLoading) {
    return <div>Loading...</div>
  }

  const cardData = [
    {
      title: "Total Emails Processed",
      value: stats?.totalEmails.toLocaleString() || "0",
      icon: Mail,
      description: "+12% from last month",
      trend: "up"
    },
    {
      title: "Threats Detected",
      value: stats?.threatsDetected.toString() || "0",
      icon: AlertTriangle,
      description: "-5% from last week",
      trend: "down"
    },
    {
      title: "Emails Blocked",
      value: stats?.emailsBlocked.toString() || "0",
      icon: Shield,
      description: "Real-time protection",
      trend: "neutral"
    },
    {
      title: "Clean Emails",
      value: `${stats?.cleanEmailPercentage || 0}%`,
      icon: CheckCircle,
      description: "Safe delivery rate",
      trend: "up"
    }
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {cardData.map((card, index) => (
        <Card key={index}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {card.title}
            </CardTitle>
            <card.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{card.value}</div>
            <p className="text-xs text-muted-foreground">
              {card.description}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

### 3. Email Analysis Components

#### Email Details Page
```tsx
// app/(dashboard)/emails/[id]/page.tsx
import { notFound } from 'next/navigation'
import { EmailHeader } from '@/components/email/email-header'
import { EmailContent } from '@/components/email/email-content'
import { ThreatAnalysis } from '@/components/email/threat-analysis'
import { EmailActions } from '@/components/email/email-actions'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

interface EmailPageProps {
  params: {
    id: string
  }
}

async function getEmail(id: string) {
  // This would be replaced with actual API call
  const res = await fetch(`${process.env.API_URL}/emails/${id}`, {
    cache: 'no-store'
  })
  
  if (!res.ok) {
    return null
  }
  
  return res.json()
}

export default async function EmailPage({ params }: EmailPageProps) {
  const email = await getEmail(params.id)

  if (!email) {
    notFound()
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Email Analysis</h1>
          <p className="text-muted-foreground">
            Detailed security analysis for email {email.id}
          </p>
        </div>
        <Badge variant={email.riskLevel === 'high' ? 'destructive' : 'secondary'}>
          {email.riskLevel} Risk
        </Badge>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Email Details</CardTitle>
            </CardHeader>
            <CardContent>
              <EmailHeader email={email} />
              <EmailContent content={email.content} />
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Threat Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <ThreatAnalysis analysis={email.analysis} />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <EmailActions emailId={email.id} currentStatus={email.status} />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
```

## State Management

### Zustand Store Configuration

#### Authentication Store
```tsx
// stores/auth-store.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'analyst' | 'user'
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        try {
          const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
          })

          if (!response.ok) {
            throw new Error('Login failed')
          }

          const data = await response.json()
          
          set({
            user: data.user,
            token: data.token,
            isAuthenticated: true,
          })
        } catch (error) {
          throw error
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },

      refreshToken: async () => {
        try {
          const response = await fetch('/api/auth/refresh', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${get().token}`,
            },
          })

          if (response.ok) {
            const data = await response.json()
            set({ token: data.token })
          } else {
            get().logout()
          }
        } catch (error) {
          get().logout()
        }
      },
    }),
    {
      name: 'auth-store',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
```

#### Email Data Store
```tsx
// stores/email-store.ts
import { create } from 'zustand'

interface Email {
  id: string
  sender: string
  recipient: string
  subject: string
  content: string
  riskScore: number
  status: 'safe' | 'flagged' | 'blocked'
  detectedAt: string
  threats: string[]
}

interface EmailState {
  emails: Email[]
  currentEmail: Email | null
  filters: {
    status: string[]
    riskLevel: string[]
    dateRange: [Date, Date] | null
  }
  setEmails: (emails: Email[]) => void
  addEmail: (email: Email) => void
  updateEmail: (id: string, updates: Partial<Email>) => void
  setCurrentEmail: (email: Email | null) => void
  setFilters: (filters: Partial<EmailState['filters']>) => void
  getFilteredEmails: () => Email[]
}

export const useEmailStore = create<EmailState>((set, get) => ({
  emails: [],
  currentEmail: null,
  filters: {
    status: [],
    riskLevel: [],
    dateRange: null,
  },

  setEmails: (emails) => set({ emails }),
  
  addEmail: (email) => 
    set((state) => ({ emails: [email, ...state.emails] })),
  
  updateEmail: (id, updates) =>
    set((state) => ({
      emails: state.emails.map((email) =>
        email.id === id ? { ...email, ...updates } : email
      ),
    })),
  
  setCurrentEmail: (email) => set({ currentEmail: email }),
  
  setFilters: (newFilters) =>
    set((state) => ({
      filters: { ...state.filters, ...newFilters },
    })),

  getFilteredEmails: () => {
    const { emails, filters } = get()
    return emails.filter((email) => {
      if (filters.status.length > 0 && !filters.status.includes(email.status)) {
        return false
      }
      // Add more filter logic as needed
      return true
    })
  },
}))
```

## API Integration

### API Client Setup
```tsx
// lib/api.ts
import axios from 'axios'
import { useAuthStore } from '@/stores/auth-store'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        await useAuthStore.getState().refreshToken()
        // Retry original request
        return api.request(error.config)
      } catch {
        useAuthStore.getState().logout()
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api

// API functions
export const emailAPI = {
  getEmails: (params?: any) => api.get('/emails', { params }),
  getEmail: (id: string) => api.get(`/emails/${id}`),
  analyzeEmail: (emailData: any) => api.post('/emails/analyze', emailData),
  updateEmailStatus: (id: string, status: string) => 
    api.patch(`/emails/${id}`, { status }),
}

export const authAPI = {
  login: (credentials: any) => api.post('/auth/login', credentials),
  register: (userData: any) => api.post('/auth/register', userData),
  refresh: () => api.post('/auth/refresh'),
  logout: () => api.post('/auth/logout'),
}
```

### React Query Integration
```tsx
// hooks/use-email-data.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { emailAPI } from '@/lib/api'
import { useEmailStore } from '@/stores/email-store'

export function useEmails(params?: any) {
  return useQuery({
    queryKey: ['emails', params],
    queryFn: () => emailAPI.getEmails(params),
    staleTime: 30000, // 30 seconds
  })
}

export function useEmail(id: string) {
  return useQuery({
    queryKey: ['email', id],
    queryFn: () => emailAPI.getEmail(id),
    enabled: !!id,
  })
}

export function useEmailStats() {
  return useQuery({
    queryKey: ['email-stats'],
    queryFn: async () => {
      const response = await emailAPI.getEmails({ stats: true })
      return response.data
    },
    refetchInterval: 60000, // Refresh every minute
  })
}

export function useAnalyzeEmail() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: emailAPI.analyzeEmail,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['emails'] })
    },
  })
}

export function useUpdateEmailStatus() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: string }) =>
      emailAPI.updateEmailStatus(id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['emails'] })
    },
  })
}
```

## Real-time Features

### WebSocket Integration
```tsx
// hooks/use-websocket.ts
import { useEffect, useRef } from 'react'
import { useEmailStore } from '@/stores/email-store'
import { useAuthStore } from '@/stores/auth-store'

export function useWebSocket() {
  const ws = useRef<WebSocket | null>(null)
  const { addEmail, updateEmail } = useEmailStore()
  const { token, isAuthenticated } = useAuthStore()

  useEffect(() => {
    if (!isAuthenticated || !token) return

    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'}/ws`
    ws.current = new WebSocket(`${wsUrl}?token=${token}`)

    ws.current.onopen = () => {
      console.log('WebSocket connected')
    }

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      switch (data.type) {
        case 'NEW_EMAIL':
          addEmail(data.email)
          break
        case 'EMAIL_UPDATED':
          updateEmail(data.email.id, data.email)
          break
        case 'THREAT_DETECTED':
          // Handle threat alerts
          break
      }
    }

    ws.current.onclose = () => {
      console.log('WebSocket disconnected')
    }

    return () => {
      ws.current?.close()
    }
  }, [isAuthenticated, token, addEmail, updateEmail])

  const sendMessage = (message: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message))
    }
  }

  return { sendMessage }
}
```

### Real-time Hook
```tsx
// hooks/use-real-time.ts
import { useEffect, useState } from 'react'
import { useWebSocket } from './use-websocket'
import { useQueryClient } from '@tanstack/react-query'

export function useRealTime() {
  const [connected, setConnected] = useState(false)
  const { sendMessage } = useWebSocket()
  const queryClient = useQueryClient()

  useEffect(() => {
    // Subscribe to real-time updates
    sendMessage({
      type: 'SUBSCRIBE',
      channels: ['emails', 'threats', 'stats']
    })

    return () => {
      sendMessage({
        type: 'UNSUBSCRIBE',
        channels: ['emails', 'threats', 'stats']
      })
    }
  }, [sendMessage])

  const refreshData = () => {
    queryClient.invalidateQueries()
  }

  return {
    connected,
    refreshData,
    sendMessage,
  }
}
```

## Performance Optimization

### Next.js Configuration
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
    serverComponentsExternalPackages: ['@prisma/client'],
  },
  images: {
    domains: ['localhost'],
  },
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ]
  },
  webpack: (config, { dev, isServer }) => {
    if (!dev && !isServer) {
      config.optimization.splitChunks.chunks = 'all'
    }
    return config
  },
}

module.exports = nextConfig
```

### Code Splitting & Lazy Loading
```tsx
// Dynamic imports for better performance
import dynamic from 'next/dynamic'

const ThreatChart = dynamic(
  () => import('@/components/charts/threat-timeline'),
  {
    loading: () => <div>Loading chart...</div>,
    ssr: false,
  }
)

const EmailAnalysis = dynamic(
  () => import('@/components/email/email-analysis'),
  {
    loading: () => <div>Loading analysis...</div>,
  }
)
```

## Build & Deployment

### Build Configuration
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:e2e": "playwright test"
  }
}
```

### Docker Configuration
```dockerfile
# Dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i --frozen-lockfile; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN yarn build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

## Testing Strategy

### Unit Testing with Vitest
```tsx
// __tests__/components/email-card.test.tsx
import { render, screen } from '@testing-library/react'
import { EmailCard } from '@/components/email/email-card'

const mockEmail = {
  id: '1',
  sender: 'test@example.com',
  subject: 'Test Email',
  riskScore: 0.8,
  status: 'flagged' as const,
  detectedAt: '2024-01-01T00:00:00Z',
}

describe('EmailCard', () => {
  it('renders email information correctly', () => {
    render(<EmailCard email={mockEmail} />)
    
    expect(screen.getByText('test@example.com')).toBeInTheDocument()
    expect(screen.getByText('Test Email')).toBeInTheDocument()
    expect(screen.getByText('flagged')).toBeInTheDocument()
  })

  it('displays high risk indicator for high risk emails', () => {
    render(<EmailCard email={{...mockEmail, riskScore: 0.9}} />)
    
    expect(screen.getByText(/high risk/i)).toBeInTheDocument()
  })
})
```

### E2E Testing with Playwright
```typescript
// e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
    await page.fill('[data-testid=email]', 'test@example.com')
    await page.fill('[data-testid=password]', 'password')
    await page.click('[data-testid=login-button]')
  })

  test('should display dashboard stats', async ({ page }) => {
    await page.goto('/dashboard')
    
    await expect(page.locator('[data-testid=total-emails]')).toBeVisible()
    await expect(page.locator('[data-testid=threats-detected]')).toBeVisible()
    await expect(page.locator('[data-testid=emails-blocked]')).toBeVisible()
  })

  test('should navigate to email details', async ({ page }) => {
    await page.goto('/dashboard')
    
    await page.click('[data-testid=email-row]:first-child')
    await expect(page).toHaveURL(/\/emails\/.*/)
    await expect(page.locator('[data-testid=email-details]')).toBeVisible()
  })
})
```

This comprehensive frontend architecture provides PhishGuard with a modern, performant, and maintainable user interface using Next.js 14 and Hero UI (Headless UI) - providing a perfect balance of flexibility and accessibility for React applications.