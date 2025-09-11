import React from 'react';

const Footer = () => (
  <footer className="w-full bg-green-700 text-white py-4 mt-12 text-center shadow-inner">
    <div className="container mx-auto flex flex-col md:flex-row items-center justify-between px-4">
      <span className="font-semibold">Intelligent Pesticide Sprinkling System Dashboard</span>
      <span className="text-sm mt-2 md:mt-0">&copy; {new Date().getFullYear()} SIH Project | Made by Team CropSentinal for Sustainable Agriculture</span>
    </div>
  </footer>
);

export default Footer;
