// frontend/src/components/ui/ExportButton.jsx
// A generic export button showing loading spinners, success toasts, and error alerts

import React, { useState } from 'react';
import { Download, Loader2, CheckCircle2, AlertCircle } from 'lucide-react';
import { downloadCsv } from '@/lib/export';

/**
 * ExportButton - initiates a file download and displays self-dismissing toast status alerts.
 * @param {string} label - button text
 * @param {string} endpoint - API endpoint to download from
 * @param {string} filename - target name of the saved file
 */
export default function ExportButton({ label, endpoint, filename }) {
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null); // { type: 'success' | 'error', message: string }

  const handleDownload = async () => {
    setLoading(true);
    setToast(null);
    try {
      await downloadCsv(endpoint, filename);
      setToast({ type: 'success', message: 'CSV downloaded successfully!' });
      setTimeout(() => setToast(null), 3000);
    } catch (err) {
      setToast({ type: 'error', message: err.message || 'Failed to download CSV' });
      setTimeout(() => setToast(null), 4000);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={handleDownload}
        disabled={loading}
        className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-sm font-semibold hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 transition-all duration-200 shadow-sm"
      >
        {loading ? (
          <Loader2 className="w-4 h-4 animate-spin text-violet-600 dark:text-violet-400" />
        ) : (
          <Download className="w-4 h-4 text-violet-600 dark:text-violet-400" />
        )}
        {label}
      </button>

      {/* Floating Toast Notification */}
      {toast && (
        <div 
          className={`fixed bottom-6 right-6 z-50 px-6 py-4 rounded-2xl shadow-lg flex items-center gap-3 text-white ${
            toast.type === 'success' ? 'bg-emerald-500 shadow-emerald-500/20' : 'bg-rose-500 shadow-rose-500/20'
          }`}
          role="alert"
        >
          {toast.type === 'success' ? (
            <CheckCircle2 className="w-5 h-5 text-white" />
          ) : (
            <AlertCircle className="w-5 h-5 text-white" />
          )}
          <span className="font-semibold text-sm">{toast.message}</span>
        </div>
      )}
    </>
  );
}
