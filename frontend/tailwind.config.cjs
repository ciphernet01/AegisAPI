/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0066cc',
        'primary-dark': '#0052a3',
        secondary: '#00a6a6',
        danger: '#cc3333',
        warning: '#ff9500',
        success: '#00b34e',
      },
      fontFamily: {
        sans: ['Space Grotesk', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
