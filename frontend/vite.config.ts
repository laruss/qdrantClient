import { defineConfig, PluginOption } from 'vite';
import UnoCSS from 'unocss/vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

// https://vitejs.dev/config/
export default defineConfig({
    server: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000/',
                changeOrigin: true,
                rewrite: path => path.replace(/^\/api/, ''),
            },
        },
    },
    plugins: [
        react(),
        UnoCSS(),
        tsconfigPaths() as PluginOption,
    ],
});
