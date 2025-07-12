'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ThreatTimeline } from '@/components/charts/threat-timeline'
import {
  DocumentArrowDownIcon,
  ChartBarIcon,
  CalendarIcon,
  FunnelIcon,
  PresentationChartLineIcon,
  DocumentTextIcon,
  TableCellsIcon,
} from '@heroicons/react/24/outline'

const reportTypes = [
  {
    id: 'executive',
    name: 'Executive Summary',
    description: 'High-level security overview and key metrics',
    icon: PresentationChartLineIcon,
    frequency: 'Weekly',
    lastGenerated: '2 days ago',
  },
  {
    id: 'technical',
    name: 'Technical Analysis',
    description: 'Detailed threat analysis and system performance',
    icon: ChartBarIcon,
    frequency: 'Daily',
    lastGenerated: '6 hours ago',
  },
  {
    id: 'compliance',
    name: 'Compliance Report',
    description: 'Security compliance and audit information',
    icon: DocumentTextIcon,
    frequency: 'Monthly',
    lastGenerated: '1 week ago',
  },
  {
    id: 'incident',
    name: 'Incident Response',
    description: 'Security incidents and response actions',
    icon: TableCellsIcon,
    frequency: 'As needed',
    lastGenerated: '3 days ago',
  },
]

const analyticsData = [
  {
    title: 'Threat Detection Trends',
    description: 'Analysis of threat patterns over the last 30 days',
    metrics: [
      { label: 'Phishing Attempts', value: '1,234', change: '+15%', trend: 'up' },
      { label: 'Malware Detected', value: '89', change: '-22%', trend: 'down' },
      { label: 'Social Engineering', value: '456', change: '+8%', trend: 'up' },
      { label: 'Spam Filtered', value: '12,847', change: '+3%', trend: 'up' },
    ],
  },
  {
    title: 'System Performance',
    description: 'Email processing and system health metrics',
    metrics: [
      { label: 'Processing Speed', value: '1.2s', change: '-0.3s', trend: 'down' },
      { label: 'System Uptime', value: '99.9%', change: '+0.1%', trend: 'up' },
      { label: 'False Positives', value: '2.1%', change: '-0.5%', trend: 'down' },
      { label: 'Detection Accuracy', value: '97.8%', change: '+1.2%', trend: 'up' },
    ],
  },
]

const complianceMetrics = [
  { standard: 'SOC 2 Type II', status: 'Compliant', lastAudit: '3 months ago', nextDue: '9 months' },
  { standard: 'GDPR', status: 'Compliant', lastAudit: '6 months ago', nextDue: '6 months' },
  { standard: 'ISO 27001', status: 'In Progress', lastAudit: '1 year ago', nextDue: '2 months' },
  { standard: 'NIST Framework', status: 'Compliant', lastAudit: '4 months ago', nextDue: '8 months' },
]

export default function ReportsPage() {
  const [selectedDateRange, setSelectedDateRange] = useState('30d')
  const [selectedFormat, setSelectedFormat] = useState('pdf')

  const generateReport = (reportType: string) => {
    // Simulate report generation
    console.log(`Generating ${reportType} report...`)
    // In a real app, this would trigger the backend report generation
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Reports & Analytics</h1>
          <p className="text-gray-500 mt-2">
            Generate comprehensive security reports and view analytics
          </p>
        </div>
        <div className="flex space-x-3">
          <div className="flex items-center space-x-2">
            <CalendarIcon className="h-4 w-4 text-gray-400" />
            <select
              value={selectedDateRange}
              onChange={(e) => setSelectedDateRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
              <option value="1y">Last year</option>
            </select>
          </div>
          <Button variant="outline" size="sm">
            <FunnelIcon className="h-4 w-4 mr-2" />
            Filters
          </Button>
        </div>
      </div>

      {/* Report Types */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {reportTypes.map((report) => (
          <Card key={report.id} className="hover:shadow-md transition-shadow cursor-pointer">
            <CardHeader className="pb-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-primary-100 rounded-lg">
                  <report.icon className="h-6 w-6 text-primary-600" />
                </div>
                <div>
                  <CardTitle className="text-lg">{report.name}</CardTitle>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <CardDescription className="mb-4">
                {report.description}
              </CardDescription>
              <div className="space-y-2 text-sm text-gray-600 mb-4">
                <div>Frequency: {report.frequency}</div>
                <div>Last generated: {report.lastGenerated}</div>
              </div>
              <div className="flex space-x-2">
                <Button
                  size="sm"
                  className="flex-1"
                  onClick={() => generateReport(report.id)}
                >
                  Generate
                </Button>
                <Button variant="outline" size="sm">
                  <DocumentArrowDownIcon className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Analytics Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {analyticsData.map((section, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle>{section.title}</CardTitle>
              <CardDescription>{section.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {section.metrics.map((metric, metricIndex) => (
                  <div key={metricIndex} className="flex items-center justify-between">
                    <div>
                      <div className="text-sm text-gray-600">{metric.label}</div>
                      <div className="text-lg font-semibold text-gray-900">{metric.value}</div>
                    </div>
                    <div className={`text-sm font-medium ${
                      metric.trend === 'up' ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      {metric.change}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Threat Timeline Chart */}
      <ThreatTimeline />

      {/* Compliance Dashboard */}
      <Card>
        <CardHeader>
          <CardTitle>Compliance Status</CardTitle>
          <CardDescription>
            Current compliance status across security standards
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Standard
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Last Audit
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Next Due
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {complianceMetrics.map((metric, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {metric.standard}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                        metric.status === 'Compliant' 
                          ? 'bg-success-100 text-success-800'
                          : 'bg-warning-100 text-warning-800'
                      }`}>
                        {metric.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {metric.lastAudit}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {metric.nextDue}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <Button variant="outline" size="sm">
                        View Report
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Export Options */}
      <Card>
        <CardHeader>
          <CardTitle>Export Options</CardTitle>
          <CardDescription>
            Generate custom reports with specific data ranges and formats
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date Range
              </label>
              <select
                value={selectedDateRange}
                onChange={(e) => setSelectedDateRange(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="7d">Last 7 days</option>
                <option value="30d">Last 30 days</option>
                <option value="90d">Last 90 days</option>
                <option value="1y">Last year</option>
                <option value="custom">Custom range</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Format
              </label>
              <select
                value={selectedFormat}
                onChange={(e) => setSelectedFormat(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="pdf">PDF</option>
                <option value="excel">Excel</option>
                <option value="csv">CSV</option>
                <option value="json">JSON</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Include
              </label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input type="checkbox" className="rounded mr-2" defaultChecked />
                  <span className="text-sm">Charts & Graphs</span>
                </label>
                <label className="flex items-center">
                  <input type="checkbox" className="rounded mr-2" defaultChecked />
                  <span className="text-sm">Raw Data</span>
                </label>
              </div>
            </div>
          </div>
          <div className="flex space-x-3">
            <Button className="flex-1">
              <DocumentArrowDownIcon className="h-4 w-4 mr-2" />
              Generate Custom Report
            </Button>
            <Button variant="outline">
              Schedule Report
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 