/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './app.vue',
  ],
  theme: {
    extend: {
      colors: {
        paper: '#F7F3EA',
        sand: '#F4EDE4',
        ink: '#172026',
        forest: '#1B4332',
        trust: '#2C7DA0',
        scan: '#00C2D1',
        night: '#07131F',
        primary: '#07131F',
        panel: '#112131',
        accent: '#00C2D1',
        action: '#FF8A00',
        body: '#ffffff',
        muted: '#5F6F78',
        placeholder: '#75848D',
      },
      fontFamily: {
        heading: ['Outfit', 'Inter', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'Courier New', 'monospace'],
      },
      maxWidth: {
        site: '1400px',
      },
      boxShadow: {
        cyan: '0 18px 45px rgba(0, 194, 209, 0.16)',
        orange: '0 16px 36px rgba(255, 138, 0, 0.26)',
        soft: '0 18px 50px rgba(23, 32, 38, 0.10)',
      },
    },
  },
  plugins: [],
};
