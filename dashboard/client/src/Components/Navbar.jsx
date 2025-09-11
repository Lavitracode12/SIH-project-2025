import React from 'react';

const Navbar = () => (
  <nav className="w-full bg-green-700 text-white py-4 shadow flex items-center justify-center">
    <div className="container mx-auto flex flex-col md:flex-row items-center justify-between px-4">
      <span className="font-bold text-lg tracking-wide">Plant Health Dashboard</span>
      <ul className="flex gap-6 mt-2 md:mt-0">
        <li><a href="#overview" className="hover:underline">Overview</a></li>
        <li><a href="#sprayer" className="hover:underline">Sprayer Control</a></li>
        <li><a href="#visualization" className="hover:underline">Visualization</a></li>
        <li><a href="#analytics" className="hover:underline">Analytics</a></li>
        <li><a href="#notifications" className="hover:underline">Notifications</a></li>
      </ul>
    </div>
  </nav>
);

export default Navbar;
