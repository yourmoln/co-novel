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
import { Notebook, House, EditPen } from '@element-plus/icons-vue'

export default defineComponent({
  name: 'App',
  components: {
    Notebook,
    House,
    EditPen
  }
})
</script>

<style lang="scss">
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
  color: #2c3e50;
  min-height: 100vh;
}

.app-container {
  min-height: 100vh;
  background: #ffffff;
}

// 头部样式
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  
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
  }
}

// 主内容区域
.main {
  padding: 0;
  min-height: calc(100vh - 180px);
  background: #f8f9fa;
}

// 底部样式
.footer {
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  color: white;
  padding: 20px;
  
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
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
  
  &:hover {
    background: #a8a8a8;
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
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  
  &:hover {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  }
}

.el-input {
  .el-input__wrapper {
    border-radius: 8px;
    transition: all 0.3s ease;
    
    &:hover {
      box-shadow: 0 2px 12px rgba(64, 158, 255, 0.15);
    }
  }
}

.el-select {
  .el-input__wrapper {
    border-radius: 8px;
  }
}
</style>
