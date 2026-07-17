// frontend/src/components/ThemeToggle.jsx
// Sun / Moon toggle button — persists theme preference to localStorage

import React from 'react';
import { Sun, Moon } from 'lucide-react';
import { getTheme, setTheme } from '@/lib/theme';

/**
 * ThemeToggle — renders a Sun icon in dark mode and a Moon icon in light mode.
 * Clicking it toggles the theme and saves the preference.
 */
export default function ThemeToggle() {
  const [theme, setThemeState] = React.useState(getTheme);

  const toggle = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    setThemeState(next);
  };

  return (
    <button
      onClick={toggle}
      aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
      title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
      className="p-2 rounded-xl border border-slate-200 dark:border-slate-700
                 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300
                 hover:bg-slate-50 dark:hover:bg-slate-700
                 transition-all duration-200 shadow-sm flex-shrink-0"
    >
      {theme === 'dark'
        ? <Sun className="w-4 h-4 text-amber-400" aria-hidden="true" />
        : <Moon className="w-4 h-4 text-slate-500" aria-hidden="true" />}
    </button>
  );
}
