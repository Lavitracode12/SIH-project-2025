import React from 'react';

const Notifications = ({ notifications }) => (
  <section className="bg-white rounded-xl shadow p-6 border border-green-200 max-w-2xl mx-auto">
    <h2 className="text-xl font-semibold text-green-600 mb-4">Notifications</h2>
    <ul className="space-y-2">
      {notifications && notifications.length > 0 ? (
        notifications.map((note, idx) => (
          <li key={idx} className="text-green-800">{note}</li>
        ))
      ) : (
        <li className="text-gray-500">No notifications</li>
      )}
    </ul>
  </section>
);

export default Notifications;
