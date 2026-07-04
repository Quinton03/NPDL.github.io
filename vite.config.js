import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'node:path';

export default defineConfig({
  plugins: [react()],
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },
  build: {
    outDir: 'js',
    emptyOutDir: false,
    lib: {
      entry: resolve(__dirname, 'src/hero-fx.jsx'),
      name: 'HeroFx',
      formats: ['iife'],
      fileName: () => 'hero-fx.js',
    },
    rollupOptions: {
      output: {
        inlineDynamicImports: true,
      },
    },
  },
});
