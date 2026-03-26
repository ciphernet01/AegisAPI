/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Monochromatic Grey/White/Black Palette
        // Dark Mode
        'dark-bg': '#0d1117',
        'dark-surface-1': '#161b22',
        'dark-surface-2': '#21262d',
        'dark-surface-3': '#30363d',
        'dark-border': '#30363d',
        'dark-text-primary': '#e6edf3',
        'dark-text-secondary': '#8b949e',
        // Light Mode
        'light-bg': '#ffffff',
        'light-surface-1': '#f6f8fa',
        'light-surface-2': '#fafbfc',
        'light-border': '#d0d7de',
        'light-text-primary': '#24292f',
        'light-text-secondary': '#57606a',
      },
      fontFamily: {
        sans: ['Space Grotesk', 'Segoe UI', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
