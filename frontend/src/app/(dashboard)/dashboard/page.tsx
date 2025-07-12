'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  ShieldCheckIcon,
  ExclamationTriangleIcon,
  EnvelopeIcon,
  ClockIcon,
} from '@heroicons/react/24/outline'
import { backendApi } from '@/lib/backend-api'
import { DashboardStats } from '@/types'
import { EmailAnalyzer } from '@/components/email/email-analyzer'

interface AnalyzedEmail {
  id: number
  subject: string
  sender_email: string
  threat_score: number
  threat_level: string
  is_phishing: boolean
  is_spam: boolean
  is_malware: boolean
  action_taken: string
  created_at: string
  processing_time?: number
}

export default function DashboardPage() {
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null)
  const [recentEmails, setRecentEmails] = useState<AnalyzedEmail[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showEmailAnalyzer, setShowEmailAnalyzer] = useState(false)

  // Load dashboard data
  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    setLoading(true)
    setError(null)

    try {
      // Fetch real data from backend
      const [emailStats, recentEmailsData] = await Promise.all([
        backendApi.getEmailStats(30),
        backendApi.getRecentEmails(10, 30)
      ])

      // Convert email stats to dashboard stats format
      const statsData = emailStats as any
      const threatDist = statsData.threat_distribution || {}
      const actionDist = statsData.action_distribution || {}
      
      const threatsDetected = (threatDist.high || 0) + (threatDist.critical || 0) + (threatDist.medium || 0)
      const blockedEmails = actionDist.quarantine || 0
      const quarantinedEmails = actionDist.quarantine || 0
      const falsePositives = 0 // Would need separate query for false positives
      const cleanEmails = (threatDist.clean || 0) + (threatDist.low || 0)
      const totalProcessed = statsData.total_emails || 0
      const accuracyRate = totalProcessed > 0 ? ((cleanEmails + threatsDetected) / totalProcessed) * 100 : 0
      
      const stats: DashboardStats = {
        total_emails: totalProcessed,
        emails_processed: totalProcessed,
        threats_detected: threatsDetected,
        blocked_emails: blockedEmails,
        quarantined_emails: quarantinedEmails,
        accuracy_percentage: accuracyRate,
        false_positives: falsePositives,
        period_days: 30
      }

      setDashboardStats(stats)
      setRecentEmails((recentEmailsData as AnalyzedEmail[]) || [])
    } catch (err) {
      console.error('Failed to load dashboard data:', err)
      setError('Failed to connect to backend. Please ensure the backend server is running.')
      // Set demo data as fallback
      setDashboardStats({
        total_emails: 0,
        emails_processed: 0,
        threats_detected: 0,
        blocked_emails: 0,
        quarantined_emails: 0,
        accuracy_percentage: 0,
        false_positives: 0,
        period_days: 30
      })
      setRecentEmails([])
    } finally {
      setLoading(false)
    }
  }

  const handleEmailAnalyzed = () => {
    // Refresh dashboard data after email analysis
    loadDashboardData()
  }

  const formatThreatLevel = (level: string, score: number) => {
    switch (level.toLowerCase()) {
      case 'critical':
        return { label: 'Critical', color: 'text-red-700', bgColor: 'bg-red-100', borderColor: 'border-red-300' }
      case 'high':
        return { label: 'High', color: 'text-red-600', bgColor: 'bg-red-50', borderColor: 'border-red-200' }
      case 'medium':
        return { label: 'Medium', color: 'text-yellow-600', bgColor: 'bg-yellow-50', borderColor: 'border-yellow-200' }
      case 'low':
        return { label: 'Low', color: 'text-blue-600', bgColor: 'bg-blue-50', borderColor: 'border-blue-200' }
      default:
        return { label: 'Clean', color: 'text-green-600', bgColor: 'bg-green-50', borderColor: 'border-green-200' }
    }
  }

  const getActionColor = (action: string) => {
    switch (action.toLowerCase()) {
      case 'block':
        return 'text-red-600 font-medium'
      case 'quarantine':
        return 'text-yellow-600 font-medium'
      case 'allow':
        return 'text-green-600 font-medium'
      default:
        return 'text-gray-600'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg text-gray-600">Loading dashboard data...</div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8 p-6">
      {error && (
        <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800 text-center">
          {error}
        </div>
      )}

      {/* Main Email Analysis Section */}
      <Card className="border-2 border-primary-200 bg-gradient-to-br from-primary-50 to-white">
        <CardHeader className="text-center pb-6">
          <CardTitle className="text-3xl font-bold text-gray-900">Email Security Analysis</CardTitle>
          <CardDescription className="text-lg text-gray-600">
            Upload an email file or paste email content for AI-powered threat detection
          </CardDescription>
        </CardHeader>
        <CardContent className="flex justify-center pb-8">
          <Button 
            size="lg"
            className="h-16 px-12 text-lg"
            onClick={() => setShowEmailAnalyzer(true)}
          >
            <EnvelopeIcon className="h-6 w-6 mr-3" />
            Analyze Email
          </Button>
        </CardContent>
      </Card>

      {/* Real Stats */}
      {dashboardStats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="text-center">
            <CardContent className="pt-6">
              <div className="text-3xl font-bold text-gray-900 mb-1">
                {dashboardStats.total_emails.toLocaleString()}
              </div>
              <div className="text-sm text-gray-600">Emails Analyzed</div>
            </CardContent>
          </Card>
          
          <Card className="text-center">
            <CardContent className="pt-6">
              <div className="text-3xl font-bold text-red-600 mb-1">
                {dashboardStats.threats_detected}
              </div>
              <div className="text-sm text-gray-600">Threats Detected</div>
            </CardContent>
          </Card>
          
          <Card className="text-center">
            <CardContent className="pt-6">
              <div className="text-3xl font-bold text-green-600 mb-1">
                {dashboardStats.accuracy_percentage.toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600">Accuracy Rate</div>
            </CardContent>
          </Card>
          
          <Card className="text-center">
            <CardContent className="pt-6">
              <div className="text-3xl font-bold text-yellow-600 mb-1">
                {dashboardStats.false_positives}
              </div>
              <div className="text-sm text-gray-600">False Positives</div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Recent Analyzed Emails - Real Data */}
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">Recently Analyzed Emails</CardTitle>
          <CardDescription>
            {recentEmails.length > 0 
              ? `Latest emails processed by AI analysis` 
              : 'No emails analyzed yet. Upload an email to get started!'
            }
          </CardDescription>
        </CardHeader>
        <CardContent>
          {recentEmails.length > 0 ? (
            <div className="space-y-4">
              {recentEmails.slice(0, 5).map((email) => {
                const threatInfo = formatThreatLevel(email.threat_level, email.threat_score)
                const threatScore = Math.round(email.threat_score * 100)
                
                return (
                  <div 
                    key={email.id} 
                    className={`flex items-center justify-between p-4 rounded-lg border ${threatInfo.bgColor} ${threatInfo.borderColor}`}
                  >
                    <div className="flex items-center space-x-3">
                      {email.threat_level === 'clean' || email.threat_level === 'low' ? (
                        <ShieldCheckIcon className="h-5 w-5 text-green-500" />
                      ) : (
                        <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
                      )}
                      <div>
                        <div className="font-medium text-gray-900">
                          {email.subject || 'No Subject'}
                        </div>
                        <div className="text-sm text-gray-600">
                          {email.sender_email}
                        </div>
                        <div className="flex items-center text-xs text-gray-500 mt-1">
                          <ClockIcon className="h-3 w-3 mr-1" />
                          {new Date(email.created_at).toLocaleString()}
                          {email.processing_time && (
                            <span className="ml-2">• {email.processing_time.toFixed(2)}s</span>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`text-2xl font-bold ${threatInfo.color}`}>
                        {threatScore}%
                      </div>
                      <div className={`text-xs font-medium uppercase ${getActionColor(email.action_taken)}`}>
                        {email.action_taken}
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <EnvelopeIcon className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>No emails analyzed yet.</p>
              <p className="text-sm">Upload an email above to see analysis results here!</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Email Analyzer Modal */}
      {showEmailAnalyzer && (
        <EmailAnalyzer 
          onClose={() => setShowEmailAnalyzer(false)}
          onEmailAnalyzed={handleEmailAnalyzed}
        />
      )}
    </div>
  )
} 