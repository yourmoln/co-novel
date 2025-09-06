<template>
  <div id="app">
    <el-container class="app-container">
      <el-header class="header">
        <div class="header-content">
          <div class="logo-section">
            <el-icon class="logo-icon"><Notebook /></el-icon>
            <h1 class="app-title">co-novel</h1>
            <span class="app-subtitle">AI小说助手</span>
          </div>
          <nav class="nav-section">
            <router-link to="/" class="nav-link" active-class="active">
              <el-icon><House /></el-icon>
              首页
            </router-link>
            <router-link to="/create" class="nav-link" active-class="active">
              <el-icon><EditPen /></el-icon>
              创作
            </router-link>
            <button class="theme-toggle" @click="toggleTheme" :title="isDarkMode ? '切换到浅色模式' : '切换到深色模式'">
              <el-icon v-if="isDarkMode"><Sunny /></el-icon>
              <el-icon v-else><Moon /></el-icon>
            </button>
          </nav>
        </div>
      </el-header>
      
      <el-main class="main">
        <router-view/>
      </el-main>
      
      <el-footer class="footer">
        <div class="footer-content">
          <p>&copy; 2025 co-novel AI小说助手 - 用AI释放创作力</p>
          <div class="footer-links">
            <span>由❤️打造</span>
          </div>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Notebook, House, EditPen, Sunny, Moon } from '@element-plus/icons-vue'
import { useTheme } from './composables/useTheme'

export default defineComponent({
  name: 'App',
  components: {
    Notebook,
    House,
    EditPen,
    Sunny,
    Moon
  },
  setup() {
    const { toggleTheme, isDarkMode, initTheme } = useTheme()
    
    // 初始化主题
    initTheme()
    
    return {
      toggleTheme,
      isDarkMode
    }
  }
})
</script>

<style lang="scss">
// App.vue 的样式已迁移到单独的样式文件中
// 所有样式都在 src/styles/ 目录下进行管理
</style>
