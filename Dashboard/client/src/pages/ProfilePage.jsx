import React from 'react'
import DashboardLayout from '../layouts/DashboardLayout.jsx'
import Card, { CardHeader, CardContent } from '../components/Card.jsx'

const Input = ({ label, type='text', placeholder='' }) => (
  <label className="block">
    <div className="text-sm text-gray-600 mb-1">{label}</div>
    <input type={type} placeholder={placeholder} className="w-full h-10 rounded-md border border-gray-300 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500" />
  </label>
)

const Select = ({ label, children }) => (
  <label className="block">
    <div className="text-sm text-gray-600 mb-1">{label}</div>
    <select className="w-full h-10 rounded-md border border-gray-300 px-3">{children}</select>
  </label>
)

const Checkbox = ({ label, defaultChecked }) => (
  <label className="flex items-start gap-3 text-sm">
    <input type="checkbox" defaultChecked={defaultChecked} className="mt-1 h-4 w-4 rounded border-gray-300" />
    <span className="text-gray-700">{label}</span>
  </label>
)

const ProfilePage = () => {
  return (
    <DashboardLayout title="Profile" subtitle="Manage your account information, system preferences, and notification settings.">
      <Card>
        <CardHeader title="Account Information" />
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input label="Name" placeholder="John Doe" />
            <Input label="Email" placeholder="john.doe@example.com" type="email" />
          </div>
          <div className="mt-4">
            <Input label="Phone Number" placeholder="+1 234 567 890" />
          </div>
          <button className="mt-4 inline-flex items-center rounded-md bg-blue-600 text-white px-4 py-2">Update Account</button>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader title="System Preferences" />
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select label="Language">
              <option>English</option>
              <option>Spanish</option>
            </Select>
            <Select label="Time Zone">
              <option>(GMT-08:00) Pacific Time</option>
              <option>(GMT+05:30) India Standard Time</option>
            </Select>
          </div>
          <button className="mt-4 inline-flex items-center rounded-md bg-blue-600 text-white px-4 py-2">Update Preferences</button>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader title="Access Control" />
        <CardContent>
          <div className="grid grid-cols-1 gap-4">
            <Input label="Current Password" type="password" placeholder="Enter current password" />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input label="New Password" type="password" placeholder="Enter new password" />
              <Input label="Confirm New Password" type="password" placeholder="Confirm new password" />
            </div>
          </div>
          <button className="mt-4 inline-flex items-center rounded-md bg-blue-600 text-white px-4 py-2">Change Password</button>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader title="Notification Preferences" />
        <CardContent>
          <div className="space-y-3">
            <Checkbox label="Receive email notifications for system alerts" defaultChecked />
            <Checkbox label="Receive SMS notifications for critical alerts" />
            <Checkbox label="Receive in-app notifications for updates" defaultChecked />
          </div>
          <button className="mt-4 inline-flex items-center rounded-md bg-blue-600 text-white px-4 py-2">Update Notifications</button>
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}

export default ProfilePage


