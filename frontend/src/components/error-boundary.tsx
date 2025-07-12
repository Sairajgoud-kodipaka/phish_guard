'use client'

import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'

interface ErrorBoundaryState {
  hasError: boolean
  error?: Error
  errorInfo?: React.ErrorInfo
}

interface ErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ComponentType<{ error: Error; retry: () => void }>
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      hasError: true,
      error,
    }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    this.setState({
      error,
      errorInfo,
    })

    // Log error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('ErrorBoundary caught an error:', error, errorInfo)
    }

    // In production, you would send this to your error reporting service
    // Example: logErrorToService(error, errorInfo)
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined })
  }

  render() {
    if (this.state.hasError) {
      const { fallback: Fallback } = this.props
      
      if (Fallback && this.state.error) {
        return <Fallback error={this.state.error} retry={this.handleRetry} />
      }

      return <DefaultErrorFallback error={this.state.error} retry={this.handleRetry} />
    }

    return this.props.children
  }
}

interface ErrorFallbackProps {
  error?: Error
  retry: () => void
}

export function DefaultErrorFallback({ error, retry }: ErrorFallbackProps) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-danger-100 mb-4">
            <ExclamationTriangleIcon className="h-6 w-6 text-danger-600" />
          </div>
          <CardTitle className="text-xl text-gray-900">Something went wrong</CardTitle>
          <CardDescription>
            An unexpected error occurred. Please try again or contact support if the problem persists.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {process.env.NODE_ENV === 'development' && error && (
            <div className="bg-gray-100 p-3 rounded-md">
              <p className="text-sm font-medium text-gray-700 mb-2">Error Details:</p>
              <pre className="text-xs text-gray-600 whitespace-pre-wrap break-words">
                {error.message}
              </pre>
            </div>
          )}
          <div className="flex space-x-3">
            <Button variant="outline" className="flex-1" onClick={() => window.location.reload()}>
              Refresh Page
            </Button>
            <Button className="flex-1" onClick={retry}>
              Try Again
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// Component-level error boundary for specific sections
export function SectionErrorBoundary({ children }: { children: React.ReactNode }) {
  return (
    <ErrorBoundary fallback={SectionErrorFallback}>
      {children}
    </ErrorBoundary>
  )
}

function SectionErrorFallback({ error, retry }: ErrorFallbackProps) {
  return (
    <Card className="border-danger-200 bg-danger-50">
      <CardContent className="p-6">
        <div className="flex items-center space-x-3">
          <ExclamationTriangleIcon className="h-5 w-5 text-danger-600" />
          <div className="flex-1">
            <h3 className="text-sm font-medium text-danger-800">
              Error loading this section
            </h3>
            <p className="text-sm text-danger-700 mt-1">
              {error?.message || 'An unexpected error occurred'}
            </p>
          </div>
          <Button size="sm" variant="outline" onClick={retry}>
            Retry
          </Button>
        </div>
      </CardContent>
    </Card>
  )
} 