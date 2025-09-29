import React from 'react'
import Topbar from '../components/Topbar.jsx'
import Sidebar from '../components/Sidebar.jsx'

const DashboardLayout = ({ title, subtitle, children }) => {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <Topbar />
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
        {title && (
          <div className="mb-4">
            <h1 className="text-2xl font-semibold">{title}</h1>
            {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
          </div>
        )}
        <div className="flex gap-6">
          <Sidebar />
          <main className="flex-1">{children}</main>
        </div>
      </div>
    </div>
  )
}

export default DashboardLayout


