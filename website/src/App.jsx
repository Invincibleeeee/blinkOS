import React from 'react';
import { Router } from './components/Router';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/Home';
import MissionPage from './pages/Mission';
import HowItWorksPage from './pages/HowItWorks';
import DemoPage from './pages/Demo';
import ApplicationsPage from './pages/Applications';

const App = () => {
  return (
    <Router>
      {({ currentPath }) => (
        <div className="min-h-screen bg-black text-white font-sans">
          <Navbar currentPath={currentPath} />
          
          {/* Traditional page rendering */}
          {currentPath === '/mission' && <MissionPage />}
          {currentPath === '/how-it-works' && <HowItWorksPage />}
          {currentPath === '/demo' && <DemoPage />}
          {currentPath === '/applications' && <ApplicationsPage />}
          {currentPath === '/' && <HomePage />}
          
          <Footer />
        </div>
      )}
    </Router>
  );
};

export default App;
