'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  XMarkIcon,
  ExclamationTriangleIcon,
  ShieldCheckIcon,
  ClockIcon,
  EnvelopeIcon,
  DocumentIcon,
  LinkIcon,
  UserIcon,
  ServerIcon,
  ChartBarIcon,
  CogIcon,
  EyeIcon,
  EyeSlashIcon,
} from '@heroicons/react/24/outline'
import { formatDate, formatThreatLevel, cn } from '@/lib/utils'

// Enhanced email interface with AI/ML analysis details
interface EmailPreviewData {
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
  
  // AI/ML Analysis Details
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

interface EmailPreviewModalProps {
  email: EmailPreviewData | null
  isOpen: boolean
  onClose: () => void
}

export function EmailPreviewModal({ email, isOpen, onClose }: EmailPreviewModalProps) {
  const [showSensitiveInfo, setShowSensitiveInfo] = useState(false)
  const [activeTab, setActiveTab] = useState<'overview' | 'analysis' | 'patterns' | 'threats' | 'technical'>('overview')

  if (!isOpen || !email) return null

  const threatInfo = formatThreatLevel(email.threatScore)
  const confidenceColor = email.confidence > 80 ? 'text-green-600' : email.confidence > 60 ? 'text-yellow-600' : 'text-red-600'

  const tabs = [
    { id: 'overview', label: 'Overview', icon: EyeIcon },
    { id: 'analysis', label: 'AI Analysis', icon: ChartBarIcon },
    { id: 'patterns', label: 'Patterns', icon: CogIcon },
    { id: 'threats', label: 'Threats', icon: ExclamationTriangleIcon },
    { id: 'technical', label: 'Technical', icon: ServerIcon },
  ]

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className={`p-2 rounded-full ${threatInfo.bgColor}`}>
              {email.threatScore > 70 ? (
                <ExclamationTriangleIcon className={`h-6 w-6 ${threatInfo.color}`} />
              ) : (
                <ShieldCheckIcon className={`h-6 w-6 ${threatInfo.color}`} />
              )}
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900">Email Analysis Details</h2>
              <p className="text-sm text-gray-500">ID: {email.id} • {formatDate(email.receivedAt)}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowSensitiveInfo(!showSensitiveInfo)}
            >
              {showSensitiveInfo ? (
                <EyeSlashIcon className="h-4 w-4 mr-2" />
              ) : (
                <EyeIcon className="h-4 w-4 mr-2" />
              )}
              {showSensitiveInfo ? 'Hide' : 'Show'} Sensitive
            </Button>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <XMarkIcon className="h-5 w-5" />
            </Button>
          </div>
        </div>

        {/* Threat Score Banner */}
        <div className={`p-4 ${threatInfo.bgColor} border-b ${threatInfo.borderColor}`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="text-center">
                <div className={`text-3xl font-bold ${threatInfo.color}`}>
                  {email.threatScore}%
                </div>
                <div className={`text-sm font-medium ${threatInfo.color}`}>
                  {threatInfo.label} Risk
                </div>
              </div>
              <div className="text-center">
                <div className={`text-2xl font-bold ${confidenceColor}`}>
                  {email.confidence}%
                </div>
                <div className="text-sm text-gray-600">Confidence</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-700">
                  {email.processingTime}s
                </div>
                <div className="text-sm text-gray-600">Processing</div>
              </div>
            </div>
            <div className="text-right">
              <Badge variant={email.actionTaken === 'block' ? 'destructive' : email.actionTaken === 'quarantine' ? 'warning' : 'success'}>
                {email.actionTaken?.toUpperCase() || 'UNKNOWN'}
              </Badge>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-gray-200 bg-gray-50">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={cn(
                'flex items-center space-x-2 px-6 py-3 text-sm font-medium transition-colors',
                activeTab === tab.id
                  ? 'text-primary-600 border-b-2 border-primary-600 bg-white'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
              )}
            >
              <tab.icon className="h-4 w-4" />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Email Basic Info */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <EnvelopeIcon className="h-5 w-5" />
                    <span>Email Information</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-700">From</label>
                      <p className="text-sm text-gray-900 mt-1">{email.from}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-700">To</label>
                      <p className="text-sm text-gray-900 mt-1">{email.to || 'Not specified'}</p>
                    </div>
                    <div className="md:col-span-2">
                      <label className="text-sm font-medium text-gray-700">Subject</label>
                      <p className="text-sm text-gray-900 mt-1 font-medium">{email.subject}</p>
                    </div>
                    <div className="md:col-span-2">
                      <label className="text-sm font-medium text-gray-700">Content</label>
                      <div className="mt-1 p-3 bg-gray-50 rounded-md max-h-32 overflow-y-auto">
                        <p className="text-sm text-gray-900 whitespace-pre-wrap">
                          {showSensitiveInfo ? email.body : email.body.substring(0, 200) + '...'}
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Quick Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Card>
                  <CardContent className="pt-4 text-center">
                    <div className="text-2xl font-bold text-blue-600">{email.analysis.nlpScore}%</div>
                    <div className="text-sm text-gray-600">NLP Score</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-4 text-center">
                    <div className="text-2xl font-bold text-purple-600">{email.analysis.urlScore}%</div>
                    <div className="text-sm text-gray-600">URL Score</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-4 text-center">
                    <div className="text-2xl font-bold text-orange-600">{email.analysis.headerScore}%</div>
                    <div className="text-sm text-gray-600">Header Score</div>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-4 text-center">
                    <div className="text-2xl font-bold text-red-600">{email.analysis.anomalyScore}%</div>
                    <div className="text-sm text-gray-600">Anomaly Score</div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {activeTab === 'analysis' && (
            <div className="space-y-6">
              {/* ML Model Info */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <CogIcon className="h-5 w-5" />
                    <span>Machine Learning Model</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-700">Model Name</label>
                      <p className="text-sm text-gray-900 mt-1">{email.analysis.mlModel.name}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-700">Version</label>
                      <p className="text-sm text-gray-900 mt-1">{email.analysis.mlModel.version}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-700">Accuracy</label>
                      <p className="text-sm text-gray-900 mt-1">{email.analysis.mlModel.accuracy}%</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-700">Last Updated</label>
                      <p className="text-sm text-gray-900 mt-1">{email.analysis.mlModel.lastUpdated}</p>
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Features Used</label>
                    <div className="mt-1 flex flex-wrap gap-2">
                      {email.analysis.mlModel.features.map((feature, index) => (
                        <Badge key={index} variant="outline">{feature}</Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Score Breakdown */}
              <Card>
                <CardHeader>
                  <CardTitle>Score Breakdown</CardTitle>
                  <CardDescription>Detailed analysis scores from different AI models</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {[
                    { label: 'Natural Language Processing', score: email.analysis.nlpScore, color: 'blue' },
                    { label: 'URL Analysis', score: email.analysis.urlScore, color: 'purple' },
                    { label: 'Header Analysis', score: email.analysis.headerScore, color: 'orange' },
                    { label: 'Anomaly Detection', score: email.analysis.anomalyScore, color: 'red' },
                  ].map((item, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="font-medium text-gray-700">{item.label}</span>
                        <span className="font-bold text-gray-900">{item.score}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full bg-${item.color}-500`}
                          style={{ width: `${item.score}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'patterns' && (
            <div className="space-y-6">
              {/* Suspicious Keywords */}
              <Card>
                <CardHeader>
                  <CardTitle>Suspicious Keywords Detected</CardTitle>
                  <CardDescription>AI-identified suspicious language patterns</CardDescription>
                </CardHeader>
                <CardContent>
                  {email.analysis.patterns.suspiciousKeywords.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                      {email.analysis.patterns.suspiciousKeywords.map((keyword, index) => (
                        <Badge key={index} variant="destructive">{keyword}</Badge>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500">No suspicious keywords detected</p>
                  )}
                </CardContent>
              </Card>

              {/* URL Analysis */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <LinkIcon className="h-5 w-5" />
                    <span>URL Analysis</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {email.analysis.patterns.urls.length > 0 ? (
                    <div className="space-y-3">
                      {email.analysis.patterns.urls.map((url, index) => (
                        <div key={index} className="p-3 border rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-900 truncate">{url.url}</span>
                            <Badge variant={url.risk === 'critical' ? 'destructive' : url.risk === 'high' ? 'destructive' : url.risk === 'medium' ? 'warning' : 'success'}>
                              {url.risk.toUpperCase()}
                            </Badge>
                          </div>
                          <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                            <span>Category: {url.category}</span>
                            <span>Reputation: {url.reputation}/100</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500">No URLs found in email</p>
                  )}
                </CardContent>
              </Card>

              {/* Content Analysis */}
              <Card>
                <CardHeader>
                  <CardTitle>Content Analysis</CardTitle>
                  <CardDescription>AI-detected content patterns and indicators</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div className="text-center p-3 border rounded-lg">
                      <div className="text-lg font-bold text-gray-900">{email.analysis.patterns.contentAnalysis.sentiment}</div>
                      <div className="text-xs text-gray-600">Sentiment</div>
                    </div>
                    <div className="text-center p-3 border rounded-lg">
                      <div className="text-lg font-bold text-gray-900">{email.analysis.patterns.contentAnalysis.urgency}</div>
                      <div className="text-xs text-gray-600">Urgency Level</div>
                    </div>
                    <div className="text-center p-3 border rounded-lg">
                      <div className="text-lg font-bold text-gray-900">{email.analysis.patterns.contentAnalysis.impersonation ? 'Yes' : 'No'}</div>
                      <div className="text-xs text-gray-600">Impersonation</div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="font-medium text-gray-700">Social Engineering Indicators:</h4>
                    <div className="flex flex-wrap gap-2">
                      {[
                        { label: 'Social Engineering', value: email.analysis.patterns.contentAnalysis.socialEngineering },
                        { label: 'Financial Pressure', value: email.analysis.patterns.contentAnalysis.financialPressure },
                        { label: 'Authority Pressure', value: email.analysis.patterns.contentAnalysis.authorityPressure },
                      ].map((indicator, index) => (
                        <Badge key={index} variant={indicator.value ? 'destructive' : 'outline'}>
                          {indicator.label}: {indicator.value ? 'Yes' : 'No'}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'threats' && (
            <div className="space-y-6">
              {/* Threat Details */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <ExclamationTriangleIcon className="h-5 w-5" />
                    <span>Detected Threats</span>
                  </CardTitle>
                  <CardDescription>AI-identified security threats and their details</CardDescription>
                </CardHeader>
                <CardContent>
                  {email.analysis.threats.length > 0 ? (
                    <div className="space-y-4">
                      {email.analysis.threats.map((threat, index) => (
                        <div key={index} className="p-4 border rounded-lg">
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center space-x-2">
                              <Badge variant={threat.severity === 'critical' ? 'destructive' : threat.severity === 'high' ? 'destructive' : threat.severity === 'medium' ? 'warning' : 'success'}>
                                {threat.severity.toUpperCase()}
                              </Badge>
                              <span className="font-medium text-gray-900">{threat.type}</span>
                            </div>
                            <div className="text-right">
                              <div className="text-lg font-bold text-gray-900">{threat.score}%</div>
                              <div className="text-sm text-gray-600">Confidence: {threat.confidence}%</div>
                            </div>
                          </div>
                          <p className="text-sm text-gray-700 mb-3">{threat.description}</p>
                          <div>
                            <h5 className="text-sm font-medium text-gray-700 mb-2">Indicators:</h5>
                            <div className="flex flex-wrap gap-2">
                              {threat.indicators.map((indicator, idx) => (
                                <Badge key={idx} variant="outline" className="text-xs">{indicator}</Badge>
                              ))}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <ShieldCheckIcon className="h-12 w-12 text-green-500 mx-auto mb-4" />
                      <p className="text-gray-500">No threats detected in this email</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'technical' && (
            <div className="space-y-6">
              {/* Sender Analysis */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <UserIcon className="h-5 w-5" />
                    <span>Sender Analysis</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div className="text-center p-3 border rounded-lg">
                      <div className="text-lg font-bold text-gray-900">{email.analysis.patterns.senderAnalysis.reputation}/100</div>
                      <div className="text-xs text-gray-600">Reputation Score</div>
                    </div>
                    <div className="text-center p-3 border rounded-lg">
                      <div className="text-lg font-bold text-gray-900">{email.analysis.patterns.senderAnalysis.domainAge} days</div>
                      <div className="text-xs text-gray-600">Domain Age</div>
                    </div>
                    <div className="text-center p-3 border rounded-lg">
                      <div className="text-lg font-bold text-gray-900">
                        {email.analysis.patterns.senderAnalysis.spfRecord ? '✅' : '❌'}
                      </div>
                      <div className="text-xs text-gray-600">SPF Record</div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="font-medium text-gray-700">Security Records:</h4>
                    <div className="flex flex-wrap gap-2">
                      {[
                        { label: 'DKIM', value: email.analysis.patterns.senderAnalysis.dkimRecord },
                        { label: 'DMARC', value: email.analysis.patterns.senderAnalysis.dmarcRecord },
                      ].map((record, index) => (
                        <Badge key={index} variant={record.value ? 'success' : 'destructive'}>
                          {record.label}: {record.value ? 'Valid' : 'Missing'}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Attachments Analysis */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <DocumentIcon className="h-5 w-5" />
                    <span>Attachments Analysis</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {email.analysis.patterns.attachments.length > 0 ? (
                    <div className="space-y-3">
                      {email.analysis.patterns.attachments.map((attachment, index) => (
                        <div key={index} className="p-3 border rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              <DocumentIcon className="h-4 w-4 text-gray-400" />
                              <span className="font-medium text-gray-900">{attachment.name}</span>
                            </div>
                            <Badge variant={attachment.risk === 'critical' ? 'destructive' : attachment.risk === 'high' ? 'destructive' : attachment.risk === 'medium' ? 'warning' : 'success'}>
                              {attachment.risk.toUpperCase()}
                            </Badge>
                          </div>
                          <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                            <span>Type: {attachment.type}</span>
                            <span>Size: {(attachment.size / 1024).toFixed(1)} KB</span>
                          </div>
                          <p className="text-sm text-gray-700 mt-2">{attachment.analysis}</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500">No attachments found</p>
                  )}
                </CardContent>
              </Card>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
          <div className="text-sm text-gray-500">
            Analysis completed in {email.processingTime} seconds
          </div>
          <div className="flex space-x-2">
            <Button variant="outline" size="sm">
              Export Report
            </Button>
            <Button variant="outline" size="sm">
              Take Action
            </Button>
            <Button variant="outline" size="sm">
              Mark as Reviewed
            </Button>
            <Button onClick={onClose}>
              Close
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
