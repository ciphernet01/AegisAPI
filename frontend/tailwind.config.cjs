/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          950: '#05070c'
        }
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(99, 102, 241, 0.25), 0 8px 30px rgba(99, 102, 241, 0.15)'
      },
      animation: {
        'fade-up': 'fadeUp 0.5s ease-out'
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: 0, transform: 'translateY(8px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' }
        }
      }
    }
  },
  plugins: []
};
