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
// Home.vue 的样式已迁移到单独的样式文件中
// 所有样式都在 src/styles/home.scss 中进行管理
</style>
