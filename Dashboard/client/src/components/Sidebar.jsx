import React from 'react'
import { NavLink } from 'react-router-dom'

const Sidebar = () => {
  const linkClass = ({isActive}) => `flex items-center gap-3 px-3 py-2 rounded-md hover:bg-gray-100 ${isActive? 'bg-gray-100 text-gray-900':'text-gray-700'}`
  return (
    <aside className="hidden md:block md:w-64 border-r border-gray-200 bg-white">
      <div className="p-4">
        <div className="text-sm font-medium text-gray-500 mb-2">Menu</div>
        <nav className="space-y-1">
          <NavLink to="/dashboard" className={linkClass}>Overview</NavLink>
          <NavLink to="/bots" className={linkClass}>Bots</NavLink>
          <NavLink to="/analytics" className={linkClass}>Analytics</NavLink>
          <NavLink to="/alerts" className={linkClass}>Alerts</NavLink>
          <NavLink to="/profile" className={linkClass}>Settings</NavLink>
        </nav>
      </div>
    </aside>
  )
}

export default Sidebar


