

'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  MagnifyingGlassIcon,
  FunnelIcon,
  ExclamationTriangleIcon,
  ShieldCheckIcon,
  ClockIcon,
  EnvelopeIcon,
  EyeIcon,
} from '@heroicons/react/24/outline'
import { formatDate, formatThreatLevel, cn } from '@/lib/utils'

// Types
type EmailStatus = 'delivered' | 'quarantined' | 'blocked'
type ThreatType = 'Phishing' | 'Malware' | 'Credential Harvesting' | 'Social Engineering' | null

interface Email {
  id: number
  from: string
  subject: string
  body: string
  receivedAt: Date
  threatLevel: number
  threatType: ThreatType
  status: EmailStatus
  attachments: number
}

// Mock email data
const emails: Email[] = [
  {
    id: 1,
    from: 'urgent-payment@fake-bank.com',
    subject: 'URGENT: Verify Your Account Immediately',
    body: 'Your account will be suspended unless you verify...',
    receivedAt: new Date(Date.now() - 5 * 60 * 1000), // 5 minutes ago
    threatLevel: 89,
    threatType: 'Phishing',
    status: 'blocked',
    attachments: 0,
  },
  {
    id: 2,
    from: 'invoice@legitimate-company.com',
    subject: 'Monthly Invoice - December 2024',
    body: 'Please find attached your monthly invoice...',
    receivedAt: new Date(Date.now() - 15 * 60 * 1000), // 15 minutes ago
    threatLevel: 12,
    threatType: null,
    status: 'delivered',
    attachments: 1,
  },
  {
    id: 3,
    from: 'security-alert@malware-site.org',
    subject: 'Security Alert: Suspicious Activity Detected',
    body: 'Click here to secure your account...',
    receivedAt: new Date(Date.now() - 60 * 60 * 1000), // 1 hour ago
    threatLevel: 94,
    threatType: 'Malware',
    status: 'quarantined',
    attachments: 2,
  },
  {
    id: 4,
    from: 'newsletter@trusted-source.com',
    subject: 'Weekly Security Newsletter',
    body: 'This week in cybersecurity...',
    receivedAt: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
    threatLevel: 5,
    threatType: null,
    status: 'delivered',
    attachments: 0,
  },
  {
    id: 5,
    from: 'document-shared@credential-harvest.com',
    subject: 'Shared Document: Q4 Financial Report.pdf',
    body: 'A document has been shared with you...',
    receivedAt: new Date(Date.now() - 3 * 60 * 60 * 1000), // 3 hours ago
    threatLevel: 82,
    threatType: 'Credential Harvesting',
    status: 'blocked',
    attachments: 1,
  },
]

const statusColors: Record<EmailStatus, 'success' | 'warning' | 'destructive'> = {
  delivered: 'success',
  quarantined: 'warning',
  blocked: 'destructive',
}

const threatTypeColors: Record<string, 'destructive' | 'warning'> = {
  'Phishing': 'destructive',
  'Malware': 'destructive',
  'Credential Harvesting': 'warning',
  'Social Engineering': 'warning',
}

interface EmailListProps {
  className?: string
}

export function EmailList({ className }: EmailListProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [selectedEmail, setSelectedEmail] = useState<number | null>(null)

  const filteredEmails = emails.filter((email) => {
    const matchesSearch = 
      email.from.toLowerCase().includes(searchTerm.toLowerCase()) ||
      email.subject.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesFilter = 
      filterStatus === 'all' || 
      email.status === filterStatus
    
    return matchesSearch && matchesFilter
  })

  return (
    <div className={cn('space-y-6', className)}>
      {/* Header and Controls */}
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Email Analysis</h2>
          <p className="text-gray-500 mt-1">
            Monitor and analyze email threats in real-time
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="relative">
            <MagnifyingGlassIcon className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <Input
              placeholder="Search emails..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-64"
            />
          </div>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="h-10 px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="all">All Status</option>
            <option value="delivered">Delivered</option>
            <option value="quarantined">Quarantined</option>
            <option value="blocked">Blocked</option>
          </select>
        </div>
      </div>

      {/* Email List */}
      <Card>
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">
              Emails ({filteredEmails.length})
            </CardTitle>
            <Button variant="outline" size="sm">
              <FunnelIcon className="h-4 w-4 mr-2" />
              Advanced Filters
            </Button>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-gray-200">
            {filteredEmails.map((email) => {
              const threatLevel = formatThreatLevel(email.threatLevel)
              const isSelected = selectedEmail === email.id
              
              return (
                <div
                  key={email.id}
                  className={cn(
                    'p-6 hover:bg-gray-50 cursor-pointer transition-colors',
                    isSelected && 'bg-primary-50 border-l-4 border-primary-500'
                  )}
                  onClick={() => setSelectedEmail(isSelected ? null : email.id)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      {/* Header Row */}
                      <div className="flex items-center space-x-3 mb-2">
                        <Badge variant={statusColors[email.status] as 'success' | 'warning' | 'destructive'}>
                          {email.status}
                        </Badge>
                        {email.threatType && (
                          <Badge variant={(threatTypeColors[email.threatType] || 'warning') as 'destructive' | 'warning'}>
                            {email.threatType}
                          </Badge>
                        )}
                        <div className={`px-2 py-1 rounded-full text-xs font-medium ${threatLevel.bgColor} ${threatLevel.color}`}>
                          Risk: {email.threatLevel}%
                        </div>
                      </div>

                      {/* Email Details */}
                      <div className="space-y-1">
                        <div className="flex items-center space-x-2">
                          <EnvelopeIcon className="h-4 w-4 text-gray-400 flex-shrink-0" />
                          <span className="text-sm font-medium text-gray-900 truncate">
                            {email.from}
                          </span>
                        </div>
                        <h3 className="text-base font-semibold text-gray-900 truncate">
                          {email.subject}
                        </h3>
                        <p className="text-sm text-gray-600 line-clamp-2">
                          {email.body}
                        </p>
                      </div>

                      {/* Footer Row */}
                      <div className="flex items-center justify-between mt-3 text-xs text-gray-500">
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center">
                            <ClockIcon className="h-3 w-3 mr-1" />
                            {formatDate(email.receivedAt)}
                          </div>
                          {email.attachments > 0 && (
                            <div className="flex items-center">
                              📎 {email.attachments} attachment{email.attachments > 1 ? 's' : ''}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Threat Level Indicator */}
                    <div className="flex flex-col items-end space-y-2 ml-4">
                      <div className="text-right">
                        <div className="text-lg font-bold text-gray-900">
                          {email.threatLevel}%
                        </div>
                        <div className={`text-xs font-medium ${threatLevel.color}`}>
                          {threatLevel.label}
                        </div>
                      </div>
                      <Button 
                        variant="ghost" 
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          // This would open the email preview modal
                          console.log('View email details:', email.id)
                        }}
                      >
                        <EyeIcon className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>

                  {/* Expanded Details */}
                  {isSelected && (
                    <div className="mt-4 pt-4 border-t border-gray-200 space-y-3">
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="font-medium text-gray-700">Threat Analysis:</span>
                          <div className="mt-1 space-y-1">
                            {email.threatType ? (
                              <div className="flex items-center">
                                <ExclamationTriangleIcon className="h-4 w-4 text-danger-500 mr-2" />
                                <span>{email.threatType} detected</span>
                              </div>
                            ) : (
                              <div className="flex items-center">
                                <ShieldCheckIcon className="h-4 w-4 text-success-500 mr-2" />
                                <span>No threats detected</span>
                              </div>
                            )}
                          </div>
                        </div>
                        <div>
                          <span className="font-medium text-gray-700">Actions:</span>
                          <div className="mt-1 space-x-2">
                            <Button variant="outline" size="sm">
                              View Details
                            </Button>
                            <Button variant="outline" size="sm">
                              Take Action
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>

          {filteredEmails.length === 0 && (
            <div className="text-center py-12">
              <EnvelopeIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-1">No emails found</h3>
              <p className="text-gray-500">
                {searchTerm || filterStatus !== 'all'
                  ? 'Try adjusting your search or filter criteria'
                  : 'No emails have been processed yet'}
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
} 