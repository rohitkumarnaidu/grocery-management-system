// frontend/src/components/SearchBar.jsx
// A controlled search bar component with a search icon and a clear button (X)

import React from 'react';
import { Search, X } from 'lucide-react';
import { Input } from '@/components/ui/input';

/**
 * SearchBar - controlled search input component.
 * @param {string} value - current search query
 * @param {function} onSearch - callback called with the search query on changes
 * @param {string} [placeholder] - input placeholder text
 */
export default function SearchBar({ value, onSearch, placeholder = "Search products..." }) {
  const handleChange = (e) => {
    onSearch(e.target.value);
  };

  const handleClear = () => {
    onSearch('');
  };

  return (
    <div className="relative w-full max-w-md">
      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400 dark:text-slate-500">
        <Search className="h-4 w-4" />
      </div>
      <Input
        type="text"
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        className="pl-10 pr-10 w-full h-11 bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-100 rounded-xl focus:border-violet-400 dark:focus:border-violet-500 focus:ring-1 focus:ring-violet-400 dark:focus:ring-violet-500 placeholder:text-slate-400 dark:placeholder:text-slate-500"
      />
      {value && (
        <button
          onClick={handleClear}
          type="button"
          aria-label="Clear search"
          className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-600 dark:text-slate-500 dark:hover:text-slate-300 transition-colors"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}
