import React from 'react'
import DashboardLayout from '../layouts/DashboardLayout.jsx'
import Card, { CardHeader, CardContent } from '../components/Card.jsx'

const BotCard = ({ id, status, area }) => (
  <Card className="p-5">
    <div className="flex items-center justify-between">
      <div className="font-semibold">{id}</div>
      <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${status==='Active'?'bg-green-50 text-green-700':'bg-yellow-50 text-yellow-700'}`}>{status}</span>
    </div>
    <div className="text-sm text-gray-600 mt-2">Working Area: {area}</div>
    <button className="mt-4 rounded-md bg-blue-600 text-white px-4 py-2">Open Controls</button>
  </Card>
)

const BotsPage = () => {
  return (
    <DashboardLayout title="Bots" subtitle="Manage individual bot status and operations.">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <BotCard id="Bot-001" status="Active" area="Field A - 15 acres" />
        <BotCard id="Bot-002" status="Active" area="Field B - 12 acres" />
        <BotCard id="Bot-003" status="Idle" area="Field C - 10 acres" />
      </div>
    </DashboardLayout>
  )
}

export default BotsPage


