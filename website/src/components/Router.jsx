// ============================================
// FILE: src/components/Router.jsx
// ============================================
import React, { useState, useEffect } from 'react';

export const Router = ({ children }) => {
  const [currentPath, setCurrentPath] = useState(window.location.pathname || '/');
  
  useEffect(() => {
    // Handle navigation events
    const handleNavigation = (e) => {
      if (e.detail?.path) {
        setCurrentPath(e.detail.path);
        window.history.pushState({}, '', e.detail.path);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    };
    
    // Handle browser back/forward buttons
    const handlePopState = () => {
      setCurrentPath(window.location.pathname);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };
    
    window.addEventListener('navigate', handleNavigation);
    window.addEventListener('popstate', handlePopState);
    
    return () => {
      window.removeEventListener('navigate', handleNavigation);
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  // Support both render props pattern and children cloning
  if (typeof children === 'function') {
    return children({ currentPath, setCurrentPath });
  }

  return React.Children.map(children, child =>
    React.cloneElement(child, { currentPath, setCurrentPath })
  );
};

export const Link = ({ to, children, className = '', onClick }) => {
  const handleClick = (e) => {
    e.preventDefault();
    window.dispatchEvent(new CustomEvent('navigate', { detail: { path: to } }));
    if (onClick) onClick();
  };
  return <a href={to} onClick={handleClick} className={className}>{children}</a>;
};
