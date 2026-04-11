/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./base/templates/**/*.html",
    "./item/templates/**/*.html",
    "./templates/**/*.html",
    "./**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f8f6f2",
          100: "#f2ede4",
          200: "#e9dcc5",
          300: "#dfca9f",
          400: "#d5b876",
          500: "#c79d4c",
          600: "#a8833f",
          700: "#876937",
          800: "#6f5630",
          900: "#5d492c",
        },
        secondary: {
          50: "#faf7f3",
          100: "#f4ede4",
          200: "#e8dccb",
          300: "#dbc7ae",
          400: "#c9a988",
          500: "#b98f68",
          600: "#9f7552",
          700: "#825d45",
          800: "#6b4d3c",
          900: "#5a4135",
        },
        success: {
          50: "#eefbf3",
          500: "#22a06b",
          700: "#156f4a",
        },
        warning: {
          50: "#fffaeb",
          500: "#d78f00",
          700: "#9b5f00",
        },
        danger: {
          50: "#fff1f1",
          500: "#dc4c64",
          700: "#a73549",
        },
        neutral: {
          50: "#f8f8f7",
          100: "#f1f1ef",
          200: "#e4e3de",
          300: "#d2d0c8",
          400: "#a5a197",
          500: "#7b766a",
          600: "#5f5a4f",
          700: "#464237",
          800: "#343027",
          900: "#26231d",
        },
      },
      fontFamily: {
        heading: ['"Cormorant Garamond"', "ui-serif", "Georgia", "serif"],
        body: ["Inter", "ui-sans-serif", "system-ui", "Segoe UI", "Arial", "sans-serif"],
        arabic: ["Cairo", "ui-sans-serif", "system-ui", "Segoe UI", "Arial", "sans-serif"],
      },
      spacing: {
        18: "4.5rem",
      },
      borderRadius: {
        xl2: "1.25rem",
      },
      boxShadow: {
        soft: "0 10px 30px rgba(38,35,29,0.08)",
      },
      typography: {
        DEFAULT: {
          css: {
            color: "#464237",
          },
        },
      },
    },
  },
  plugins: [],
};
