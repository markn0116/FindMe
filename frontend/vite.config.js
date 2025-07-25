import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // ← これで '@' が 'src/' に
    },
  },
  server: {
    port: 5173,     // ★ ここでポートを固定
    host: true,     // ★ Dockerホストからのアクセスも許可
    proxy: {
      '/api': {
        target: 'http://backend:8000',  // コンテナ名ベースでつなぐ
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  }
})
