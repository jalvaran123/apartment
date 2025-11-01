/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f9f7fb',
          100: '#f3edf7',
          200: '#e6d9ef',
          300: '#d9c5e7',
          400: '#ccb1df',
          500: '#9D6DC2',
          600: '#7A3DB8',
          700: '#5A2D82',
          800: '#3d1e57',
          900: '#1f0f2b',
        },
      },
    },
  },
  plugins: [],
}

