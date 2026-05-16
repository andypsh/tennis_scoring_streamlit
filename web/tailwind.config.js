/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        court: {
          50: '#f0fdf4',
          500: '#16a34a',
          700: '#15803d',
        },
        smash: {
          50: '#fff7ed',
          500: '#f97316',
          600: '#ea580c',
          700: '#c2410c',
        },
      },
      fontFamily: {
        sans: ['"Noto Sans KR"', '"Pretendard"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
