// frontend/src/lib/theme.js
// Theme persistence utility — reads/writes the 'grocery-theme' localStorage key

/**
 * Returns the currently stored theme ('light' or 'dark').
 * Defaults to 'light' if no preference is saved.
 */
export function getTheme() {
  return localStorage.getItem('grocery-theme') || 'light';
}

/**
 * Persists the chosen theme and updates the <html> class immediately.
 * @param {'light' | 'dark'} theme
 */
export function setTheme(theme) {
  localStorage.setItem('grocery-theme', theme);
  document.documentElement.classList.toggle('dark', theme === 'dark');
}
