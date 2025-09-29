import React from 'react'
import DashboardLayout from '../layouts/DashboardLayout.jsx'
import Card, { CardHeader, CardContent } from '../components/Card.jsx'

const StatCard = ({ label, value, delta, positive }) => (
  <Card className="p-5">
    <div className="text-sm text-gray-500">{label}</div>
    <div className="mt-2 flex items-end gap-2">
      <div className="text-2xl font-semibold">{value}</div>
      <div className={`text-sm ${positive? 'text-green-600':'text-red-600'}`}>{delta}</div>
    </div>
  </Card>
)

const ActivityRow = ({ id, status, position, area, tank, usage }) => (
  <tr className="border-t">
    <td className="px-4 py-3 text-sm text-blue-600 font-medium">{id}</td>
    <td className="px-4 py-3"><span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${status==='Active'?'bg-green-50 text-green-700':'bg-yellow-50 text-yellow-700'}`}>{status}</span></td>
    <td className="px-4 py-3 text-sm text-gray-700">{position}</td>
    <td className="px-4 py-3 text-sm text-gray-700">{area}</td>
    <td className="px-4 py-3">
      <div className="h-2 w-28 bg-gray-200 rounded-full overflow-hidden">
        <div className="h-full bg-blue-500" style={{width: tank}} />
      </div>
    </td>
    <td className="px-4 py-3 text-sm text-gray-700">{usage}</td>
  </tr>
)

const DashboardPage = () => {
  return (
    <DashboardLayout title="Dashboard Overview" subtitle="Real-time monitoring and control of your automated pesticide system.">
      <section>
        <h2 className="text-lg font-semibold mb-3">System Status</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard label="Total Plants Monitored" value="12,500" delta="+10%" positive />
          <StatCard label="Infection Rate" value="3.5%" delta="-0.5%" />
          <StatCard label="Pesticide Consumption" value="250L" delta="+5%" positive />
          <StatCard label="Bots Active" value="3" delta="+1" positive />
        </div>
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <Card>
          <CardHeader title="Bot Control" />
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <div className="text-sm font-medium mb-2">Manual Operation</div>
                <div className="grid grid-cols-3 gap-2 w-40">
                  <button className="h-10 rounded-md bg-gray-100">↑</button>
                  <button className="h-10 rounded-md bg-red-600 text-white">■</button>
                  <button className="h-10 rounded-md bg-gray-100">↗</button>
                  <button className="h-10 rounded-md bg-gray-100">←</button>
                  <button className="h-10 rounded-md bg-blue-600 text-white">⬛</button>
                  <button className="h-10 rounded-md bg-gray-100">→</button>
                  <button className="h-10 rounded-md bg-gray-100">↙</button>
                  <button className="h-10 rounded-md bg-gray-100">↓</button>
                  <button className="h-10 rounded-md bg-gray-100">↘</button>
                </div>
                <div className="mt-6">
                  <div className="text-sm font-medium mb-1">Spray Pattern</div>
                  <select className="w-56 h-10 rounded-md border-gray-300">
                    <option>Standard Cone</option>
                    <option>Fine Mist</option>
                  </select>
                </div>
                <button className="mt-6 inline-flex items-center gap-2 rounded-md bg-red-600 text-white px-4 py-2">Emergency Stop</button>
              </div>
              <div className="space-y-6">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-sm font-medium">Task Scheduling & Automation</div>
                    <button className="text-blue-600 text-sm">+ Add New Task</button>
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between rounded-lg border p-3">
                      <div>
                        <div className="font-medium text-sm">Daily Spraying - Field A</div>
                        <div className="text-xs text-gray-500">Starts at 08:00 AM</div>
                      </div>
                      <label className="inline-flex items-center cursor-pointer">
                        <input type="checkbox" defaultChecked className="sr-only peer" />
                        <div className="w-10 h-5 bg-gray-200 rounded-full peer-checked:bg-blue-600 relative after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:h-4 after:w-4 after:bg-white after:rounded-full peer-checked:after:translate-x-5 transition" />
                      </label>
                    </div>
                    <div className="flex items-center justify-between rounded-lg border p-3">
                      <div>
                        <div className="font-medium text-sm">Weekly Inspection - All Fields</div>
                        <div className="text-xs text-gray-500">Every Monday</div>
                      </div>
                      <label className="inline-flex items-center cursor-pointer">
                        <input type="checkbox" className="sr-only peer" />
                        <div className="w-10 h-5 bg-gray-200 rounded-full peer-checked:bg-blue-600 relative after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:h-4 after:w-4 after:bg-white after:rounded-full peer-checked:after:translate-x-5 transition" />
                      </label>
                    </div>
                  </div>
                </div>
                <div>
                  <div className="text-sm font-medium mb-2">Path Planning & Navigation</div>
                  <div className="h-40 rounded-lg border border-dashed bg-gray-50 flex items-center justify-center text-gray-400">Path Visualization Area</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader title="Bot Activity" />
          <CardContent className="px-0 pb-0">
            <div className="overflow-x-auto">
              <table className="min-w-full text-left">
                <thead className="text-xs text-gray-500">
                  <tr>
                    <th className="px-4 py-2">BOT ID</th>
                    <th className="px-4 py-2">STATUS</th>
                    <th className="px-4 py-2">CURRENT POSITION</th>
                    <th className="px-4 py-2">WORKING AREA</th>
                    <th className="px-4 py-2">TANK LEVEL</th>
                    <th className="px-4 py-2">USAGE</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  <ActivityRow id="Bot-001" status="Active" position="Field A, Sector 3" area="15 acres" tank="76%" usage="20L/hr" />
                  <ActivityRow id="Bot-002" status="Active" position="Field B, Sector 1" area="12 acres" tank="60%" usage="16L/hr" />
                  <ActivityRow id="Bot-003" status="Idle" position="Field C, Sector 2" area="10 acres" tank="100%" usage="0L/hr" />
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader title="Disease Detection Results" />
            <CardContent>
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <div className="text-sm text-gray-500">Disease Distribution</div>
                  <div className="text-3xl font-semibold mt-2">3.5%</div>
                  <div className="text-xs text-green-600 mt-1">Last 7 Days  +0.5%</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Infection Rate Over Time</div>
                  <div className="h-24 bg-gradient-to-t from-blue-200 to-transparent rounded-b" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default DashboardPage


