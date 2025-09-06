<template>
  <div class="create-page">
    <div class="page-header">
      <h1>小说创作工作台</h1>
      <p>让AI成为您的创作伙伴，开始一段精彩的文学之旅</p>
      
      <!-- 已保存章节按钮 -->
      <div class="saved-chapters-button" v-if="state.currentStep === 0">
        <el-button 
          type="info" 
          @click="showSavedChaptersDialog = true"
          size="large"
          plain
        >
          <el-icon><FolderOpened /></el-icon>
          查看已保存章节
        </el-button>
      </div>
    </div>

      <!-- 步骤指示器 -->
    <div class="steps-container">
      <el-steps :active="state.currentStep" finish-status="success" align-center>
        <el-step title="基础设置" description="设置类型和主题"></el-step>
        <el-step title="生成标题" description="AI生成小说标题"></el-step>
        <el-step title="创建大纲" description="AI生成章节大纲"></el-step>
        <el-step title="确认信息" description="编辑和确认内容"></el-step>
        <el-step title="生成章节" description="开始创作之旅"></el-step>
      </el-steps>
    </div>
    
    <div class="create-container">
      <!-- 步骤1: 基础设置 -->
      <div v-if="state.currentStep === 0" class="step-content">
        <el-card class="form-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><Edit /></el-icon>
              <span>基础设置</span>
            </div>
          </template>
          
          <el-form :model="state.novelForm" label-position="top" class="create-form">
            <el-form-item label="小说类型" class="form-item">
              <el-select 
                v-model="state.novelForm.genre" 
                placeholder="选择您喜欢的类型" 
                class="genre-select"
                size="large"
              >
                <el-option 
                  v-for="option in genreOptions" 
                  :key="option.value"
                  :label="option.label" 
                  :value="option.value"
                ></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="创作主题" class="form-item">
              <el-input 
                v-model="state.novelForm.theme" 
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
                @click="handleNextStep" 
                size="large"
                :disabled="!canProceedToNext"
              >
                下一步：生成标题
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </el-form>
        </el-card>
      </div>

      <!-- 步骤2: 生成标题 -->
      <div v-if="state.currentStep === 1" class="step-content">
        <el-card class="form-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><MagicStick /></el-icon>
              <span>生成标题</span>
            </div>
          </template>

          <div class="step-info">
            <p><strong>类型:</strong> {{ state.novelForm.genre }}</p>
            <p><strong>主题:</strong> {{ state.novelForm.theme }}</p>
          </div>

          <div v-if="!state.generatedTitle" class="generate-section">
            <el-button 
              type="primary" 
              @click="generateTitle" 
              :loading="state.loading"
              size="large"
              class="generate-btn"
            >
              <el-icon v-if="!state.loading"><MagicStick /></el-icon>
              生成标题
            </el-button>
          </div>

          <div v-else class="result-section">
            <h3>生成的标题：</h3>
            <div class="title-display">{{ state.generatedTitle }}</div>
            
            <div class="step-actions">
              <el-button @click="regenerateTitle" :loading="state.loading">
                <el-icon><Refresh /></el-icon>
                重新生成
              </el-button>
              <el-button type="primary" @click="handleNextStep" size="large">
                确认标题，下一步
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </div>

          <div class="step-navigation">
            <el-button @click="handlePrevStep">
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 步骤3: 创建大纲 -->
      <div v-if="state.currentStep === 2" class="step-content">
        <el-card class="form-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><Document /></el-icon>
              <span>创建大纲</span>
            </div>
          </template>

          <div class="step-info">
            <p><strong>标题:</strong> {{ state.generatedTitle }}</p>
            <p><strong>类型:</strong> {{ state.novelForm.genre }} | <strong>主题:</strong> {{ state.novelForm.theme }}</p>
          </div>

          <div v-if="!state.generatedOutline" class="generate-section">
            <el-button 
              type="primary" 
              @click="generateOutline" 
              :loading="state.loading"
              size="large"
              class="generate-btn"
            >
              <el-icon v-if="!state.loading"><Document /></el-icon>
              流式生成大纲
            </el-button>
          </div>

          <!-- 流式生成大纲 -->
          <div v-if="state.isStreamingOutline" class="streaming-container">
            <h3>正在生成大纲：</h3>
            <div class="streaming-outline">
              {{ formatOutlineText(state.streamingOutlineContent) }}
              <div class="cursor-indicator"></div>
            </div>
          </div>

          <div v-else-if="state.generatedOutline" class="result-section">
            <h3>生成的大纲：</h3>
            <div class="outline-display">{{ formatOutlineText(state.generatedOutline) }}</div>
            
            <div class="step-actions">
              <el-button @click="regenerateOutline" :loading="state.loading">
                <el-icon><Refresh /></el-icon>
                重新生成
              </el-button>
              <el-button type="primary" @click="handleNextStep" size="large">
                确认大纲，下一步
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </div>

          <div class="step-navigation">
            <el-button @click="handlePrevStep">
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 步骤4: 确认信息 -->
      <div v-if="state.currentStep === 3" class="step-content">
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
                <span>{{ state.novelForm.genre }}</span>
              </div>
              <div class="info-item">
                <label>创作主题：</label>
                <span>{{ state.novelForm.theme }}</span>
              </div>
            </div>
          </div>

          <div class="confirm-section">
            <el-form label-position="top">
              <el-form-item label="小说标题">
                <el-input 
                  v-model="state.editableTitle" 
                  size="large"
                  placeholder="您可以编辑标题"
                />
                <div class="hint-text">原标题：{{ state.generatedTitle }}</div>
              </el-form-item>
              
              <el-form-item label="小说大纲">
                <el-input 
                  v-model="state.editableOutline" 
                  type="textarea"
                  :rows="8"
                  placeholder="您可以编辑大纲"
                  resize="vertical"
                  class="outline-textarea"
                />
                <div class="hint-text">可以在此处修改AI生成的大纲内容</div>
              </el-form-item>
            </el-form>
            
            <div class="step-actions">
              <el-button type="primary" @click="handleConfirmAndNext" size="large">
                确认信息，进入章节生成
                <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </div>

          <div class="step-navigation">
            <el-button @click="handlePrevStep">
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 步骤5: 章节生成 -->
      <div v-if="state.currentStep === 4" class="step-content">
        <el-card class="result-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon class="header-icon"><DocumentAdd /></el-icon>
              <span>章节生成</span>
              <div class="header-actions" v-if="state.isStreaming">
                <el-tag type="success" effect="plain">
                  <el-icon class="spinning"><Loading /></el-icon>
                  生成中...
                </el-tag>
              </div>
            </div>
          </template>

          <!-- 小说信息展示 -->
          <div class="novel-info">
            <h2>{{ state.finalTitle }}</h2>
            <div class="novel-meta">
              <el-tag>{{ state.novelForm.genre }}</el-tag>
              <el-tag type="info">{{ state.novelForm.theme }}</el-tag>
            </div>
          </div>

          <!-- 章节选择区域 -->
          <div v-if="!state.chapterContent && !state.isStreaming" class="chapter-selection">
            <h3>选择要生成的章节</h3>
            <div class="chapter-options">
              <el-form :model="state.chapterForm" label-position="top">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="章节序号">
                      <el-select v-model="state.chapterForm.number" size="large" placeholder="选择章节" @change="handleChapterNumberChange">
                        <el-option v-for="i in 20" :key="i" :label="`第${i}章`" :value="i" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="章节标题（可选）">
                      <el-input 
                        v-model="state.chapterForm.customTitle" 
                        size="large"
                        placeholder="自定义章节标题"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
              
              <!-- 章节状态提示 -->
              <div v-if="currentChapterStatus" class="chapter-status-info">
                <el-alert 
                  :title="currentChapterStatus.message" 
                  :type="currentChapterStatus.type"
                  :closable="false"
                  show-icon
                />
              </div>
              
              <div class="generate-actions">
                <!-- 已存在章节的按钮 -->
                <template v-if="currentChapterStatus?.exists">
                  <el-button 
                    type="primary"
                    @click="viewExistingChapter" 
                    size="large"
                    class="action-btn"
                  >
                    <el-icon><View /></el-icon>
                    查看已生成结果
                  </el-button>
                  <el-button 
                    type="warning"
                    @click="regenerateExistingChapter" 
                    size="large"
                    class="action-btn"
                    :loading="state.loading"
                  >
                    <el-icon><Refresh /></el-icon>
                    重新生成第{{ state.chapterForm.number }}章
                  </el-button>
                </template>
                
                <!-- 未存在章节的按钮 -->
                <template v-else>
                  <el-button 
                    type="primary" 
                    @click="generateChapter" 
                    size="large"
                    class="generate-btn"
                    :disabled="!state.chapterForm.number"
                    :loading="state.loading"
                  >
                    <el-icon><DocumentAdd /></el-icon>
                    生成第{{ state.chapterForm.number }}章
                  </el-button>
                </template>
              </div>
            </div>
          </div>

          <!-- 流式生成内容 -->
          <div v-if="state.isStreaming" class="streaming-container">
            <div class="streaming-content">
              <h3>{{ state.currentChapterTitle }}</h3>
              {{ state.streamingContent }}
              <div class="cursor-indicator"></div>
            </div>
          </div>

          <!-- 最终结果 -->
          <div v-else-if="state.chapterContent" class="final-result">
            <div class="chapter-header">
              <h3>{{ state.currentChapterTitle }}</h3>
            </div>
            <div class="chapter-content">
              {{ state.chapterContent }}
            </div>
            
            <div class="final-actions">
              <el-button @click="generateAnotherChapter" size="large">
                <el-icon><DocumentAdd /></el-icon>
                生成其他章节
              </el-button>
              <el-button @click="handleSaveChapter" type="success" size="large" :loading="savingChapter">
                <el-icon><Check /></el-icon>
                {{ savingChapter ? '保存中...' : '保存章节' }}
              </el-button>
              <el-button @click="showSavedChaptersDialog = true" type="info" size="large">
                <el-icon><FolderOpened /></el-icon>
                查看已保存章节
              </el-button>
              <el-button @click="startOver">
                <el-icon><RefreshLeft /></el-icon>
                重新开始
              </el-button>
            </div>
          </div>

          <div class="step-navigation" v-if="!state.isStreaming">
            <el-button @click="handlePrevStep">
              <el-icon><ArrowLeft /></el-icon>
              上一步
            </el-button>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 已保存章节对话框 -->
    <el-dialog 
      v-model="showSavedChaptersDialog" 
      title="已保存的章节"
      width="80%"
      :before-close="closeSavedChaptersDialog"
    >
      <div v-loading="loadingChapters" class="saved-chapters-container">
        <div v-if="savedChapters.length === 0" class="empty-state">
          <el-empty description="暂无已保存的章节">
            <el-button type="primary" @click="closeSavedChaptersDialog">开始创作</el-button>
          </el-empty>
        </div>
        
        <div v-else class="chapters-grid">
          <el-card 
            v-for="chapter in savedChapters" 
            :key="chapter.chapter_id"
            class="chapter-card"
            shadow="hover"
          >
            <div class="chapter-info">
              <h4>{{ chapter.title }}</h4>
              <div class="chapter-meta">
                <p class="novel-title">小说：{{ chapter.novel_title }}</p>
                <p class="chapter-details">
                  <el-tag size="small">第{{ chapter.chapter_number }}章</el-tag>
                  <el-tag size="small" type="info">{{ chapter.genre }}</el-tag>
                  <span class="word-count">{{ chapter.word_count }}字</span>
                  <span class="create-time">{{ formatDate(chapter.created_at) }}</span>
                </p>
                <p class="theme">主题：{{ chapter.theme }}</p>
              </div>
            </div>
            
            <div class="chapter-actions">
              <div class="position-editor">
                <el-input-number 
                  v-model="chapter.editPosition" 
                  :min="1" 
                  :max="99" 
                  size="small"
                  controls-position="right"
                  @change="handlePositionChange(chapter)"
                  style="width: 80px; margin-right: 8px;"
                />
                <el-button 
                  size="small" 
                  @click="confirmPositionChange(chapter)"
                  :disabled="chapter.editPosition === chapter.chapter_number"
                >
                  修改
                </el-button>
              </div>
              <el-button 
                type="primary" 
                @click="handleOpenChapter(chapter.chapter_id)"
                :loading="openingChapter === chapter.chapter_id"
                size="small"
              >
                <el-icon><View /></el-icon>
                打开章节
              </el-button>
            </div>
          </el-card>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="loadSavedChapters" :loading="loadingChapters">
            <el-icon><Refresh /></el-icon>
            刷新列表
          </el-button>
          <el-button @click="closeSavedChaptersDialog">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted, ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
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
  Check,
  FolderOpened,
  View
} from '@element-plus/icons-vue'
import { useCreationState } from '@/composables/useCreationState'
import type { NovelGenre } from '@/types'

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
    Check,
    FolderOpened,
    View
  },
  setup() {
    // 使用状态管理组合函数
    const {
      state,
      canProceedToNext,
      currentStepName,
      nextStep,
      prevStep,
      generateTitle,
      regenerateTitle,
      generateOutline,
      regenerateOutline,
      confirmAndNext,
      generateChapter,
      generateAnotherChapter,
      startOver,
      saveProgress,
      loadProgress,
      cleanup,
      saveChapterToServer,
      getSavedChapters,
      openSavedChapter,
      checkExistingChapter,
      updateChapterPosition
    } = useCreationState()
    
    // 已保存章节相关状态
    const showSavedChaptersDialog = ref(false)
    const savedChapters = ref<any[]>([])
    const loadingChapters = ref(false)
    const savingChapter = ref(false)
    const openingChapter = ref('')
    const currentChapterStatus = ref<any>(null)
    const updatingPosition = ref('')
    
    // 组件生命周期
    onMounted(async () => {
      // 尝试加载之前保存的进度
      loadProgress()
      
      // 如果已经在第5步，检查当前章节状态
      if (state.currentStep === 4) {
        await checkCurrentChapterStatus()
      }
    })
    
    onUnmounted(() => {
      // 清理资源
      cleanup()
    })
    
    // 小说类型选项
    const genreOptions = [
      { label: '🎆 玄幻', value: '玄幻' },
      { label: '🏢 都市', value: '都市' },
      { label: '🚀 科幻', value: '科幻' },
      { label: '⚔️ 武侠', value: '武侠' },
      { label: '💕 言情', value: '言情' }
    ]
    
    // 处理步骤切换
    const handleNextStep = () => {
      if (canProceedToNext.value) {
        nextStep()
        // 自动保存进度
        saveProgress()
      } else {
        ElMessage.warning('请完成当前步骤的必填项')
      }
    }
    
    // 处理上一步
    const handlePrevStep = () => {
      prevStep()
      saveProgress()
    }
    
    // 处理确认并下一步
    const handleConfirmAndNext = () => {
      confirmAndNext()
      saveProgress()
    }
    
    // 格式化大纲文本
    const formatOutlineText = (text: string) => {
      if (!text) return ''
      
      // 先清理和规范化文本
      let formatted = text
        .replace(/\r\n/g, '\n') // 统一换行符
        .replace(/\r/g, '\n')   // 统一换行符
        .trim()
      
      // 确保每章之间有适当的换行
      formatted = formatted
        .replace(/第([一二三四五六七八九十\d]+)章/g, '\n\n第$1章')
        .replace(/^[\n\s]+/, '') // 移除开头的换行和空格
        .replace(/\n{3,}/g, '\n\n') // 将多个换行统一为两个
        .replace(/[ \t]+/g, ' ') // 规范化空格
      
      return formatted
    }
    
    // 保存章节到服务器
    const handleSaveChapter = async () => {
      savingChapter.value = true
      try {
        const success = await saveChapterToServer()
        if (success) {
          // 保存成功后刷新已保存章节列表
          await loadSavedChapters()
        }
      } finally {
        savingChapter.value = false
      }
    }
    
    // 加载已保存的章节列表
    const loadSavedChapters = async () => {
      loadingChapters.value = true
      try {
        const chapters = await getSavedChapters()
        // 为每个章节添加编辑位置属性
        savedChapters.value = chapters.map((ch: any) => ({
          ...ch,
          editPosition: ch.chapter_number
        }))
      } finally {
        loadingChapters.value = false
      }
    }
    
    // 检查当前选中章节的状态
    const checkCurrentChapterStatus = async () => {
      if (!state.chapterForm.number || !state.finalTitle) {
        currentChapterStatus.value = null
        return
      }
      
      try {
        const existingChapter = await checkExistingChapter(state.chapterForm.number, state.finalTitle)
        
        if (existingChapter) {
          currentChapterStatus.value = {
            exists: true,
            type: 'success',
            message: `第${state.chapterForm.number}章已存在，可以查看或重新生成`,
            chapter: existingChapter
          }
        } else {
          currentChapterStatus.value = {
            exists: false,
            type: 'info',
            message: `第${state.chapterForm.number}章尚未生成`,
            chapter: null
          }
        }
      } catch (error) {
        console.error('检查章节状态时出错:', error)
        currentChapterStatus.value = null
      }
    }
    
    // 处理章节序号变化
    const handleChapterNumberChange = () => {
      checkCurrentChapterStatus()
    }
    
    // 查看已存在的章节
    const viewExistingChapter = async () => {
      if (currentChapterStatus.value?.chapter) {
        const success = await openSavedChapter(currentChapterStatus.value.chapter.chapter_id)
        if (success) {
          // 成功加载后自动刷新状态
          await checkCurrentChapterStatus()
        }
      }
    }
    
    // 重新生成已存在的章节
    const regenerateExistingChapter = async () => {
      try {
        const confirm = await ElMessageBox.confirm(
          `确定要重新生成第${state.chapterForm.number}章吗？这将覆盖现有内容。`,
          '重新生成章节',
          {
            confirmButtonText: '确定重新生成',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        
        if (confirm) {
          // 清空当前章节内容
          state.chapterContent = ''
          state.streamingContent = ''
          // 开始生成
          await generateChapter()
        }
      } catch {
        // 用户取消
      }
    }
    
    // 打开已保存的章节
    const handleOpenChapter = async (chapterId: string) => {
      openingChapter.value = chapterId
      try {
        const success = await openSavedChapter(chapterId)
        if (success) {
          showSavedChaptersDialog.value = false
        }
      } finally {
        openingChapter.value = ''
      }
    }
    
    // 关闭对话框
    const closeSavedChaptersDialog = () => {
      showSavedChaptersDialog.value = false
    }
    
    // 处理章节位置变化
    const handlePositionChange = (chapter: any) => {
      // 即时更新编辑值，但不立即提交
      console.log(`章节 ${chapter.title} 的位置将从第${chapter.chapter_number}章改为第${chapter.editPosition}章`)
    }
    
    // 确认位置修改
    const confirmPositionChange = async (chapter: any) => {
      if (chapter.editPosition === chapter.chapter_number) {
        ElMessage.info('位置没有变化')
        return
      }
      
      try {
        const confirm = await ElMessageBox.confirm(
          `确定要将《${chapter.title}》从第${chapter.chapter_number}章改为第${chapter.editPosition}章吗？`,
          '修改章节位置',
          {
            confirmButtonText: '确定修改',
            cancelButtonText: '取消',
            type: 'warning',
          }
        )
        
        if (confirm) {
          updatingPosition.value = chapter.chapter_id
          const success = await updateChapterPosition(chapter.chapter_id, chapter.editPosition)
          
          if (success) {
            // 更新本地数据
            chapter.chapter_number = chapter.editPosition
            // 重新加载列表以确保数据一致性
            await loadSavedChapters()
          } else {
            // 失败时恢复原值
            chapter.editPosition = chapter.chapter_number
          }
        } else {
          // 用户取消时恢复原值
          chapter.editPosition = chapter.chapter_number
        }
      } catch (error) {
        // 取消或错误时恢复原值
        chapter.editPosition = chapter.chapter_number
      } finally {
        updatingPosition.value = ''
      }
    }
    
    // 格式化日期
    const formatDate = (dateString: string) => {
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('zh-CN', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch {
        return dateString
      }
    }
    return {
      // 状态
      state,
      
      // 计算属性
      canProceedToNext,
      currentStepName,
      
      // 选项
      genreOptions,
      
      // 方法
      handleNextStep,
      handlePrevStep,
      generateTitle,
      regenerateTitle,
      generateOutline,
      regenerateOutline,
      handleConfirmAndNext,
      generateChapter,
      generateAnotherChapter,
      startOver,
      formatOutlineText,
      
      // 新增的章节管理功能
      showSavedChaptersDialog,
      savedChapters,
      loadingChapters,
      savingChapter,
      openingChapter,
      currentChapterStatus,
      updatingPosition,
      handleSaveChapter,
      loadSavedChapters,
      handleOpenChapter,
      closeSavedChaptersDialog,
      formatDate,
      handleChapterNumberChange,
      checkCurrentChapterStatus,
      viewExistingChapter,
      regenerateExistingChapter,
      handlePositionChange,
      confirmPositionChange
    }
  }
})
</script>

<style scoped lang="scss">
// Create.vue 的样式已迁移到单独的样式文件中
// 所有样式都在 src/styles/create.scss 中进行管理
</style>