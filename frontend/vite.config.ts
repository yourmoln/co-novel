import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    host: '0.0.0.0',
    port: 3000
  },
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern' // Vite 6 默认使用现代 Sass API
      }
    }
  },
  optimizeDeps: {
    include: ['@element-plus/icons-vue']
  }
})
