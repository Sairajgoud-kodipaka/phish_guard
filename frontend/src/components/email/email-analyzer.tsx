'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { LoadingSpinner } from '@/components/ui/loading-spinner'
import {
  CloudArrowUpIcon,
  DocumentTextIcon,
  ExclamationTriangleIcon,
  ShieldCheckIcon,
  ClockIcon,
} from '@heroicons/react/24/outline'
import { backendApi } from '@/lib/backend-api'

interface EmailAnalysisResult {
  email_id: number
  threat_score: number
  threat_level: string
  is_phishing: boolean
  is_spam: boolean
  is_malware: boolean
  confidence_score: number
  recommended_action: string
  threat_indicators: string[]
  analysis_summary: Record<string, any>
  processing_time: number
}

interface EmailAnalyzerProps {
  onClose: () => void
  onEmailAnalyzed?: () => void
}

export function EmailAnalyzer({ onClose, onEmailAnalyzed }: EmailAnalyzerProps) {
  const [file, setFile] = useState<File | null>(null)
  const [emailText, setEmailText] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState<EmailAnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [showPreview, setShowPreview] = useState(false)
  const [emailPreview, setEmailPreview] = useState<{
    from: string
    to: string
    subject: string
    date: string
    body: string
  } | null>(null)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      setEmailText('')
      setError(null)
    }
  }

  const handleAnalyze = async () => {
    if (!file && !emailText.trim()) {
      setError('Please select a file or paste email content')
      return
    }

    setError(null)
    
    // Parse email content for preview
    let contentToAnalyze = emailText
    if (file) {
      // For file upload, we'll read the file content
      const reader = new FileReader()
      reader.onload = (e) => {
        contentToAnalyze = e.target?.result as string
        showEmailPreview(contentToAnalyze)
      }
      reader.readAsText(file)
    } else {
      showEmailPreview(contentToAnalyze)
    }
  }

  const showEmailPreview = (content: string) => {
    // Parse email headers and content
    const lines = content.split('\n')
    const preview = {
      from: '',
      to: '',
      subject: '',
      date: '',
      body: ''
    }

    let bodyStartIndex = 0
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim()
      if (line.toLowerCase().startsWith('from:')) {
        preview.from = line.substring(5).trim()
      } else if (line.toLowerCase().startsWith('to:')) {
        preview.to = line.substring(3).trim()
      } else if (line.toLowerCase().startsWith('subject:')) {
        preview.subject = line.substring(8).trim()
      } else if (line.toLowerCase().startsWith('date:')) {
        preview.date = line.substring(5).trim()
      } else if (line === '' && i > 0) {
        bodyStartIndex = i + 1
        break
      }
    }

    // Get email body (first 300 characters)
    const bodyLines = lines.slice(bodyStartIndex)
    const fullBody = bodyLines.join('\n').trim()
    preview.body = fullBody.length > 300 ? fullBody.substring(0, 300) + '...' : fullBody

    setEmailPreview(preview)
    setShowPreview(true)
  }

  const handleConfirmAnalysis = async () => {
    setShowPreview(false)
    setAnalyzing(true)
    setResult(null)

    try {
      let analysisResult: EmailAnalysisResult

      if (file) {
        // Analyze uploaded file
        analysisResult = await backendApi.analyzeEmailFile(file) as EmailAnalysisResult
      } else {
        // Analyze pasted email text directly
        analysisResult = await backendApi.analyzeEmail(emailText) as EmailAnalysisResult
      }

      setResult(analysisResult)
      // Notify parent component that email was analyzed
      if (onEmailAnalyzed) {
        onEmailAnalyzed()
      }
    } catch (err) {
      console.error('Email analysis failed:', err)
      setError('Failed to analyze email. Please try again.')
    } finally {
      setAnalyzing(false)
    }
  }

  const getThreatLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical':
        return 'text-red-700 bg-red-100 border-red-200'
      case 'high':
        return 'text-orange-700 bg-orange-100 border-orange-200'
      case 'medium':
        return 'text-yellow-700 bg-yellow-100 border-yellow-200'
      case 'low':
        return 'text-blue-700 bg-blue-100 border-blue-200'
      default:
        return 'text-green-700 bg-green-100 border-green-200'
    }
  }

  const getActionColor = (action: string) => {
    switch (action.toLowerCase()) {
      case 'block':
      case 'quarantine':
        return 'text-red-700 bg-red-100'
      case 'flag':
        return 'text-yellow-700 bg-yellow-100'
      default:
        return 'text-green-700 bg-green-100'
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <Card className="border-0 shadow-none">
          <CardHeader className="border-b">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Analyze Email</CardTitle>
                <CardDescription>
                  Upload an email file or paste email content for AI-powered threat analysis
                </CardDescription>
              </div>
              <Button variant="outline" onClick={onClose}>
                Close
              </Button>
            </div>
          </CardHeader>
          <CardContent className="p-6">
            {!result ? (
              <div className="space-y-6">
                {/* File Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Upload Email File
                  </label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
                    <input
                      type="file"
                      accept=".eml,.msg,.txt"
                      onChange={handleFileChange}
                      className="hidden"
                      id="email-file"
                    />
                    <label htmlFor="email-file" className="cursor-pointer">
                      <CloudArrowUpIcon className="h-12 w-12 text-gray-500 mx-auto mb-4" />
                      <p className="text-sm text-gray-700 font-medium">
                        Click to upload or drag and drop
                      </p>
                      <p className="text-xs text-gray-600">
                        Supports .eml, .msg, and .txt files
                      </p>
                    </label>
                  </div>
                  {file && (
                    <p className="mt-2 text-sm text-gray-800 font-medium bg-green-50 border border-green-200 rounded px-3 py-2">
                      ✓ Selected: {file.name}
                    </p>
                  )}
                </div>

                {/* Text Input */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Or Paste Email Content
                  </label>
                  <div className="mb-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                    <h4 className="font-medium text-blue-900 mb-2">💡 How to use:</h4>
                    <ol className="text-sm text-blue-800 space-y-1">
                      <li>1. Copy the full email content (including headers)</li>
                      <li>2. Paste it in the text area below</li>
                      <li>3. Click "Preview & Analyze Email" to review the content</li>
                      <li>4. Confirm to proceed with AI-powered threat analysis</li>
                    </ol>
                  </div>
                  <textarea
                    value={emailText}
                    onChange={(e) => {
                      setEmailText(e.target.value)
                      if (e.target.value.trim()) {
                        setFile(null)
                      }
                    }}
                    placeholder="Example:
From: suspicious@example.com
To: victim@company.com
Subject: Urgent Account Verification
Date: Mon, 15 Jan 2024 10:00:00 +0000

Dear Customer,
Your account will be suspended unless you verify...
[Paste your complete email content here]"
                    className="w-full h-48 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 placeholder-gray-500 bg-white text-sm"
                  />
                  <div className="mt-2 text-xs text-gray-600">
                    💡 Tip: Include email headers (From, To, Subject, Date) for better analysis
                  </div>
                </div>

                {/* What Will Happen */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h4 className="font-medium text-green-900 mb-2">📊 What you'll get after analysis:</h4>
                  <ul className="text-sm text-green-800 space-y-1">
                    <li>• <strong>Threat Score:</strong> 0-100% risk assessment</li>
                    <li>• <strong>Threat Level:</strong> Clean, Low, Medium, High, or Critical</li>
                    <li>• <strong>Detection Results:</strong> Phishing, Spam, and Malware analysis</li>
                    <li>• <strong>Detailed Breakdown:</strong> URL analysis, sender verification, security tips</li>
                    <li>• <strong>Recommendations:</strong> What action to take with this email</li>
                  </ul>
                </div>

                {error && (
                  <div className="p-3 bg-red-100 border border-red-300 rounded text-sm text-red-700">
                    {error}
                  </div>
                )}

                <Button
                  onClick={handleAnalyze}
                  disabled={analyzing || (!file && !emailText.trim())}
                  className="w-full"
                >
                  {analyzing ? (
                    <>
                      <LoadingSpinner className="h-4 w-4 mr-2" />
                      Analyzing Email...
                    </>
                  ) : (
                    <>
                      <DocumentTextIcon className="h-4 w-4 mr-2" />
                      Preview & Analyze Email
                    </>
                  )}
                </Button>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Analysis Results */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-gray-900">
                      {Math.round(result.threat_score * 100)}%
                    </div>
                    <div className="text-sm text-gray-600">Threat Score</div>
                  </div>
                  <div className="text-center">
                    <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium border ${getThreatLevelColor(result.threat_level)}`}>
                      {result.threat_level.toUpperCase()}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">Threat Level</div>
                  </div>
                  <div className="text-center">
                    <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getActionColor(result.recommended_action)}`}>
                      {result.recommended_action.toUpperCase()}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">Recommended Action</div>
                  </div>
                </div>

                {/* Threat Indicators */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className={`p-4 rounded-lg border ${result.is_phishing ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
                    <div className="flex items-center">
                      {result.is_phishing ? (
                        <ExclamationTriangleIcon className="h-5 w-5 text-red-600 mr-2" />
                      ) : (
                        <ShieldCheckIcon className="h-5 w-5 text-green-600 mr-2" />
                      )}
                      <span className="text-sm font-medium">
                        {result.is_phishing ? 'Phishing Detected' : 'No Phishing'}
                      </span>
                    </div>
                  </div>
                  <div className={`p-4 rounded-lg border ${result.is_spam ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
                    <div className="flex items-center">
                      {result.is_spam ? (
                        <ExclamationTriangleIcon className="h-5 w-5 text-red-600 mr-2" />
                      ) : (
                        <ShieldCheckIcon className="h-5 w-5 text-green-600 mr-2" />
                      )}
                      <span className="text-sm font-medium">
                        {result.is_spam ? 'Spam Detected' : 'Not Spam'}
                      </span>
                    </div>
                  </div>
                  <div className={`p-4 rounded-lg border ${result.is_malware ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
                    <div className="flex items-center">
                      {result.is_malware ? (
                        <ExclamationTriangleIcon className="h-5 w-5 text-red-600 mr-2" />
                      ) : (
                        <ShieldCheckIcon className="h-5 w-5 text-green-600 mr-2" />
                      )}
                      <span className="text-sm font-medium">
                        {result.is_malware ? 'Malware Detected' : 'No Malware'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Threat Indicators */}
                {result.threat_indicators.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Threat Indicators</h4>
                    <div className="bg-gray-50 rounded-lg p-4">
                      <ul className="space-y-1">
                        {result.threat_indicators.map((indicator, index) => (
                          <li key={index} className="text-sm text-gray-700 flex items-start">
                            <span className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                            {indicator}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}

                {/* Analysis Details */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Analysis Details</h4>
                    <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-700">
                      <div className="flex justify-between mb-2">
                        <span>Confidence Score:</span>
                        <span>{Math.round(result.confidence_score * 100)}%</span>
                      </div>
                      <div className="flex justify-between mb-2">
                        <span>Processing Time:</span>
                        <span>{result.processing_time.toFixed(2)}s</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Email ID:</span>
                        <span>{result.email_id}</span>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Recommended Actions</h4>
                    <div className="bg-gray-50 rounded-lg p-4">
                      <ul className="space-y-1 text-sm text-gray-700">
                        {result.recommended_action === 'quarantine' && (
                          <li>• Move email to quarantine folder</li>
                        )}
                        {result.recommended_action === 'block' && (
                          <li>• Block sender permanently</li>
                        )}
                        {result.recommended_action === 'flag' && (
                          <li>• Flag for manual review</li>
                        )}
                        <li>• Review threat indicators</li>
                        <li>• Update security policies if needed</li>
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Enhanced Analysis Summary */}
                {result.analysis_summary && Object.keys(result.analysis_summary).length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Detailed Analysis Summary</h4>
                    <div className="bg-gray-50 rounded-lg p-4 space-y-3">
                      {result.analysis_summary.url_analysis && (
                        <div>
                          <h5 className="font-medium text-gray-800 text-sm mb-1">URL Analysis</h5>
                          <div className="text-sm text-gray-600 space-y-1">
                            <div className="flex justify-between">
                              <span>URLs Found:</span>
                              <span>{result.analysis_summary.url_analysis.total_urls || 0}</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Suspicious URLs:</span>
                              <span className="text-red-600">{result.analysis_summary.url_analysis.suspicious_urls || 0}</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Malicious Domains:</span>
                              <span className="text-red-600">{result.analysis_summary.url_analysis.malicious_domains || 0}</span>
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {result.analysis_summary.attachment_analysis && (
                        <div>
                          <h5 className="font-medium text-gray-800 text-sm mb-1">Attachment Analysis</h5>
                          <div className="text-sm text-gray-600 space-y-1">
                            <div className="flex justify-between">
                              <span>Attachments Found:</span>
                              <span>{result.analysis_summary.attachment_analysis.total_attachments || 0}</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Dangerous Types:</span>
                              <span className="text-red-600">{result.analysis_summary.attachment_analysis.dangerous_types || 0}</span>
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {result.analysis_summary.sender_analysis && (
                        <div>
                          <h5 className="font-medium text-gray-800 text-sm mb-1">Sender Analysis</h5>
                          <div className="text-sm text-gray-600 space-y-1">
                            <div className="flex justify-between">
                              <span>SPF Status:</span>
                              <span className={result.analysis_summary.sender_analysis.spf_valid ? 'text-green-600' : 'text-red-600'}>
                                {result.analysis_summary.sender_analysis.spf_valid ? 'Valid' : 'Invalid/Missing'}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>DKIM Status:</span>
                              <span className={result.analysis_summary.sender_analysis.dkim_valid ? 'text-green-600' : 'text-red-600'}>
                                {result.analysis_summary.sender_analysis.dkim_valid ? 'Valid' : 'Invalid/Missing'}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span>Domain Reputation:</span>
                              <span className={result.analysis_summary.sender_analysis.domain_reputation === 'good' ? 'text-green-600' : 'text-red-600'}>
                                {result.analysis_summary.sender_analysis.domain_reputation || 'Unknown'}
                              </span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Threat Explanation */}
                {result.threat_level !== 'clean' && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Why This Email is Flagged</h4>
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                      <div className="text-sm text-gray-700 space-y-2">
                        {result.is_phishing && (
                          <div>
                            <span className="font-medium text-red-700">Phishing Risk:</span>
                            <span className="ml-2">This email appears to be attempting to steal personal information or credentials through deceptive content.</span>
                          </div>
                        )}
                        {result.is_spam && (
                          <div>
                            <span className="font-medium text-orange-700">Spam Risk:</span>
                            <span className="ml-2">This email contains characteristics typical of unsolicited bulk messages.</span>
                          </div>
                        )}
                        {result.is_malware && (
                          <div>
                            <span className="font-medium text-red-700">Malware Risk:</span>
                            <span className="ml-2">This email may contain malicious software or links to infected websites.</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Security Tips */}
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Security Tips</h4>
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <ul className="text-sm text-gray-700 space-y-1">
                      <li>• Never click links in suspicious emails</li>
                      <li>• Verify sender identity through separate communication</li>
                      <li>• Be cautious of urgent requests for personal information</li>
                      <li>• Report suspicious emails to your IT security team</li>
                      <li>• Keep your email client and security software updated</li>
                    </ul>
                  </div>
                </div>

                <div className="flex space-x-3">
                  <Button
                    onClick={() => {
                      setResult(null)
                      setFile(null)
                      setEmailText('')
                      setError(null)
                    }}
                    variant="outline"
                  >
                    Analyze Another
                  </Button>
                  <Button onClick={onClose}>
                    Close
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
      
      {/* Email Preview Dialog */}
      {showPreview && emailPreview && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-[60]">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="border-b p-4">
              <h3 className="text-lg font-semibold text-gray-900">Email Preview</h3>
              <p className="text-sm text-gray-600 mt-1">Review the email content before analysis</p>
            </div>
            
            <div className="p-6 space-y-4">
              {/* Email Headers */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-3">Email Headers</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex">
                    <span className="font-medium text-gray-700 w-16">From:</span>
                    <span className="text-gray-900">{emailPreview.from || 'Not specified'}</span>
                  </div>
                  <div className="flex">
                    <span className="font-medium text-gray-700 w-16">To:</span>
                    <span className="text-gray-900">{emailPreview.to || 'Not specified'}</span>
                  </div>
                  <div className="flex">
                    <span className="font-medium text-gray-700 w-16">Subject:</span>
                    <span className="text-gray-900">{emailPreview.subject || 'No subject'}</span>
                  </div>
                  <div className="flex">
                    <span className="font-medium text-gray-700 w-16">Date:</span>
                    <span className="text-gray-900">{emailPreview.date || 'Not specified'}</span>
                  </div>
                </div>
              </div>
              
              {/* Email Body Preview */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-3">Email Content Preview</h4>
                <div className="text-sm text-gray-700 whitespace-pre-wrap bg-white p-3 rounded border max-h-40 overflow-y-auto">
                  {emailPreview.body || 'No content available'}
                </div>
              </div>
            </div>
            
            <div className="border-t p-4 flex justify-end space-x-3">
              <Button 
                variant="outline" 
                onClick={() => setShowPreview(false)}
              >
                Cancel
              </Button>
              <Button 
                onClick={handleConfirmAnalysis}
                className="bg-blue-600 hover:bg-blue-700"
              >
                Proceed with Analysis
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 