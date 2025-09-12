import React from 'react';
import Dashboard from './Components/Dashboard';
import Footer from './Components/Footer';
import Navbar from './Components/Navbar';


const App = () => {
  return (
    <>
    <Navbar/>
      <Dashboard />
      <Footer />
    </>
  );
}

export default App