import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import fs from 'fs'
import path from 'path'

// Copy images from old PWA to React automatically
const srcDir = path.resolve(process.cwd(), '../museum-pwa/public');
const destDir = path.resolve(process.cwd(), 'public');
if (fs.existsSync(srcDir)) {
  if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });
  fs.readdirSync(srcDir).forEach(file => {
    if (file.match(/\.(png|jpe?g|gif|svg|webp|ico)$/i)) {
      const srcFile = path.join(srcDir, file);
      const destFile = path.join(destDir, file);
      if (!fs.existsSync(destFile)) {
        fs.copyFileSync(srcFile, destFile);
      }
    }
  });
}

// https://vite.dev/config/
export default defineConfig({
  base: '/sodam-web/',
  build: {
    outDir: 'dist/sodam-web'
  },
  plugins: [
    tailwindcss(),
    react()
  ],
  server: {
    host: '0.0.0.0', // Allows network access
    allowedHosts: true // Prevents "Invalid Host header" when using tunnels
  }
})
