'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import {
  CogIcon,
  UserGroupIcon,
  ShieldCheckIcon,
  BellIcon,
  DatabaseIcon,
  KeyIcon,
  GlobeAltIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline'

const settingsSections = [
  {
    id: 'general',
    name: 'General Settings',
    icon: CogIcon,
    description: 'Basic system configuration',
  },
  {
    id: 'security',
    name: 'Security Settings',
    icon: ShieldCheckIcon,
    description: 'Threat detection and response',
  },
  {
    id: 'users',
    name: 'User Management',
    icon: UserGroupIcon,
    description: 'User accounts and permissions',
  },
  {
    id: 'notifications',
    name: 'Notifications',
    icon: BellIcon,
    description: 'Alert and notification settings',
  },
  {
    id: 'integrations',
    name: 'Integrations',
    icon: GlobeAltIcon,
    description: 'External service connections',
  },
  {
    id: 'analytics',
    name: 'Analytics',
    icon: ChartBarIcon,
    description: 'Reporting and analytics settings',
  },
]

const users = [
  {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@company.com',
    role: 'Administrator',
    status: 'Active',
    lastLogin: '2 hours ago',
  },
  {
    id: 2,
    name: 'Jane Smith',
    email: 'jane.smith@company.com',
    role: 'Security Analyst',
    status: 'Active',
    lastLogin: '1 day ago',
  },
  {
    id: 3,
    name: 'Bob Wilson',
    email: 'bob.wilson@company.com',
    role: 'Viewer',
    status: 'Inactive',
    lastLogin: '1 week ago',
  },
]

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('general')
  const [threatThresholds, setThreatThresholds] = useState({
    phishing: 75,
    malware: 80,
    socialEngineering: 70,
    spam: 85,
  })
  const [notificationSettings, setNotificationSettings] = useState({
    emailAlerts: true,
    slackNotifications: false,
    webhookUrl: '',
    criticalThreatsOnly: false,
  })

  const renderGeneralSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>System Configuration</CardTitle>
          <CardDescription>Basic system settings and preferences</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Organization Name
              </label>
              <Input defaultValue="PhishGuard Security Corp" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Time Zone
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option>UTC-05:00 (Eastern Time)</option>
                <option>UTC-08:00 (Pacific Time)</option>
                <option>UTC+00:00 (GMT)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Default Language
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500">
                <option>English</option>
                <option>Spanish</option>
                <option>French</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Session Timeout (minutes)
              </label>
              <Input type="number" defaultValue="30" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Email Processing</CardTitle>
          <CardDescription>Configure email processing settings</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Emails per Batch
              </label>
              <Input type="number" defaultValue="100" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Processing Timeout (seconds)
              </label>
              <Input type="number" defaultValue="30" />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <input type="checkbox" id="autoProcess" className="rounded" defaultChecked />
            <label htmlFor="autoProcess" className="text-sm text-gray-700">
              Enable automatic email processing
            </label>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderSecuritySettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Threat Detection Thresholds</CardTitle>
          <CardDescription>Configure threat detection sensitivity levels</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {Object.entries(threatThresholds).map(([threat, value]) => (
            <div key={threat} className="space-y-2">
              <div className="flex justify-between">
                <label className="text-sm font-medium text-gray-700 capitalize">
                  {threat.replace(/([A-Z])/g, ' $1')} Threshold
                </label>
                <span className="text-sm text-gray-600">{value}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={value}
                onChange={(e) => setThreatThresholds(prev => ({
                  ...prev,
                  [threat]: Number(e.target.value)
                }))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Response Actions</CardTitle>
          <CardDescription>Configure automatic response actions for threats</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Block high-risk emails automatically</span>
              <input type="checkbox" className="rounded" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Quarantine medium-risk emails</span>
              <input type="checkbox" className="rounded" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Send alerts for critical threats</span>
              <input type="checkbox" className="rounded" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Log all threat detections</span>
              <input type="checkbox" className="rounded" defaultChecked />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderUserManagement = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>User Accounts</CardTitle>
              <CardDescription>Manage user accounts and permissions</CardDescription>
            </div>
            <Button>Add User</Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    User
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Role
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Last Login
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{user.name}</div>
                        <div className="text-sm text-gray-500">{user.email}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Badge variant={user.role === 'Administrator' ? 'default' : 'secondary'}>
                        {user.role}
                      </Badge>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Badge variant={user.status === 'Active' ? 'success' : 'secondary'}>
                        {user.status}
                      </Badge>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {user.lastLogin}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <div className="flex space-x-2">
                        <Button variant="outline" size="sm">Edit</Button>
                        <Button variant="outline" size="sm">Delete</Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderNotificationSettings = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Alert Settings</CardTitle>
          <CardDescription>Configure how you receive threat notifications</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Email Alerts</span>
              <input
                type="checkbox"
                className="rounded"
                checked={notificationSettings.emailAlerts}
                onChange={(e) => setNotificationSettings(prev => ({
                  ...prev,
                  emailAlerts: e.target.checked
                }))}
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Slack Notifications</span>
              <input
                type="checkbox"
                className="rounded"
                checked={notificationSettings.slackNotifications}
                onChange={(e) => setNotificationSettings(prev => ({
                  ...prev,
                  slackNotifications: e.target.checked
                }))}
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Critical Threats Only</span>
              <input
                type="checkbox"
                className="rounded"
                checked={notificationSettings.criticalThreatsOnly}
                onChange={(e) => setNotificationSettings(prev => ({
                  ...prev,
                  criticalThreatsOnly: e.target.checked
                }))}
              />
            </div>
          </div>
          
          <div className="pt-4 border-t">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Webhook URL
            </label>
            <Input
              placeholder="https://your-webhook-url.com/alerts"
              value={notificationSettings.webhookUrl}
              onChange={(e) => setNotificationSettings(prev => ({
                ...prev,
                webhookUrl: e.target.value
              }))}
            />
            <p className="text-xs text-gray-500 mt-1">
              Receive threat notifications via HTTP webhook
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderIntegrations = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>External Integrations</CardTitle>
          <CardDescription>Connect PhishGuard with external services</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-gray-900">VirusTotal</h4>
                <Badge variant="success">Connected</Badge>
              </div>
              <p className="text-sm text-gray-600 mb-3">
                URL and file reputation checking
              </p>
              <Button variant="outline" size="sm">Configure</Button>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-gray-900">Microsoft 365</h4>
                <Badge variant="secondary">Not Connected</Badge>
              </div>
              <p className="text-sm text-gray-600 mb-3">
                Email integration and protection
              </p>
              <Button variant="outline" size="sm">Connect</Button>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-gray-900">Google Workspace</h4>
                <Badge variant="secondary">Not Connected</Badge>
              </div>
              <p className="text-sm text-gray-600 mb-3">
                Gmail security integration
              </p>
              <Button variant="outline" size="sm">Connect</Button>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-gray-900">Slack</h4>
                <Badge variant="warning">Pending</Badge>
              </div>
              <p className="text-sm text-gray-600 mb-3">
                Team notifications and alerts
              </p>
              <Button variant="outline" size="sm">Configure</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderAnalytics = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Analytics Configuration</CardTitle>
          <CardDescription>Configure data collection and reporting</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Enable detailed analytics</span>
              <input type="checkbox" className="rounded" defaultChecked />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Collect user behavior data</span>
              <input type="checkbox" className="rounded" />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Generate automatic reports</span>
              <input type="checkbox" className="rounded" defaultChecked />
            </div>
          </div>
          
          <div className="pt-4 border-t">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Data Retention Period (days)
            </label>
            <select className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-primary-500">
              <option value="30">30 days</option>
              <option value="90">90 days</option>
              <option value="365">1 year</option>
              <option value="1095">3 years</option>
            </select>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderContent = () => {
    switch (activeSection) {
      case 'general':
        return renderGeneralSettings()
      case 'security':
        return renderSecuritySettings()
      case 'users':
        return renderUserManagement()
      case 'notifications':
        return renderNotificationSettings()
      case 'integrations':
        return renderIntegrations()
      case 'analytics':
        return renderAnalytics()
      default:
        return renderGeneralSettings()
    }
  }

  return (
    <div className="flex space-x-6">
      {/* Sidebar */}
      <div className="w-64 flex-shrink-0">
        <nav className="space-y-1">
          {settingsSections.map((section) => (
            <button
              key={section.id}
              onClick={() => setActiveSection(section.id)}
              className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                activeSection === section.id
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`}
            >
              <section.icon className="mr-3 h-5 w-5" />
              <span>{section.name}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-500 mt-2">
            {settingsSections.find(s => s.id === activeSection)?.description}
          </p>
        </div>

        {renderContent()}

        {/* Save Button */}
        <div className="mt-8 flex justify-end space-x-3">
          <Button variant="outline">Cancel</Button>
          <Button>Save Changes</Button>
        </div>
      </div>
    </div>
  )
} 