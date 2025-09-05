<template>
  <div class="home">
    <!-- 英雄区域 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">co-novel AI小说助手</h1>
        <p class="hero-subtitle">让AI成为您创作路上的最佳伙伴，释放无限想象力</p>
        <el-button type="primary" size="large" class="cta-button" @click="goToCreate">
          <el-icon class="mr-2"><EditPen /></el-icon>
          开始创作
        </el-button>
      </div>
      <div class="hero-decoration">
        <div class="floating-card">📖</div>
        <div class="floating-card delay-1">✨</div>
        <div class="floating-card delay-2">🖋️</div>
      </div>
    </div>
    
    <!-- 功能特色区域 -->
    <div class="features-section">
      <h2 class="section-title">核心功能</h2>
      <el-row :gutter="30" class="features-row">
        <el-col :xs="24" :sm="12" :md="8">
          <div class="feature-card">
            <div class="feature-icon ai-icon">
              <el-icon><MagicStick /></el-icon>
            </div>
            <h3>AI智能创作</h3>
            <p>基于先进的AI技术，为您生成高质量的小说内容、精彩标题和创作建议</p>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <div class="feature-card">
            <div class="feature-icon design-icon">
              <el-icon><Compass /></el-icon>
            </div>
            <h3>直观易用</h3>
            <p>简洁优雅的界面设计，让创作过程更加流畅，专注于内容而非复杂操作</p>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <div class="feature-card">
            <div class="feature-icon stream-icon">
              <el-icon><Connection /></el-icon>
            </div>
            <h3>实时流式生成</h3>
            <p>支持流式内容生成，实时展示AI创作过程，让灵感源源不断地涌现</p>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 快速开始区域 -->
    <div class="quick-start-section">
      <div class="quick-start-card">
        <h3>准备好开始您的创作之旅了吗？</h3>
        <p>只需几个简单步骤，就能创作出令人惊艳的小说内容</p>
        <el-button type="primary" size="large" @click="goToCreate" class="start-button">
          立即开始创作
        </el-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import { EditPen, MagicStick, Compass, Connection } from '@element-plus/icons-vue'

export default defineComponent({
  name: 'Home',
  components: {
    EditPen,
    MagicStick,
    Compass,
    Connection
  },
  setup() {
    const router = useRouter()
    
    const goToCreate = () => {
      router.push('/create')
    }
    
    return {
      goToCreate
    }
  }
})
</script>

<style scoped lang="scss">
.home {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: calc(100vh - 120px);
  padding: 0;
  overflow-x: hidden;
}

// 英雄区域
.hero-section {
  position: relative;
  padding: 80px 20px;
  text-align: center;
  color: white;
  overflow: hidden;
  
  .hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, #fff, #f0f9ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    
    @media (max-width: 768px) {
      font-size: 2.5rem;
    }
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    opacity: 0.9;
    line-height: 1.6;
  }
  
  .cta-button {
    padding: 16px 32px;
    font-size: 1.1rem;
    border-radius: 50px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
    
    .mr-2 {
      margin-right: 8px;
    }
  }
}

// 浮动装饰元素
.hero-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  
  .floating-card {
    position: absolute;
    font-size: 3rem;
    opacity: 0.1;
    animation: float 6s ease-in-out infinite;
    
    &:nth-child(1) {
      top: 20%;
      left: 10%;
    }
    
    &:nth-child(2) {
      top: 60%;
      right: 15%;
      animation-delay: -2s;
    }
    
    &:nth-child(3) {
      bottom: 20%;
      left: 20%;
      animation-delay: -4s;
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(10deg);
  }
}

// 功能特色区域
.features-section {
  padding: 80px 20px;
  background: white;
  
  .section-title {
    text-align: center;
    font-size: 2.5rem;
    color: #2c3e50;
    margin-bottom: 3rem;
    font-weight: 600;
  }
  
  .features-row {
    max-width: 1200px;
    margin: 0 auto;
  }
}

.feature-card {
  text-align: center;
  padding: 2rem;
  border-radius: 20px;
  transition: all 0.3s ease;
  height: 100%;
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  }
  
  .feature-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: white;
    
    &.ai-icon {
      background: linear-gradient(135deg, #667eea, #764ba2);
    }
    
    &.design-icon {
      background: linear-gradient(135deg, #f093fb, #f5576c);
    }
    
    &.stream-icon {
      background: linear-gradient(135deg, #4facfe, #00f2fe);
    }
  }
  
  h3 {
    font-size: 1.5rem;
    color: #2c3e50;
    margin-bottom: 1rem;
    font-weight: 600;
  }
  
  p {
    color: #6c757d;
    line-height: 1.6;
    font-size: 1rem;
  }
}

// 快速开始区域
.quick-start-section {
  padding: 60px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  
  .quick-start-card {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
    color: white;
    
    h3 {
      font-size: 2rem;
      margin-bottom: 1rem;
      font-weight: 600;
    }
    
    p {
      font-size: 1.1rem;
      opacity: 0.9;
      margin-bottom: 2rem;
      line-height: 1.6;
    }
    
    .start-button {
      padding: 16px 32px;
      font-size: 1.1rem;
      border-radius: 50px;
      background: white;
      color: #667eea;
      border: none;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        background: #f8f9fa;
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .hero-section {
    padding: 60px 20px;
    
    .hero-title {
      font-size: 2.5rem;
    }
    
    .hero-subtitle {
      font-size: 1rem;
    }
  }
  
  .features-section {
    padding: 60px 20px;
    
    .section-title {
      font-size: 2rem;
    }
  }
  
  .feature-card {
    margin-bottom: 2rem;
  }
  
  .quick-start-section {
    padding: 40px 20px;
    
    .quick-start-card h3 {
      font-size: 1.5rem;
    }
  }
}
</style>
