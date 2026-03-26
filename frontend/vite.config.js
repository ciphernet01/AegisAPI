import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
            '@components': path.resolve(__dirname, './src/components'),
            '@pages': path.resolve(__dirname, './src/pages'),
            '@hooks': path.resolve(__dirname, './src/hooks'),
            '@services': path.resolve(__dirname, './src/services'),
            '@types': path.resolve(__dirname, './src/types'),
            '@styles': path.resolve(__dirname, './src/styles'),
            '@context': path.resolve(__dirname, './src/context'),
        },
    },
    server: {
        port: 3000,
        proxy: {
            '/api': {
                target: process.env.VITE_API_URL || 'http://localhost:8000',
                changeOrigin: true,
                // Keep the /api prefix so backend receives /api/v1/... without stripping
                rewrite: function (path) { return path; },
            },
        },
    },
    build: {
        outDir: 'dist',
        sourcemap: false,
        minify: 'terser',
    },
});
