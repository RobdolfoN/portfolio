/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./portfolioapp/**/*.{html,js}"],
  theme: {
    extend: {
      width: {
        'custom': '400rem',  // 800px if 1rem = 16px
        '80': '20rem'  // Adds a custom width of 20rem
      },
      // height: {
      //   'custom': '50rem',  // 800px if 1rem = 16px
      // },
    },
  },
  plugins: [],
}