'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { DataTable, Column } from '@/components/ui/data-table'
import {
  ExclamationTriangleIcon,
  ShieldCheckIcon,
  ClockIcon,
  EyeIcon,
  MagnifyingGlassIcon,
  ChartBarIcon,
  DocumentArrowDownIcon,
  FunnelIcon,
} from '@heroicons/react/24/outline'
import { formatDate, formatThreatLevel, cn } from '@/lib/utils'

interface ThreatData {
  id: number
  email: string
  sender: string
  subject: string
  threatType: string
  riskLevel: number
  status: 'blocked' | 'quarantined' | 'investigating'
  detectedAt: Date
  indicators: string[]
  description: string
  actionTaken: string
}

const mockThreats: ThreatData[] = [
  {
    id: 1,
    email: 'urgent-payment@fake-bank.com',
    sender: 'security@fake-bank.com',
    subject: 'URGENT: Verify Your Account Immediately',
    threatType: 'Phishing',
    riskLevel: 89,
    status: 'blocked',
    detectedAt: new Date(Date.now() - 5 * 60 * 1000),
    indicators: ['Suspicious sender', 'Malicious URLs', 'Social engineering'],
    description: 'Phishing email attempting to steal banking credentials',
    actionTaken: 'Email blocked and sender blacklisted',
  },
  {
    id: 2,
    email: 'invoice-update@suspicious-domain.net',
    sender: 'billing@suspicious-domain.net',
    subject: 'Invoice Update Required - Action Needed',
    threatType: 'Social Engineering',
    riskLevel: 76,
    status: 'quarantined',
    detectedAt: new Date(Date.now() - 15 * 60 * 1000),
    indicators: ['Unknown sender', 'Suspicious attachment', 'Urgency tactics'],
    description: 'Social engineering attempt with fake invoice',
    actionTaken: 'Email quarantined for review',
  },
  {
    id: 3,
    email: 'security-alert@malware-site.org',
    sender: 'alerts@malware-site.org',
    subject: 'Security Alert: Suspicious Activity Detected',
    threatType: 'Malware',
    riskLevel: 94,
    status: 'blocked',
    detectedAt: new Date(Date.now() - 60 * 60 * 1000),
    indicators: ['Known malware domain', 'Suspicious attachment', 'Command & Control'],
    description: 'Email containing malware payload',
    actionTaken: 'Email blocked and attachment quarantined',
  },
  {
    id: 4,
    email: 'document-shared@credential-harvest.com',
    sender: 'noreply@credential-harvest.com',
    subject: 'Shared Document: Q4 Financial Report.pdf',
    threatType: 'Credential Harvesting',
    riskLevel: 82,
    status: 'investigating',
    detectedAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
    indicators: ['Credential harvesting patterns', 'Fake document sharing', 'Suspicious links'],
    description: 'Attempt to harvest credentials via fake document sharing',
    actionTaken: 'Under investigation by security team',
  },
  {
    id: 5,
    email: 'prize-notification@lottery-scam.biz',
    sender: 'winner@lottery-scam.biz',
    subject: 'Congratulations! You\'ve Won $1,000,000',
    threatType: 'Scam',
    riskLevel: 71,
    status: 'blocked',
    detectedAt: new Date(Date.now() - 3 * 60 * 60 * 1000),
    indicators: ['Known scam patterns', 'Financial fraud', 'Emotional manipulation'],
    description: 'Classic lottery scam attempting financial fraud',
    actionTaken: 'Email blocked and domain reported',
  },
]

const statusColors = {
  blocked: 'destructive',
  quarantined: 'warning',
  investigating: 'secondary',
} as const

const threatTypeColors = {
  'Phishing': 'destructive',
  'Malware': 'destructive',
  'Social Engineering': 'warning',
  'Credential Harvesting': 'warning',
  'Scam': 'secondary',
} as const

export default function ThreatsPage() {
  const [selectedThreat, setSelectedThreat] = useState<ThreatData | null>(null)
  const [filterStatus, setFilterStatus] = useState('all')
  const [filterThreatType, setFilterThreatType] = useState('all')

  const filteredThreats = mockThreats.filter((threat) => {
    const matchesStatus = filterStatus === 'all' || threat.status === filterStatus
    const matchesThreatType = filterThreatType === 'all' || threat.threatType === filterThreatType
    return matchesStatus && matchesThreatType
  })

  const columns: Column<ThreatData>[] = [
    {
      key: 'sender',
      header: 'Sender',
      sortable: true,
      render: (value, row) => (
        <div className="space-y-1">
          <div className="font-medium text-gray-900 truncate">{value}</div>
          <div className="text-xs text-gray-500 truncate">{row.email}</div>
        </div>
      ),
    },
    {
      key: 'subject',
      header: 'Subject',
      sortable: true,
      render: (value) => (
        <div className="max-w-xs truncate font-medium text-gray-900" title={value}>
          {value}
        </div>
      ),
    },
    {
      key: 'threatType',
      header: 'Threat Type',
      sortable: true,
      render: (value) => (
        <Badge variant={threatTypeColors[value as keyof typeof threatTypeColors] || 'secondary'}>
          {value}
        </Badge>
      ),
    },
    {
      key: 'riskLevel',
      header: 'Risk Level',
      sortable: true,
      render: (value) => {
        const threat = formatThreatLevel(value)
        return (
          <div className="flex items-center space-x-2">
            <div className={`px-2 py-1 rounded-full text-xs font-medium ${threat.bgColor} ${threat.color}`}>
              {value}%
            </div>
            <span className={`text-xs font-medium ${threat.color}`}>
              {threat.label}
            </span>
          </div>
        )
      },
    },
    {
      key: 'status',
      header: 'Status',
      sortable: true,
      render: (value) => (
        <Badge variant={statusColors[value as keyof typeof statusColors]}>
          {value}
        </Badge>
      ),
    },
    {
      key: 'detectedAt',
      header: 'Detected At',
      sortable: true,
      render: (value) => (
        <div className="text-sm text-gray-600">
          {formatDate(value)}
        </div>
      ),
    },
    {
      key: 'id',
      header: 'Actions',
      render: (_, row) => (
        <Button
          variant="ghost"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            setSelectedThreat(row)
          }}
        >
          <EyeIcon className="h-4 w-4" />
        </Button>
      ),
    },
  ]

  const threatStats = [
    {
      name: 'Total Threats',
      value: filteredThreats.length,
      icon: ExclamationTriangleIcon,
      color: 'text-danger-600',
      bgColor: 'bg-danger-100',
    },
    {
      name: 'Blocked',
      value: filteredThreats.filter(t => t.status === 'blocked').length,
      icon: ShieldCheckIcon,
      color: 'text-danger-600',
      bgColor: 'bg-danger-100',
    },
    {
      name: 'Quarantined',
      value: filteredThreats.filter(t => t.status === 'quarantined').length,
      icon: ClockIcon,
      color: 'text-warning-600',
      bgColor: 'bg-warning-100',
    },
    {
      name: 'Investigating',
      value: filteredThreats.filter(t => t.status === 'investigating').length,
      icon: MagnifyingGlassIcon,
      color: 'text-primary-600',
      bgColor: 'bg-primary-100',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Threat Analysis</h1>
          <p className="text-gray-500 mt-2">
            Comprehensive threat detection and analysis
          </p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline" size="sm">
            <DocumentArrowDownIcon className="h-4 w-4 mr-2" />
            Export Report
          </Button>
          <Button size="sm">
            <ChartBarIcon className="h-4 w-4 mr-2" />
            Analytics
          </Button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {threatStats.map((stat) => (
          <Card key={stat.name}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className={`p-3 rounded-full ${stat.bgColor}`}>
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Filters */}
      <Card>
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center">
            <FunnelIcon className="h-5 w-5 mr-2" />
            Filters
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">All Status</option>
                <option value="blocked">Blocked</option>
                <option value="quarantined">Quarantined</option>
                <option value="investigating">Investigating</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Threat Type
              </label>
              <select
                value={filterThreatType}
                onChange={(e) => setFilterThreatType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="all">All Types</option>
                <option value="Phishing">Phishing</option>
                <option value="Malware">Malware</option>
                <option value="Social Engineering">Social Engineering</option>
                <option value="Credential Harvesting">Credential Harvesting</option>
                <option value="Scam">Scam</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Threats Table */}
      <Card>
        <CardHeader>
          <CardTitle>Detected Threats</CardTitle>
          <CardDescription>
            All threats detected by the PhishGuard AI engine
          </CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <DataTable
            data={filteredThreats}
            columns={columns}
            onRowClick={setSelectedThreat}
            searchable
            pagination
            pageSize={10}
            emptyMessage="No threats detected"
          />
        </CardContent>
      </Card>

      {/* Threat Detail Modal */}
      {selectedThreat && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Threat Details</CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedThreat(null)}
                >
                  ✕
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Basic Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Threat ID</label>
                  <p className="text-sm text-gray-900">TH-{selectedThreat.id.toString().padStart(6, '0')}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Risk Level</label>
                  <div className="flex items-center space-x-2 mt-1">
                    {(() => {
                      const threat = formatThreatLevel(selectedThreat.riskLevel)
                      return (
                        <>
                          <div className={`px-2 py-1 rounded-full text-xs font-medium ${threat.bgColor} ${threat.color}`}>
                            {selectedThreat.riskLevel}%
                          </div>
                          <span className={`text-sm font-medium ${threat.color}`}>
                            {threat.label}
                          </span>
                        </>
                      )
                    })()}
                  </div>
                </div>
              </div>

              {/* Email Details */}
              <div className="space-y-4">
                <h4 className="font-medium text-gray-900">Email Details</h4>
                <div className="bg-gray-50 p-4 rounded-lg space-y-3">
                  <div>
                    <label className="text-sm font-medium text-gray-500">From</label>
                    <p className="text-sm text-gray-900">{selectedThreat.sender}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Subject</label>
                    <p className="text-sm text-gray-900">{selectedThreat.subject}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Detected At</label>
                    <p className="text-sm text-gray-900">{formatDate(selectedThreat.detectedAt)}</p>
                  </div>
                </div>
              </div>

              {/* Threat Analysis */}
              <div className="space-y-4">
                <h4 className="font-medium text-gray-900">Threat Analysis</h4>
                <div className="space-y-3">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Threat Type</label>
                    <div className="mt-1">
                      <Badge variant={threatTypeColors[selectedThreat.threatType as keyof typeof threatTypeColors]}>
                        {selectedThreat.threatType}
                      </Badge>
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Description</label>
                    <p className="text-sm text-gray-900 mt-1">{selectedThreat.description}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Threat Indicators</label>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {selectedThreat.indicators.map((indicator, index) => (
                        <Badge key={index} variant="outline">
                          {indicator}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Actions Taken */}
              <div className="space-y-4">
                <h4 className="font-medium text-gray-900">Response</h4>
                <div className="bg-gray-50 p-4 rounded-lg space-y-3">
                  <div>
                    <label className="text-sm font-medium text-gray-500">Status</label>
                    <div className="mt-1">
                      <Badge variant={statusColors[selectedThreat.status]}>
                        {selectedThreat.status}
                      </Badge>
                    </div>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-500">Action Taken</label>
                    <p className="text-sm text-gray-900 mt-1">{selectedThreat.actionTaken}</p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex space-x-3">
                <Button variant="outline" className="flex-1">
                  Export Details
                </Button>
                <Button variant="outline" className="flex-1">
                  Create Report
                </Button>
                <Button className="flex-1">
                  Take Action
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
} 