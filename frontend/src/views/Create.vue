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
      <div v-if="isStreaming" class="streaming-content">
        <div class="streaming-text">{{ streamingContent }}</div>
      </div>
      <div v-else-if="aiResult" class="streaming-content">
        <div class="streaming-text">{{ aiResult?.content }}</div>
      </div>
      <!-- <el-alert
        v-else-if="aiResult"
        :title="aiResult?.title || ''"
        :description="aiResult?.content || ''"
        type="success"
        show-icon
      ></el-alert> -->
      <div v-else class="empty-result">
        <p>点击按钮生成内容</p>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'

export default defineComponent({
  name: 'Create',
  setup() {
    const novelForm = ref({
      genre: '',
      theme: '',
      content: ''
    })
    
    const aiResult = ref<any>(null)
    
    const loading = ref(false)
    const streamingContent = ref('')
    const isStreaming = ref(false)
    const abortController = ref<AbortController | null>(null)
    
    // 配置API基础URL
    const API_BASE_URL = 'http://localhost:8000/api/ai'
    
    const generateTitle = async () => {
      if (!novelForm.value.genre || !novelForm.value.theme) {
        ElMessage.warning('请填写小说类型和主题')
        return
      }
      
      loading.value = true
      try {
        const response = await fetch(`${API_BASE_URL}/generate-title`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            genre: novelForm.value.genre,
            theme: novelForm.value.theme
          })
        })
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        aiResult.value = {
          title: data.title,
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
      streamingContent.value = ''
      isStreaming.value = true
      aiResult.value = null
      
      // 创建AbortController用于取消请求
      abortController.value = new AbortController()
      
      try {
        // 使用流式API
        const response = await fetch(`${API_BASE_URL}/generate-content-stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            prompt: `请为${novelForm.value.genre}类型的小说，主题是${novelForm.value.theme}，生成一段内容。`,
            max_tokens: 500
          }),
          signal: abortController.value.signal
        })
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        // 处理SSE格式的流式响应
        if (response.body) {
          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let fullContent = '';
          
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n\n');
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const jsonData = line.substring(6); // 去掉 'data: ' 前缀
                try {
                  const parsed = JSON.parse(jsonData);
                  // 检查是否是结束标记
                  if (parsed.choices && parsed.choices[0] && parsed.choices[0].delta && parsed.choices[0].delta.content !== undefined) {
                    const content = parsed.choices[0].delta.content;
                    if (content !== null && content !== undefined) {
                      fullContent += content;
                      streamingContent.value = fullContent;
                    }
                  }
                } catch (e) {
                  console.error('解析JSON失败:', e);
                }
              }
            }
          }
        }
        
        aiResult.value = {
          title: aiResult.value?.title || `《${novelForm.value.genre}：${novelForm.value.theme}》`,
          content: streamingContent.value
        }
        ElMessage.success('内容生成成功')
      } catch (error: any) {
        if (error.name !== 'AbortError') {
          console.error('生成内容失败:', error)
          ElMessage.error('内容生成失败')
        }
      } finally {
        loading.value = false
        isStreaming.value = false
      }
    }
    
    const clearContent = () => {
      novelForm.value = {
        genre: '',
        theme: '',
        content: ''
      }
      aiResult.value = null
      streamingContent.value = ''
      // streamingLines.value = []
      if (abortController.value) {
        abortController.value.abort()
      }
    }
    
    onUnmounted(() => {
      if (abortController.value) {
        abortController.value.abort()
      }
    })
    
    return {
      novelForm,
      aiResult,
      loading,
      streamingContent,
      isStreaming,
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

.streaming-content {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.6;
  text-align: left;
}

.streaming-text {
  text-align: left;
}
</style>
