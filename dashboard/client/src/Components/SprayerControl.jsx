import React from 'react';

const SprayerControl = ({ status, onStart, onStop }) => (
  <section className="bg-white rounded-xl shadow p-6 border border-green-200">
    <h2 className="text-xl font-semibold text-green-600 mb-4">Sprayer Control</h2>
    <div className="flex gap-4 mb-2">
      <button
        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
        onClick={onStart}
        disabled={status === 'active'}
      >
        Start Spraying
      </button>
      <button
        className="px-4 py-2 bg-gray-300 text-green-700 rounded hover:bg-green-200 transition"
        onClick={onStop}
        disabled={status === 'inactive'}
      >
        Stop Spraying
      </button>
    </div>
    <div className="text-green-800">Status: <span className="font-bold">{status}</span></div>
  </section>
);

export default SprayerControl;
