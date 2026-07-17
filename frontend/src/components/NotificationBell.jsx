// frontend/src/components/NotificationBell.jsx
// A notification bell that listens to real-time socket events for stock levels

import React, { useState, useEffect, useRef } from 'react';
import { Bell, Trash2, CheckSquare } from 'lucide-react';
import { socket } from '@/lib/socket';

export default function NotificationBell() {
  const [alerts, setAlerts] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    // Connect to WebSocket server on mount
    socket.connect();

    // Listen for low stock notifications
    const handleLowStock = (data) => {
      const newAlert = {
        id: Math.random().toString(36).substr(2, 9),
        type: 'low',
        productName: data.product_name,
        remainingQty: data.remaining_qty,
        timestamp: new Date().toLocaleTimeString(),
        read: false
      };
      setAlerts(prev => [newAlert, ...prev]);
    };

    // Listen for out of stock notifications
    const handleOutStock = (data) => {
      const newAlert = {
        id: Math.random().toString(36).substr(2, 9),
        type: 'out',
        productName: data.product_name,
        remainingQty: 0,
        timestamp: new Date().toLocaleTimeString(),
        read: false
      };
      setAlerts(prev => [newAlert, ...prev]);
    };

    socket.on('stock:low', handleLowStock);
    socket.on('stock:out', handleOutStock);

    // Click outside listener to close dropdown
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      socket.off('stock:low', handleLowStock);
      socket.off('stock:out', handleOutStock);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const unreadCount = alerts.filter(a => !a.read).length;

  const markAllAsRead = () => {
    setAlerts(prev => prev.map(a => ({ ...a, read: true })));
  };

  const clearAllAlerts = () => {
    setAlerts([]);
  };

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Bell Button Icon */}
      <button
        onClick={handleToggle}
        aria-label="Stock alerts notifications"
        className="relative p-2.5 rounded-xl border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition-all duration-200 shadow-sm flex items-center justify-center"
      >
        <Bell className="w-4 h-4 text-slate-500" />
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 w-2 h-2 bg-rose-500 rounded-full animate-ping" />
        )}
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 w-2 h-2 bg-rose-500 rounded-full" />
        )}
      </button>

      {/* Notifications Dropdown Panel */}
      {isOpen && (
        <div className="absolute right-0 mt-3 w-80 bg-white/95 backdrop-blur-xl border border-slate-200/80 rounded-2xl shadow-xl z-50 overflow-hidden animate-in fade-in slide-in-from-top-3 duration-200">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 bg-slate-50 border-b border-slate-100">
            <span className="text-sm font-bold text-slate-800 flex items-center gap-1.5">
              🔔 Stock Alerts
              {unreadCount > 0 && (
                <span className="bg-rose-100 text-rose-600 text-[11px] font-extrabold px-2 py-0.5 rounded-full">
                  {unreadCount} new
                </span>
              )}
            </span>
            <div className="flex gap-2">
              {alerts.length > 0 && (
                <button
                  onClick={markAllAsRead}
                  title="Mark all as read"
                  className="text-slate-400 hover:text-violet-600 p-1 rounded transition-colors"
                >
                  <CheckSquare className="w-3.5 h-3.5" />
                </button>
              )}
              {alerts.length > 0 && (
                <button
                  onClick={clearAllAlerts}
                  title="Clear all alerts"
                  className="text-slate-400 hover:text-rose-500 p-1 rounded transition-colors"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>

          {/* List items */}
          <div className="max-h-64 overflow-y-auto divide-y divide-slate-100">
            {alerts.length === 0 ? (
              <div className="py-10 text-center text-slate-400 text-xs font-medium flex flex-col items-center gap-2">
                <span className="text-xl">📭</span>
                <p>No alerts yet</p>
              </div>
            ) : (
              alerts.map(alert => (
                <div
                  key={alert.id}
                  className={`p-3.5 flex flex-col gap-1 transition-colors ${
                    alert.read ? 'bg-white opacity-85' : 'bg-violet-50/20'
                  }`}
                >
                  <div className="flex justify-between items-start gap-2">
                    <span className="font-semibold text-slate-700 capitalize text-sm">
                      {alert.productName}
                    </span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        alert.type === 'out'
                          ? 'bg-rose-100 text-rose-600'
                          : 'bg-amber-100 text-amber-600'
                      }`}
                    >
                      {alert.type === 'out' ? 'Out of Stock' : 'Low Stock'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-xs mt-1 text-slate-400">
                    <span>
                      {alert.type === 'out'
                        ? 'Needs immediate refill'
                        : `Only ${alert.remainingQty} units remaining`}
                    </span>
                    <span className="text-[10px] font-medium">{alert.timestamp}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
