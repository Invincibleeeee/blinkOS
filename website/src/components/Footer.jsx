
// ============================================
// FILE: src/components/Footer.jsx
// ============================================
import React from 'react';
import { Eye, Github, Twitter, Heart } from 'lucide-react';

const Footer = () => (
  <footer className="relative bg-black border-t border-white/10 py-12">
    <div className="max-w-6xl mx-auto px-6">
      <div className="grid md:grid-cols-3 gap-12 mb-8">
        {/* Brand Section */}
        <div className="flex flex-col items-center md:items-start">
          <div className="flex items-center space-x-2 mb-3 group cursor-pointer">
            <Eye className="w-5 h-5 text-white transition-opacity duration-200 group-hover:opacity-70" />
            <span className="text-sm font-medium text-white">
              Blink OS
            </span>
          </div>
          <p className="text-xs text-neutral-500 text-center md:text-left max-w-xs leading-relaxed">
            Empowering the world through accessible iris tracking technology
          </p>
        </div>

        {/* Quick Links */}
        <div className="flex flex-col items-center">
          <h3 className="text-white text-xs font-medium mb-3 uppercase tracking-wider">Quick Links</h3>
          <div className="flex flex-wrap justify-center gap-4 text-xs">
            {['Privacy Policy', 'Terms of Service', 'Documentation', 'Support'].map((link, index) => (
              <a 
                key={index}
                href="#" 
                className="text-neutral-500 hover:text-white transition-colors duration-200"
              >
                {link}
              </a>
            ))}
          </div>
        </div>

        {/* Social Links */}
        <div className="flex flex-col items-center md:items-end">
          <h3 className="text-white text-xs font-medium mb-3 uppercase tracking-wider">Connect</h3>
          <div className="flex space-x-3">
            <a 
              href="https://github.com/Invincibleeeee/blinkOS"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-lg bg-white/5 text-neutral-400 hover:text-white hover:bg-white/10 transition-all duration-200"
            >
              <Github className="w-4 h-4" />
            </a>
            <a 
              href="#"
              className="p-2 rounded-lg bg-white/5 text-neutral-400 hover:text-white hover:bg-white/10 transition-all duration-200"
            >
              <Twitter className="w-4 h-4" />
            </a>
          </div>
        </div>
      </div>

      {/* Divider */}
      <div className="h-px bg-white/10 mb-6"></div>

      {/* Bottom Section */}
      <div className="flex flex-col md:flex-row justify-between items-center text-xs">
        <p className="text-neutral-500 mb-4 md:mb-0 flex items-center gap-2">
          © 2025 Blink OS. Made with 
          <Heart className="w-3 h-3 text-white inline" fill="currentColor" />
          for accessibility
        </p>
        <div className="flex items-center gap-2 text-neutral-500">
          <span>Powered by</span>
          <span className="font-medium text-white">
            Computer Vision & AI
          </span>
        </div>
      </div>
    </div>
  </footer>
);

export default Footer;