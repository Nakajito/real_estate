/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../templates/**/*.html",
    "../../templates/**/*.html",
    "../../**/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          charcoal: "#1F2937",
          teal: "#0F766E",
          emerald: "#166534",
          blue: "#2563EB",
          gray: "#9CA3AF",
          grayLight: "#E5E7EB",
        },
      },
      fontFamily: {
        sans: ["Inter", "Montserrat", "ui-sans-serif", "system-ui"],
      },
      borderRadius: {
        card: "8px",
        btn: "6px",
        badge: "4px",
      },
      boxShadow: {
        card: "0 4px 6px -1px rgba(0,0,0,0.1)",
      },
    },
  },
  plugins: [],
};
