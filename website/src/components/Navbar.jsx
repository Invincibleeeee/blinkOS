// ============================================
// FILE: src/components/Navbar.jsx
// ============================================
import React, { useState, useEffect } from 'react';
import { Eye, Menu, X } from 'lucide-react';
import { Link } from './Router';

const Navbar = ({ currentPath }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { to: '/', label: 'Home' },
    { to: '/mission', label: 'Mission' },
    { to: '/how-it-works', label: 'How It Works' },
    { to: '/demo', label: 'Demo' },
    { to: '/applications', label: 'Applications' }
  ];

  return (
    <nav className={`fixed w-full z-50 transition-all duration-300 ${
      scrolled 
        ? 'bg-black/80 backdrop-blur-xl border-b border-white/10' 
        : 'bg-transparent'
    }`}>
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <Eye className="w-5 h-5 text-white transition-opacity duration-100 group-hover:opacity-70" />
            <span className="text-sm font-medium tracking-tight text-white">
              Blink OS
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map(link => (
              <Link
                key={link.to}
                to={link.to}
                className="relative py-2 group"
              >
                <span className={`text-xs font-medium tracking-wide transition-colors duration-100 ${
                  currentPath === link.to 
                    ? 'text-white' 
                    : 'text-neutral-400 group-hover:text-white'
                }`}>
                  {link.label}
                </span>
                {/* Minimal underline */}
                <span className={`absolute bottom-0 left-0 w-full h-px bg-white transform origin-left transition-transform duration-100 ${
                  currentPath === link.to ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'
                }`}></span>
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <button 
            onClick={() => setMobileOpen(!mobileOpen)} 
            className="md:hidden p-2 text-white hover:opacity-70 transition-opacity duration-100"
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <div className="md:hidden absolute top-full left-0 w-full bg-black/95 backdrop-blur-xl border-b border-white/10">
          <div className="px-6 py-4 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`block px-3 py-2 rounded text-sm font-medium transition-colors duration-100 ${
                  currentPath === link.to 
                    ? 'text-white bg-white/5' 
                    : 'text-neutral-400 hover:text-white hover:bg-white/5'
                }`}
                onClick={() => setMobileOpen(false)}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;