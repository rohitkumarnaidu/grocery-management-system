import React from 'react';
import './UiverseButton.css';

export default function UiverseButton({ children, className = '', ...props }) {
  return (
    <button className={`uiverse-btn ${className}`} {...props}>
      {children}
    </button>
  );
}
