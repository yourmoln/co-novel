<template>
  <div class="home">
    <el-row :gutter="20" class="content-row">
      <el-col :span="24">
        <el-card class="home-card">
          <template #header>
            <div class="card-header">
              <span>欢迎使用co-novel AI小说助手</span>
            </div>
          </template>
          <p>这是一个用AI辅助写小说的助手，帮助您创作精彩的小说内容。</p>
          <el-button type="primary" @click="goToCreate">开始创作</el-button>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="content-row">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>AI智能创作</span>
            </div>
          </template>
          <p>利用先进的AI技术，帮助您生成小说内容、标题和建议。</p>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>轻松创作</span>
            </div>
          </template>
          <p>直观的界面设计，让您的创作过程更加轻松愉快。</p>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>历史记录</span>
            </div>
          </template>
          <p>保存您的创作历史，方便随时回顾和继续创作。</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Home',
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
  padding: 20px;
}

.content-row {
  margin-bottom: 20px;
}

.home-card {
  text-align: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
