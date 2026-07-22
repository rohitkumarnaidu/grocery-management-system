// frontend/src/pages/NotFound.jsx
// 404 Not Found page — rendered when URL hash doesn't match any known route

import React from 'react';
import { Leaf, Home, LayoutDashboard } from 'lucide-react';

/**
 * NotFound — displayed for any unrecognised URL hash.
 * Uses hash-based navigation to return users to valid routes.
 */
export default function NotFound() {
  const goTo = (hash) => {
    window.location.hash = hash;
  };

  return (
    <div
      className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-violet-50/30 flex items-center justify-center relative overflow-hidden font-sans selection:bg-violet-200"
      role="main"
    >
      {/* Decorative background blobs — matches App.jsx pattern */}
      <div className="absolute inset-0 -z-10 pointer-events-none" aria-hidden="true">
        <div className="absolute top-[-15%] right-[-10%] w-[600px] h-[600px] bg-violet-200/30 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-15%] left-[-10%] w-[500px] h-[500px] bg-blue-100/40 rounded-full blur-[120px]" />
        <div className="absolute top-[50%] left-[50%] w-[400px] h-[400px] bg-amber-100/20 rounded-full blur-[100px]" />
      </div>

      <div className="text-center px-6 max-w-md w-full">
        {/* Glass card — matches App.jsx panel style */}
        <div className="bg-white/60 border border-slate-200/50 backdrop-blur-xl rounded-3xl p-10 shadow-sm">

          {/* Brand logo */}
          <div className="flex justify-center mb-6">
            <div className="w-14 h-14 bg-gradient-to-br from-violet-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-md shadow-violet-500/20">
              <Leaf className="w-7 h-7 text-white" strokeWidth={2.5} aria-hidden="true" />
            </div>
          </div>

          {/* 404 number */}
          <p
            className="text-8xl font-extrabold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent mb-2 leading-none"
            aria-hidden="true"
          >
            404
          </p>

          {/* Heading — h1 for proper hierarchy */}
          <h1 className="text-xl font-bold text-slate-800 mb-3">
            Page Not Found
          </h1>

          <p className="text-slate-500 text-sm leading-relaxed mb-8">
            The page you're looking for doesn't exist or has been moved.
          </p>

          {/* Navigation actions */}
          <nav className="flex flex-col gap-3" aria-label="Recovery navigation">
            <button
              onClick={() => goTo('#/shop')}
              aria-label="Go to the Shop"
              className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-violet-600 to-purple-600 text-white font-semibold text-sm shadow-md shadow-violet-500/20 hover:opacity-90 active:scale-[0.98] transition-all duration-200"
            >
              <Home className="w-4 h-4" aria-hidden="true" />
              Go to Shop
            </button>

            <button
              onClick={() => goTo('#/admin')}
              aria-label="Go to Admin Dashboard"
              className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-xl border border-slate-200 text-slate-600 font-semibold text-sm hover:bg-violet-50 hover:text-violet-700 hover:border-violet-200 active:scale-[0.98] transition-all duration-200"
            >
              <LayoutDashboard className="w-4 h-4" aria-hidden="true" />
              Go to Admin Dashboard
            </button>
          </nav>

        </div>
      </div>
    </div>
  );
}
