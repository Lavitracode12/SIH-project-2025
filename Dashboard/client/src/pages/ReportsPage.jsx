import React from 'react'
import DashboardLayout from '../layouts/DashboardLayout.jsx'
import Card, { CardHeader, CardContent } from '../components/Card.jsx'

const ReportsPage = () => {
  return (
    <DashboardLayout title="Reports" subtitle="Download and review system performance and activity reports.">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader title="Monthly Summary" />
          <CardContent>
            <p className="text-sm text-gray-600">Overview of plants monitored, infections, pesticide usage, and uptime.</p>
            <button className="mt-4 inline-flex items-center rounded-md bg-blue-600 text-white px-4 py-2">Download PDF</button>
          </CardContent>
        </Card>
        <Card>
          <CardHeader title="Detailed Activity Logs" />
          <CardContent>
            <p className="text-sm text-gray-600">Export raw logs for audits and analysis.</p>
            <div className="mt-4 flex gap-3">
              <button className="rounded-md bg-gray-900 text-white px-4 py-2">Export CSV</button>
              <button className="rounded-md bg-gray-100 px-4 py-2">Export JSON</button>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}

export default ReportsPage


