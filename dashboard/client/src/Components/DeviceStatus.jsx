import React from 'react';

const DeviceStatus = ({ devices }) => (
  <section className="bg-white rounded-xl shadow p-6 border border-green-200">
    <h2 className="text-xl font-semibold text-green-600 mb-4">Device Status</h2>
    <ul className="space-y-2">
      {devices && devices.length > 0 ? (
        devices.map((device, idx) => (
          <li key={idx} className="flex justify-between items-center">
            <span>{device.name}</span>
            <span className={`px-2 py-1 rounded text-xs font-bold ${device.online ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
              {device.online ? 'Online' : 'Offline'}
            </span>
          </li>
        ))
      ) : (
        <li className="text-gray-500">No devices found</li>
      )}
    </ul>
  </section>
);

export default DeviceStatus;
