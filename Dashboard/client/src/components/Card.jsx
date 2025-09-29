import React from 'react'

const Card = ({ children, className="" }) => {
  return (
    <div className={`rounded-xl border border-gray-200 bg-white ${className}`}>
      {children}
    </div>
  )
}

export const CardHeader = ({ title, action }) => (
  <div className="px-5 pt-5 pb-3 flex items-center justify-between">
    <h3 className="font-semibold text-gray-900">{title}</h3>
    {action}
  </div>
)

export const CardContent = ({ children, className="px-5 pb-5" }) => (
  <div className={className}>{children}</div>
)

export default Card


