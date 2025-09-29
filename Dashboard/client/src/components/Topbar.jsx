import React from 'react'
import { Link, NavLink } from 'react-router-dom'

const Topbar = () => {
  return (
    <header className="sticky top-0 z-30 w-full bg-white/80 backdrop-blur border-b border-gray-200">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center gap-2">
          <span className="inline-flex h-6 w-6 items-center justify-center rounded-md bg-blue-600 text-white font-bold">■</span>
          <span className="font-semibold">CropDoc</span>
        </Link>
        <nav className="hidden md:flex items-center gap-6 text-sm">
          <NavLink to="/dashboard" className={({isActive})=>`hover:text-gray-900 ${isActive? 'text-gray-900 font-semibold':'text-gray-600'}`}>Dashboard</NavLink>
          <NavLink to="/reports" className={({isActive})=>`hover:text-gray-900 ${isActive? 'text-gray-900 font-semibold':'text-gray-600'}`}>Reports</NavLink>
          <NavLink to="/settings" className={({isActive})=>`hover:text-gray-900 ${isActive? 'text-gray-900 font-semibold':'text-gray-600'}`}>Settings</NavLink>
        </nav>
        <div className="flex items-center gap-4">
          <button className="relative h-9 w-9 rounded-full bg-gray-100 flex items-center justify-center">
            <span className="absolute -top-0.5 -right-0.5 h-4 w-4 rounded-full bg-red-500 text-white text-[10px] leading-4">3</span>
            <span className="i-bell text-gray-600">🔔</span>
          </button>
          <div className="h-9 w-9 rounded-full bg-gray-300"/>
        </div>
      </div>
    </header>
  )
}

export default Topbar


