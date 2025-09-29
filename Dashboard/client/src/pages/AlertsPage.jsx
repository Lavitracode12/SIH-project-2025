import React from 'react'
import DashboardLayout from '../layouts/DashboardLayout.jsx'
import Card, { CardHeader, CardContent } from '../components/Card.jsx'

const AlertRow = ({ type, message, time }) => (
  <div className="flex items-start justify-between border-t first:border-t-0 py-3">
    <div>
      <div className="text-sm font-medium">{type}</div>
      <div className="text-sm text-gray-600">{message}</div>
    </div>
    <div className="text-xs text-gray-500">{time}</div>
  </div>
)

const AlertsPage = () => {
  return (
    <DashboardLayout title="Alerts" subtitle="Recent system alerts and notifications.">
      <Card>
        <CardHeader title="Recent Alerts" />
        <CardContent className="px-5 pb-5">
          <AlertRow type="Warning" message="High infection rate detected in Field B." time="2m ago" />
          <AlertRow type="Info" message="Bot-003 completed scheduled inspection." time="1h ago" />
          <AlertRow type="Critical" message="Bot-002 tank below 10%." time="3h ago" />
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}

export default AlertsPage


