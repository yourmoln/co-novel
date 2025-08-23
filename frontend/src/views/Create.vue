<template>
  <div class="create-page">
    <el-card class="create-card">
      <template #header>
        <div class="card-header">
          <span>小说创作</span>
        </div>
      </template>
      <el-form :model="novelForm" label-width="100px">
        <el-form-item label="小说类型">
          <el-select v-model="novelForm.genre" placeholder="请选择小说类型">
            <el-option label="玄幻" value="玄幻"></el-option>
            <el-option label="都市" value="都市"></el-option>
            <el-option label="科幻" value="科幻"></el-option>
            <el-option label="武侠" value="武侠"></el-option>
            <el-option label="言情" value="言情"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="主题">
          <el-input v-model="novelForm.theme" placeholder="请输入小说主题"></el-input>
        </el-form-item>
        
        <el-form-item label="内容">
          <el-input
            v-model="novelForm.content"
            type="textarea"
            :rows="10"
            placeholder="请输入小说内容"
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="generateTitle" :loading="loading">生成标题</el-button>
          <el-button type="success" @click="generateContent" :loading="loading">生成内容</el-button>
          <el-button @click="clearContent">清空</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="result-card">
      <template #header>
        <div class="card-header">
          <span>AI生成结果</span>
        </div>
      </template>
      <el-alert
        v-if="aiResult"
        :title="aiResult.title"
        :description="aiResult.content"
        type="success"
        show-icon
      ></el-alert>
      <div v-else class="empty-result">
        <p>点击按钮生成内容</p>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default defineComponent({
  name: 'Create',
  setup() {
    const novelForm = ref({
      genre: '',
      theme: '',
      content: ''
    })
    
    const aiResult = ref<{
      title: string;
      content: string;
    } | null>(null)
    
    const loading = ref(false)
    
    // 配置API基础URL
    const API_BASE_URL = 'http://localhost:8000/api/ai'
    
    const generateTitle = async () => {
      if (!novelForm.value.genre || !novelForm.value.theme) {
        ElMessage.warning('请填写小说类型和主题')
        return
      }
      
      loading.value = true
      try {
        const response = await axios.post(`${API_BASE_URL}/generate-title`, {
          genre: novelForm.value.genre,
          theme: novelForm.value.theme
        })
        aiResult.value = {
          title: response.data.title,
          content: '点击"生成内容"按钮生成小说内容'
        }
        ElMessage.success('标题生成成功')
      } catch (error) {
        console.error('生成标题失败:', error)
        ElMessage.error('标题生成失败')
      } finally {
        loading.value = false
      }
    }
    
    const generateContent = async () => {
      if (!novelForm.value.genre || !novelForm.value.theme) {
        ElMessage.warning('请填写小说类型和主题')
        return
      }
      
      loading.value = true
      try {
        const response = await axios.post(`${API_BASE_URL}/generate-content`, {
          prompt: `请为${novelForm.value.genre}类型的小说，主题是${novelForm.value.theme}，生成一段内容。`,
          max_tokens: 500
        })
        aiResult.value = {
          title: aiResult.value?.title || `《${novelForm.value.genre}：${novelForm.value.theme}》`,
          content: response.data.content
        }
        ElMessage.success('内容生成成功')
      } catch (error) {
        console.error('生成内容失败:', error)
        ElMessage.error('内容生成失败')
      } finally {
        loading.value = false
      }
    }
    
    const clearContent = () => {
      novelForm.value = {
        genre: '',
        theme: '',
        content: ''
      }
      aiResult.value = null
    }
    
    return {
      novelForm,
      aiResult,
      loading,
      generateTitle,
      generateContent,
      clearContent
    }
  }
})
</script>

<style scoped lang="scss">
.create-page {
  padding: 20px;
}

.create-card {
  margin-bottom: 20px;
}

.result-card {
  min-height: 200px;
}

.empty-result {
  text-align: center;
  padding: 40px 0;
  color: #999;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
