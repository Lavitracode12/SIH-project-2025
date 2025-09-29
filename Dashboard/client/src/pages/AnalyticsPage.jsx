import React from 'react'
import DashboardLayout from '../layouts/DashboardLayout.jsx'
import Card, { CardHeader, CardContent } from '../components/Card.jsx'

const AnalyticsPage = () => {
  return (
    <DashboardLayout title="Analytics" subtitle="Trends and metrics for disease detection and operations.">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader title="Infection Rate Over Time" />
          <CardContent>
            <div className="h-56 rounded-md bg-gradient-to-t from-blue-200 to-transparent" />
          </CardContent>
        </Card>
        <Card>
          <CardHeader title="Pesticide Consumption" />
          <CardContent>
            <div className="h-56 rounded-md bg-gradient-to-t from-emerald-200 to-transparent" />
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}

export default AnalyticsPage


