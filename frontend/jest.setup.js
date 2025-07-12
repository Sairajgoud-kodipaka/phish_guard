// Jest setup file for PhishGuard frontend testing
import '@testing-library/jest-dom'

// Mock Next.js router
jest.mock('next/router', () => ({
  useRouter() {
    return {
      route: '/',
      pathname: '/',
      query: {},
      asPath: '/',
      push: jest.fn(),
      pop: jest.fn(),
      reload: jest.fn(),
      back: jest.fn(),
      prefetch: jest.fn().mockResolvedValue(undefined),
      beforePopState: jest.fn(),
      isFallback: false,
      events: {
        on: jest.fn(),
        off: jest.fn(),
        emit: jest.fn(),
      },
    }
  },
}))

// Mock Next.js navigation
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
      back: jest.fn(),
      forward: jest.fn(),
      refresh: jest.fn(),
    }
  },
  useSearchParams() {
    return {
      get: jest.fn(),
    }
  },
  usePathname() {
    return '/'
  },
}))

// Mock environment variables
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000'

// Global test utilities
global.mockUser = {
  id: 1,
  email: 'admin@phishguard.com',
  username: 'admin',
  full_name: 'Admin User',
  role: 'admin',
  is_superuser: true,
  organization_id: 1,
}

global.mockEmail = {
  id: 1,
  subject: 'Test Email Subject',
  sender_email: 'test@example.com',
  recipient_email: 'user@company.com',
  threat_level: 'medium',
  threat_score: 0.75,
  date_received: '2024-01-15T10:30:00Z',
  is_phishing: true,
  quarantined: false,
}

global.mockThreat = {
  id: 1,
  threat_type: 'phishing',
  severity: 'high',
  title: 'Credential Theft Attempt',
  confidence_score: 0.9,
  status: 'detected',
  email_id: 1,
  created_at: '2024-01-15T10:30:00Z',
}

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
})

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
}

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
}

// Mock fetch if not available
if (!global.fetch) {
  global.fetch = jest.fn()
}

// Console error suppression for known warnings
const originalError = console.error
beforeAll(() => {
  console.error = (...args) => {
    if (
      typeof args[0] === 'string' &&
      args[0].includes('Warning: ReactDOM.render is no longer supported')
    ) {
      return
    }
    originalError.call(console, ...args)
  }
})

afterAll(() => {
  console.error = originalError
}) 