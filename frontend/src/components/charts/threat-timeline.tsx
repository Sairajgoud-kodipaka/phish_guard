'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

// Mock data for the timeline
const timelineData = [
  { time: '00:00', threats: 12, blocked: 8, quarantined: 3, delivered: 1 },
  { time: '04:00', threats: 8, blocked: 5, quarantined: 2, delivered: 1 },
  { time: '08:00', threats: 23, blocked: 18, quarantined: 4, delivered: 1 },
  { time: '12:00', threats: 35, blocked: 28, quarantined: 6, delivered: 1 },
  { time: '16:00', threats: 19, blocked: 15, quarantined: 3, delivered: 1 },
  { time: '20:00', threats: 16, blocked: 12, quarantined: 3, delivered: 1 },
]

export function ThreatTimeline() {
  const maxThreats = Math.max(...timelineData.map(d => d.threats))

  return (
    <Card>
      <CardHeader>
        <CardTitle>Threat Timeline</CardTitle>
        <CardDescription>
          Real-time threat detection over the last 24 hours
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Chart Area */}
          <div className="h-64 flex items-end justify-between px-4 pb-4 border-b border-gray-200">
            {timelineData.map((data, index) => {
              const height = (data.threats / maxThreats) * 100
              return (
                <div key={index} className="flex flex-col items-center space-y-2">
                  <div 
                    className="w-8 bg-gradient-to-t from-danger-500 to-danger-300 rounded-t transition-all duration-300 hover:from-danger-600 hover:to-danger-400"
                    style={{ height: `${height}%`, minHeight: '4px' }}
                    title={`${data.threats} threats at ${data.time}`}
                  />
                  <span className="text-xs text-gray-500 font-medium">
                    {data.time}
                  </span>
                </div>
              )
            })}
          </div>

          {/* Legend */}
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-danger-500 rounded" />
              <span className="text-gray-700">Blocked</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-warning-500 rounded" />
              <span className="text-gray-700">Quarantined</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-success-500 rounded" />
              <span className="text-gray-700">Delivered</span>
            </div>
          </div>

          {/* Summary Stats */}
          <div className="pt-4 border-t border-gray-200">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-gray-900">
                  {timelineData.reduce((sum, d) => sum + d.blocked, 0)}
                </div>
                <div className="text-sm text-gray-500">Total Blocked</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-900">
                  {timelineData.reduce((sum, d) => sum + d.quarantined, 0)}
                </div>
                <div className="text-sm text-gray-500">Quarantined</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-900">
                  {((timelineData.reduce((sum, d) => sum + d.blocked, 0) / 
                     timelineData.reduce((sum, d) => sum + d.threats, 0)) * 100).toFixed(1)}%
                </div>
                <div className="text-sm text-gray-500">Block Rate</div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 