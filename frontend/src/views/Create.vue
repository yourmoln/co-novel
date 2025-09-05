<template>
  <div class="create-page">
    <div class="page-header">
      <h1>小说创作工作台</h1>
      <p>让AI成为您的创作伙伴，开始一段精彩的文学之旅</p>
    </div>

    <!-- 步骤指示器 -->
    <div class="steps-container">
      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="基础设置" description="设置类型和主题"></el-step>
        <el-step title="生成标题" description="AI生成小说标题"></el-step>
        <el-step title="创建大纲" description="AI生成章节大纲"></el-step>
        <el-step title="确认信息" description="编辑和确认内容"></el-step>
        <el-step title="生成第一章" description="开始创作之旅"></el-step>
      </el-steps>
    </div>
    
    <div class="create-container">
      <!-- 步骤1: 基础设置 -->
      <div v-if="currentStep === 0" class="step-content">
        <el-card class="form-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><Edit /></el-icon>
              <span>基础设置</span>
            </div>
          </template>
          
          <el-form :model="novelForm" label-position="top" class="create-form">
            <el-form-item label="小说类型" class="form-item">
              <el-select 
                v-model="novelForm.genre" 
                placeholder="选择您喜欢的类型" 
                class="genre-select"
                size="large"
              >
                <el-option label="🎆 玄幻" value="玄幻"></el-option>
                <el-option label="🏢 都市" value="都市"></el-option>
                <el-option label="🚀 科幻" value="科幻"></el-option>
                <el-option label="⚔️ 武侠" value="武侠"></el-option>
                <el-option label="💕 言情" value="言情"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="创作主题" class="form-item">
              <el-input 
                v-model="novelForm.theme" 
                placeholder="请输入您的小说主题或灵感..."
                size="large"
                class="theme-input"
              >
                <template #prefix>
                  <el-icon><Star /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            
            <div class="step-actions">
              <el-button 
                type="primary" 
                @click="nextStep" 
                size="large"
                :disabled="!novelForm.genre || !novelForm.theme"
              >
                下一步：生成标题
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </el-form>
        </el-card>
      </div>

      <!-- 步骤2: 生成标题 -->
      <div v-if="currentStep === 1" class="step-content">
        <el-card class="form-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><MagicStick /></el-icon>
              <span>生成标题</span>
            </div>
          </template>

          <div class="step-info">
            <p><strong>类型:</strong> {{ novelForm.genre }}</p>
            <p><strong>主题:</strong> {{ novelForm.theme }}</p>
          </div>

          <div v-if="!generatedTitle" class="generate-section">
            <el-button 
              type="primary" 
              @click="generateTitle" 
              :loading="loading"
              size="large"
              class="generate-btn"
            >
              <el-icon v-if="!loading"><MagicStick /></el-icon>
              生成标题
            </el-button>
          </div>

          <div v-else class="result-section">
            <h3>生成的标题：</h3>
            <div class="title-display">{{ generatedTitle }}</div>
            
            <div class="step-actions">
              <el-button @click="regenerateTitle" :loading="loading">
                <el-icon><Refresh /></el-icon>
                重新生成
              </el-button>
              <el-button type="primary" @click="nextStep" size="large">
                确认标题，下一步
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </div>

          <div class="step-navigation">
            <el-button @click="prevStep">
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 步骤3: 创建大纲 -->
      <div v-if="currentStep === 2" class="step-content">
        <el-card class="form-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><Document /></el-icon>
              <span>创建大纲</span>
            </div>
          </template>

          <div class="step-info">
            <p><strong>标题:</strong> {{ generatedTitle }}</p>
            <p><strong>类型:</strong> {{ novelForm.genre }} | <strong>主题:</strong> {{ novelForm.theme }}</p>
          </div>

          <div v-if="!generatedOutline" class="generate-section">
            <el-button 
              type="primary" 
              @click="generateOutline" 
              :loading="loading"
              size="large"
              class="generate-btn"
            >
              <el-icon v-if="!loading"><Document /></el-icon>
              流式生成大纲
            </el-button>
          </div>

          <!-- 流式生成大纲 -->
          <div v-if="isStreamingOutline" class="streaming-container">
            <h3>正在生成大纲：</h3>
            <div class="streaming-outline">
              <div class="streaming-text">{{ streamingOutlineContent }}</div>
              <div class="cursor-indicator"></div>
            </div>
          </div>

          <div v-else-if="generatedOutline" class="result-section">
            <h3>生成的大纲：</h3>
            <div class="outline-display">{{ generatedOutline }}</div>
            
            <div class="step-actions">
              <el-button @click="regenerateOutline" :loading="loading">
                <el-icon><Refresh /></el-icon>
                重新生成
              </el-button>
              <el-button type="primary" @click="nextStep" size="large">
                确认大纲，下一步
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </div>

          <div class="step-navigation">
            <el-button @click="prevStep">
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 步骤4: 确认信息 -->
      <div v-if="currentStep === 3" class="step-content">
        <el-card class="form-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><EditPen /></el-icon>
              <span>确认信息</span>
            </div>
          </template>

          <!-- 显示已生成的内容摘要 -->
          <div class="summary-section">
            <h3>创作信息摘要</h3>
            <div class="info-grid">
              <div class="info-item">
                <label>小说类型：</label>
                <span>{{ novelForm.genre }}</span>
              </div>
              <div class="info-item">
                <label>创作主题：</label>
                <span>{{ novelForm.theme }}</span>
              </div>
            </div>
          </div>

          <div class="confirm-section">
            <el-form label-position="top">
              <el-form-item label="小说标题">
                <el-input 
                  v-model="editableTitle" 
                  size="large"
                  placeholder="您可以编辑标题"
                />
                <div class="hint-text">原标题：{{ generatedTitle }}</div>
              </el-form-item>
              
              <el-form-item label="小说大纲">
                <el-input 
                  v-model="editableOutline" 
                  type="textarea"
                  :rows="8"
                  placeholder="您可以编辑大纲"
                  resize="vertical"
                />
                <div class="hint-text">可以在此处修改AI生成的大纲内容</div>
              </el-form-item>
            </el-form>
            
            <div class="step-actions">
              <el-button type="primary" @click="confirmAndNext" size="large">
                确认信息，进入章节生成
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </div>

          <div class="step-navigation">
            <el-button @click="prevStep">
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 步骤5: 章节生成 -->
      <div v-if="currentStep === 4" class="step-content">
        <el-card class="result-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><DocumentAdd /></el-icon>
              <span>章节生成</span>
              <div class="header-actions" v-if="isStreaming">
                <el-tag type="success" effect="plain">
                  <el-icon class="spinning"><Loading /></el-icon>
                  生成中...
                </el-tag>
              </div>
            </div>
          </template>

          <!-- 小说信息展示 -->
          <div class="novel-info">
            <h2>{{ finalTitle }}</h2>
            <div class="novel-meta">
              <el-tag>{{ novelForm.genre }}</el-tag>
              <el-tag type="info">{{ novelForm.theme }}</el-tag>
            </div>
          </div>

          <!-- 章节选择区域 -->
          <div v-if="!chapterContent && !isStreaming" class="chapter-selection">
            <h3>选择要生成的章节</h3>
            <div class="chapter-options">
              <el-form :model="chapterForm" label-position="top">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="章节序号">
                      <el-select v-model="chapterForm.number" size="large" placeholder="选择章节">
                        <el-option v-for="i in 20" :key="i" :label="`第${i}章`" :value="i" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="章节标题（可选）">
                      <el-input 
                        v-model="chapterForm.customTitle" 
                        size="large"
                        placeholder="自定义章节标题"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
              
              <div class="generate-actions">
                <el-button 
                  type="primary" 
                  @click="generateChapter" 
                  size="large"
                  class="generate-btn"
                  :disabled="!chapterForm.number"
                >
                  <el-icon><DocumentAdd /></el-icon>
                  生成第{{ chapterForm.number }}章
                </el-button>
              </div>
            </div>
          </div>

          <!-- 流式生成内容 -->
          <div v-if="isStreaming" class="streaming-container">
            <div class="streaming-content">
              <h3>{{ currentChapterTitle }}</h3>
              <div class="streaming-text">{{ streamingContent }}</div>
              <div class="cursor-indicator"></div>
            </div>
          </div>

          <!-- 最终结果 -->
          <div v-else-if="chapterContent" class="final-result">
            <div class="chapter-header">
              <h3>{{ currentChapterTitle }}</h3>
            </div>
            <div class="chapter-content">
              {{ chapterContent }}
            </div>
            
            <div class="final-actions">
              <el-button @click="generateAnotherChapter" size="large">
                <el-icon><DocumentAdd /></el-icon>
                生成其他章节
              </el-button>
              <el-button type="success" size="large">
                <el-icon><Check /></el-icon>
                保存章节
              </el-button>
              <el-button @click="startOver">
                <el-icon><RefreshLeft /></el-icon>
                重新开始
              </el-button>
            </div>
          </div>

          <div class="step-navigation" v-if="!isStreaming">
            <el-button @click="prevStep">
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Edit, 
  Star, 
  MagicStick, 
  DocumentAdd, 
  RefreshLeft, 
  Document, 
  Loading,
  ArrowRight,
  ArrowLeft,
  Refresh,
  EditPen,
  Check
} from '@element-plus/icons-vue'

export default defineComponent({
  name: 'Create',
  components: {
    Edit,
    Star,
    MagicStick,
    DocumentAdd,
    RefreshLeft,
    Document,
    Loading,
    ArrowRight,
    ArrowLeft,
    Refresh,
    EditPen,
    Check
  },
  setup() {
    // 基础表单数据
    const novelForm = ref({
      genre: '',
      theme: ''
    })
    
    // 章节表单数据
    const chapterForm = ref({
      number: 1,
      customTitle: ''
    })
    
    // 步骤控制
    const currentStep = ref(0)
    
    // 生成的内容
    const generatedTitle = ref('')
    const generatedOutline = ref('')
    const streamingOutlineContent = ref('')
    const editableTitle = ref('')
    const editableOutline = ref('')
    const finalTitle = ref('')
    const finalOutline = ref('')
    
    // 章节内容
    const chapterContent = ref('')
    const streamingContent = ref('')
    const currentChapterTitle = ref('')
    
    // 状态控制
    const loading = ref(false)
    const isStreaming = ref(false)
    const isStreamingOutline = ref(false)
    const abortController = ref<AbortController | null>(null)
    
    // 配置API基础URL
    const API_BASE_URL = 'http://localhost:8000/api/ai'
    
    // 步骤导航
    const nextStep = () => {
      if (currentStep.value < 4) {
        currentStep.value++
        // 进入确认信息步骤时，初始化编辑内容
        if (currentStep.value === 3) {
          initEditableContent()
        }
      }
    }
    
    const prevStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
      }
    }
    
    // 生成标题
    const generateTitle = async () => {
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
        generatedTitle.value = data.title
        ElMessage.success('标题生成成功')
      } catch (error) {
        console.error('生成标题失败:', error)
        ElMessage.error('标题生成失败')
      } finally {
        loading.value = false
      }
    }
    
    // 重新生成标题
    const regenerateTitle = async () => {
      generatedTitle.value = ''
      await generateTitle()
    }
    
    // 生成大纲
    const generateOutline = async () => {
      loading.value = true
      streamingOutlineContent.value = ''
      isStreamingOutline.value = true
      
      abortController.value = new AbortController()
      
      try {
        const response = await fetch(`${API_BASE_URL}/generate-outline-stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            genre: novelForm.value.genre,
            theme: novelForm.value.theme,
            title: generatedTitle.value
          }),
          signal: abortController.value.signal
        })
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        // 处理SSE格式的流式响应
        if (response.body) {
          const reader = response.body.getReader()
          const decoder = new TextDecoder()
          let fullOutline = ''
          
          while (true) {
            const { done, value } = await reader.read()
            if (done) break
            
            const chunk = decoder.decode(value)
            const lines = chunk.split('\n\n')
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const jsonData = line.substring(6)
                try {
                  const parsed = JSON.parse(jsonData)
                  if (parsed.choices && parsed.choices[0] && parsed.choices[0].delta && parsed.choices[0].delta.content !== undefined) {
                    const content = parsed.choices[0].delta.content
                    if (content !== null && content !== undefined) {
                      fullOutline += content
                      streamingOutlineContent.value = fullOutline
                    }
                  }
                } catch (e) {
                  console.error('解析JSON失败:', e)
                }
              }
            }
          }
        }
        
        generatedOutline.value = streamingOutlineContent.value
        ElMessage.success('大纲生成成功')
      } catch (error: any) {
        if (error.name !== 'AbortError') {
          console.error('生成大纲失败:', error)
          ElMessage.error('大纲生成失败')
        }
      } finally {
        loading.value = false
        isStreamingOutline.value = false
      }
    }
    
    // 重新生成大纲
    const regenerateOutline = async () => {
      generatedOutline.value = ''
      streamingOutlineContent.value = ''
      await generateOutline()
    }
    
    // 确认并进入下一步
    const confirmAndNext = () => {
      editableTitle.value = editableTitle.value || generatedTitle.value
      editableOutline.value = editableOutline.value || generatedOutline.value
      
      finalTitle.value = editableTitle.value
      finalOutline.value = editableOutline.value
      
      nextStep()
    }
    
    // 生成章节
    const generateChapter = async () => {
      loading.value = true
      streamingContent.value = ''
      isStreaming.value = true
      
      // 设置当前章节标题
      const chapterNumber = chapterForm.value.number
      currentChapterTitle.value = chapterForm.value.customTitle || `第${chapterNumber}章`
      
      abortController.value = new AbortController()
      
      try {
        const response = await fetch(`${API_BASE_URL}/generate-chapter-stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: finalTitle.value,
            outline: finalOutline.value,
            chapter_number: chapterNumber,
            custom_title: chapterForm.value.customTitle
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
                const jsonData = line.substring(6);
                try {
                  const parsed = JSON.parse(jsonData);
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
        
        chapterContent.value = streamingContent.value
        ElMessage.success(`第${chapterNumber}章生成成功`)
      } catch (error: any) {
        if (error.name !== 'AbortError') {
          console.error('生成章节失败:', error)
          ElMessage.error('章节生成失败')
        }
      } finally {
        loading.value = false
        isStreaming.value = false
      }
    }
    
    // 生成其他章节
    const generateAnotherChapter = () => {
      chapterContent.value = ''
      streamingContent.value = ''
      chapterForm.value.number = Math.min(chapterForm.value.number + 1, 20)
      chapterForm.value.customTitle = ''
    }
    
    // 重新开始
    const startOver = () => {
      // 重置所有状态
      currentStep.value = 0
      novelForm.value = { genre: '', theme: '' }
      chapterForm.value = { number: 1, customTitle: '' }
      generatedTitle.value = ''
      generatedOutline.value = ''
      streamingOutlineContent.value = ''
      editableTitle.value = ''
      editableOutline.value = ''
      finalTitle.value = ''
      finalOutline.value = ''
      chapterContent.value = ''
      streamingContent.value = ''
      currentChapterTitle.value = ''
      
      if (abortController.value) {
        abortController.value.abort()
      }
    }
    
    // 初始化编辑内容
    const initEditableContent = () => {
      editableTitle.value = generatedTitle.value
      editableOutline.value = generatedOutline.value
    }
    
    // 监听步骤变化，初始化编辑内容
    const handleStepChange = () => {
      if (currentStep.value === 3) {
        initEditableContent()
      }
    }
    
    onUnmounted(() => {
      if (abortController.value) {
        abortController.value.abort()
      }
    })
    
    return {
      // 数据
      novelForm,
      chapterForm,
      currentStep,
      generatedTitle,
      generatedOutline,
      streamingOutlineContent,
      editableTitle,
      editableOutline,
      finalTitle,
      finalOutline,
      chapterContent,
      streamingContent,
      currentChapterTitle,
      
      // 状态
      loading,
      isStreaming,
      isStreamingOutline,
      
      // 方法
      nextStep,
      prevStep,
      generateTitle,
      regenerateTitle,
      generateOutline,
      regenerateOutline,
      confirmAndNext,
      generateChapter,
      generateAnotherChapter,
      startOver
    }
  }
})
</script>

<style scoped lang="scss">
// Create.vue 的样式已迁移到单独的样式文件中
// 所有样式都在 src/styles/create.scss 中进行管理
</style>