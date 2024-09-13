/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './brreg_api/templates/*.html',
    './theme/src/*.css',
    './theme/**/**/*.css',
    './**/*.py',  
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
