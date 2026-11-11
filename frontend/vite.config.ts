import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  // Read VITE_* variables from the shared .env at the repository root.
  // Vite only exposes variables prefixed with VITE_ to the browser bundle,
  // so backend secrets in the same file are never shipped to the client.
  envDir: '..',
  server: {
    // Must match CORS_ALLOWED_ORIGINS in .env (http://localhost:5173).
    port: 5173,
    strictPort: true,
  },
})
