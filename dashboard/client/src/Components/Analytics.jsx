
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const dummyData = [
  { name: 'Mon', healthy: 40, mild: 10, infected: 5 },
  { name: 'Tue', healthy: 38, mild: 12, infected: 7 },
  { name: 'Wed', healthy: 35, mild: 15, infected: 10 },
  { name: 'Thu', healthy: 30, mild: 18, infected: 12 },
  { name: 'Fri', healthy: 32, mild: 14, infected: 8 },
  { name: 'Sat', healthy: 36, mild: 11, infected: 6 },
  { name: 'Sun', healthy: 39, mild: 9, infected: 4 },
];

const Analytics = () => (
  <section className="bg-white rounded-xl shadow p-6 border border-green-200">
    <h2 className="text-xl font-semibold text-green-600 mb-4">Analytics</h2>
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={dummyData}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="infected" fill="#ef4444" name="Infected" />
        <Bar dataKey="healthy" fill="#22c55e" name="Healthy" />
        <Bar dataKey="mild" fill="#fde047" name="Mildly Infected" />
      </BarChart>
    </ResponsiveContainer>
  </section>
);

export default Analytics;
