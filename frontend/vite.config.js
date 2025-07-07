// frontend/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { configDefaults } from 'vitest/config';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,       // ✅ Enables `test`, `expect`, etc. without import
    environment: 'jsdom' // ✅ Needed for testing React components
  },
});
