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
// CSS 变量定义
:root {
  // 浅色模式变量
  --bg-color: #ffffff;
  --bg-secondary: #f8f9fa;
  --bg-tertiary: #f5f7fa;
  --text-primary: #2c3e50;
  --text-secondary: #6c757d;
  --text-muted: #8e8e93;
  --border-color: #e4e7ed;
  --border-light: #f1f1f1;
  --card-bg: #ffffff;
  --header-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --footer-bg: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  --shadow-light: rgba(0, 0, 0, 0.08);
  --shadow-medium: rgba(0, 0, 0, 0.12);
  --shadow-dark: rgba(0, 0, 0, 0.15);
  --primary-color: #409eff;
  --success-color: #67c23a;
  --warning-color: #e6a23c;
  --danger-color: #f56c6c;
  --info-color: #909399;
}

// 深色模式变量
[data-theme="dark"] {
  --bg-color: #1a1a1a;
  --bg-secondary: #2d2d2d;
  --bg-tertiary: #3a3a3a;
  --text-primary: #ffffff;
  --text-secondary: #e2e2e2;
  --text-muted: #999999;
  --border-color: #4a4a4a;
  --border-light: #3a3a3a;
  --card-bg: #2d2d2d;
  --header-bg: linear-gradient(135deg, #4a5568 0%, #553c9a 100%);
  --footer-bg: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
  --shadow-light: rgba(0, 0, 0, 0.3);
  --shadow-medium: rgba(0, 0, 0, 0.4);
  --shadow-dark: rgba(0, 0, 0, 0.5);
  --primary-color: #409eff;
  --success-color: #67c23a;
  --warning-color: #e6a23c;
  --danger-color: #f56c6c;
  --info-color: #909399;
}

// 全局重置
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text-primary);
  min-height: 100vh;
  background-color: var(--bg-color);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.app-container {
  min-height: 100vh;
  background: var(--bg-color);
  transition: background-color 0.3s ease;
}

// 头部样式
.header {
  background: var(--header-bg);
  color: white;
  padding: 0 20px;
  box-shadow: 0 4px 20px var(--shadow-light);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: box-shadow 0.3s ease;
  
  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1400px;
    margin: 0 auto;
    height: 100%;
  }
  
  .logo-section {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .logo-icon {
      font-size: 2rem;
      color: #fff;
    }
    
    .app-title {
      font-size: 1.8rem;
      font-weight: 700;
      margin: 0;
      background: linear-gradient(45deg, #fff, #f0f9ff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .app-subtitle {
      font-size: 0.9rem;
      opacity: 0.8;
      font-weight: 500;
    }
  }
  
  .nav-section {
    display: flex;
    align-items: center;
    gap: 20px;
    
    .nav-link {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 16px;
      border-radius: 25px;
      color: white;
      text-decoration: none;
      font-weight: 500;
      transition: all 0.3s ease;
      background: rgba(255, 255, 255, 0.1);
      
      &:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-1px);
      }
      
      &.active {
        background: rgba(255, 255, 255, 0.25);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
      }
      
      .el-icon {
        font-size: 1.1rem;
      }
    }
    
    .theme-toggle {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      border: none;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.15);
      color: white;
      cursor: pointer;
      transition: all 0.3s ease;
      
      &:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-1px) scale(1.05);
      }
      
      .el-icon {
        font-size: 1.2rem;
      }
    }
  }
}

// 主内容区域
.main {
  padding: 0;
  min-height: calc(100vh - 180px);
  background: var(--bg-secondary);
  transition: background-color 0.3s ease;
}

// 底部样式
.footer {
  background: var(--footer-bg);
  color: white;
  padding: 20px;
  transition: background-color 0.3s ease;
  
  .footer-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1400px;
    margin: 0 auto;
    
    p {
      margin: 0;
      font-size: 0.9rem;
      opacity: 0.9;
    }
    
    .footer-links {
      font-size: 0.9rem;
      opacity: 0.8;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .header {
    padding: 0 15px;
    
    .header-content {
      flex-direction: column;
      gap: 15px;
      padding: 10px 0;
    }
    
    .logo-section {
      .app-title {
        font-size: 1.5rem;
      }
      
      .app-subtitle {
        font-size: 0.8rem;
      }
    }
    
    .nav-section {
      gap: 15px;
      
      .nav-link {
        padding: 8px 12px;
        font-size: 0.9rem;
      }
    }
  }
  
  .footer {
    padding: 15px;
    
    .footer-content {
      flex-direction: column;
      gap: 10px;
      text-align: center;
      
      p, .footer-links {
        font-size: 0.8rem;
      }
    }
  }
}

@media (max-width: 480px) {
  .header {
    .logo-section {
      gap: 8px;
      
      .logo-icon {
        font-size: 1.5rem;
      }
      
      .app-title {
        font-size: 1.3rem;
      }
      
      .app-subtitle {
        display: none;
      }
    }
    
    .nav-section {
      .nav-link {
        padding: 6px 10px;
        font-size: 0.8rem;
        
        .el-icon {
          font-size: 1rem;
        }
      }
    }
  }
}

// 全局滚动条美化
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--border-light);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
  
  &:hover {
    background: var(--text-muted);
  }
}

// Element Plus 组件样式覆盖
.el-button {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-1px);
  }
}

.el-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 20px var(--shadow-light);
  background: var(--card-bg);
  transition: all 0.3s ease;
  
  &:hover {
    box-shadow: 0 8px 30px var(--shadow-medium);
  }
  
  :deep(.el-card__header) {
    background: var(--card-bg);
    border-bottom: 1px solid var(--border-color);
    color: var(--text-primary);
  }
  
  :deep(.el-card__body) {
    background: var(--card-bg);
    color: var(--text-primary);
  }
}

.el-input {
  :deep(.el-input__wrapper) {
    border-radius: 8px;
    transition: all 0.3s ease;
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    
    &:hover {
      box-shadow: 0 2px 12px rgba(64, 158, 255, 0.15);
    }
    
    .el-input__inner {
      color: var(--text-primary);
      
      &::placeholder {
        color: var(--text-muted);
      }
    }
  }
}

.el-select {
  :deep(.el-input__wrapper) {
    border-radius: 8px;
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
  }
}

.el-textarea {
  :deep(.el-textarea__inner) {
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    
    &::placeholder {
      color: var(--text-muted);
    }
  }
}

// 下拉菜单样式
.el-popper {
  background: var(--card-bg) !important;
  border: 1px solid var(--border-color) !important;
  box-shadow: 0 4px 20px var(--shadow-light) !important;
  
  .el-select-dropdown__item {
    color: var(--text-primary) !important;
    
    &:hover {
      background-color: var(--bg-secondary) !important;
    }
    
    &.selected {
      background-color: var(--primary-color) !important;
      color: white !important;
    }
  }
}

// 步骤条样式
.el-steps {
  :deep(.el-step__title) {
    color: var(--text-primary);
    transition: color 0.3s ease;
    
    &.is-finish {
      color: var(--primary-color);
    }
    
    &.is-process {
      color: var(--primary-color);
    }
  }
  
  :deep(.el-step__description) {
    color: var(--text-secondary);
    transition: color 0.3s ease;
  }
  
  :deep(.el-step__icon) {
    border-color: var(--border-color);
    color: var(--text-muted);
    transition: all 0.3s ease;
    
    &.is-text {
      background-color: var(--bg-secondary);
      border-color: var(--border-color);
    }
  }
  
  :deep(.el-step__line) {
    background-color: var(--border-color);
    transition: background-color 0.3s ease;
  }
}

// 消息提示样式
.el-message {
  background-color: var(--card-bg) !important;
  border: 1px solid var(--border-color) !important;
  color: var(--text-primary) !important;
  box-shadow: 0 4px 20px var(--shadow-light) !important;
}

// 标签样式
.el-tag {
  background-color: var(--bg-secondary) !important;
  border-color: var(--border-color) !important;
  color: var(--text-primary) !important;
  
  &.el-tag--info {
    background-color: var(--bg-tertiary) !important;
  }
  
  &.el-tag--success {
    background-color: rgba(103, 194, 58, 0.1) !important;
    border-color: var(--success-color) !important;
    color: var(--success-color) !important;
  }
}

// 加载指示器样式
.el-loading-mask {
  background-color: rgba(0, 0, 0, 0.5) !important;
}

[data-theme="dark"] .el-loading-mask {
  background-color: rgba(0, 0, 0, 0.8) !important;
}
</style>
