/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  darkMode: "class",
  theme: {
    fontFamily: {
      display: ["Poppins", "sans-serif"],
      body: ["Poppins", "sans-serif"],
      secondary: ["Roboto", "sans-serif"],
    },
    extend: {
      fontSize: {
        12: "12px",
        14: "14px",
        16: "16px",
        20: "20px",
        24: "24px",
        28: "28px",
      },
      gridTemplateColumns: {
        24: "repeat(24, minmax(0, 1fr))",
      },
      backgroundColor: {
        "main-bg": "#FAFBFB",
        "secondary-main-bg": "#FAFBFF",
        "main-dark-bg": "#20232A",
        "secondary-dark-bg": "#33373E",
        "light-gray": "#F7F7F7",
        "dark-periwinkle": "#6169D0",
        "greenish-cyan": "#81D6BE",
        "cornflower-blue": "#5892FF",
        "half-transparent": "rgba(0, 0, 0, 0.5)",
        "dark-green-800": "#021B38",
        "dark-green-600": "#0D243F",
        "dark-green-400": "#192D45",
        "dark-green-300": "#24374C",
      },
      borderWidth: {
        1: "1px",
      },
      colors: {
        "shuttle-grey": "#576270",
        "dark-green-800": "#021B38",
      },
      borderColor: {
        color: "rgba(0, 0, 0, 0.1)",
      },
      width: {
        400: "400px",
        760: "760px",
        780: "780px",
        800: "800px",
        1000: "1000px",
        1200: "1200px",
        1400: "1400px",
      },
      minWidth: {
        "1/2": "50%",
        400: "400px",
        760: "760px",
        780: "780px",
        800: "800px",
        1000: "1000px",
        1200: "1200px",
        1400: "1400px",
      },
      screens: {
        xs: "480px",
        xxs: "320px",
        xxxl: "1600px",
        xxxxl: "1920px",
      },
      height: {
        80: "80px",
      },
      minHeight: {
        590: "590px",
      },
      backgroundImage: {
        "hero-pattern":
          "url('https://demos.wrappixel.com/premium-admin-templates/react/flexy-react/main/static/media/welcome-bg-2x-svg.25338f53.svg')",
      },
    },
  },
  plugins: [],
};
