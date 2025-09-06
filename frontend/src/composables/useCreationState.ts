// 创作状态管理组合式函数
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { 
  CreationState, 
  NovelForm, 
  ChapterForm, 
  CreationStep, 
  APIResponse,
  GenerateTitleRequest,
  GenerateOutlineRequest,
  GenerateChapterRequest
} from '@/types'

export function useCreationState() {
  // 基础状态
  const state = reactive<CreationState>({
    currentStep: 0 as CreationStep,
    
    // 表单数据
    novelForm: {
      genre: '',
      theme: ''
    } as NovelForm,
    
    chapterForm: {
      number: 1,
      customTitle: ''
    } as ChapterForm,
    
    // 生成的内容
    generatedTitle: '',
    generatedOutline: '',
    editableTitle: '',
    editableOutline: '',
    finalTitle: '',
    finalOutline: '',
    chapterContent: '',
    currentChapterTitle: '',
    
    // 流式状态
    streamingContent: '',
    streamingOutlineContent: '',
    isStreaming: false,
    isStreamingOutline: false,
    loading: false,
    
    // 会话信息
    sessionId: undefined,
    novelId: undefined
  })
  
  // 流控制
  const abortController = ref<AbortController | null>(null)
  
  // API配置
  const API_BASE_URL = 'http://localhost:8000/api/ai'
  
  // 计算属性
  const canProceedToNext = computed(() => {
    switch (state.currentStep) {
      case 0: // 基础设置
        return state.novelForm.genre && state.novelForm.theme
      case 1: // 标题生成
        return state.generatedTitle
      case 2: // 大纲生成
        return state.generatedOutline
      case 3: // 信息确认
        return state.editableTitle && state.editableOutline
      case 4: // 章节生成
        return true
      default:
        return false
    }
  })
  
  const currentStepName = computed(() => {
    const stepNames = ['基础设置', '生成标题', '创建大纲', '确认信息', '生成章节']
    return stepNames[state.currentStep] || '未知步骤'
  })
  
  // 步骤控制
  const nextStep = () => {
    if (state.currentStep < 4) {
      state.currentStep++
      
      // 进入确认信息步骤时，初始化编辑内容
      if (state.currentStep === 3) {
        initEditableContent()
      }
    }
  }
  
  const prevStep = () => {
    if (state.currentStep > 0) {
      state.currentStep--
    }
  }
  
  // 初始化编辑内容
  const initEditableContent = () => {
    state.editableTitle = state.generatedTitle
    // 格式化大纲内容
    state.editableOutline = formatOutlineContent(state.generatedOutline)
  }
  
  // 格式化大纲内容
  const formatOutlineContent = (text: string) => {
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
  
  // 错误处理
  const handleError = (error: any, defaultMessage: string) => {
    console.error(error)
    const message = error?.message || defaultMessage
    ElMessage.error(message)
    return message
  }
  
  // 中止请求
  const abortCurrentRequest = () => {
    if (abortController.value) {
      abortController.value.abort()
      abortController.value = null
    }
  }
  
  // API调用函数
  const callAPI = async <T>(url: string, data: any): Promise<APIResponse<T>> => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  }
  
  // 流式API调用
  const callStreamAPI = async (url: string, data: any, onChunk: (chunk: string) => void) => {
    abortController.value = new AbortController()
    
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data),
      signal: abortController.value.signal
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    // 处理SSE格式的流式响应
    if (response.body) {
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      
      let buffer = '' // 用于处理跨chunk的数据
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        const chunk = decoder.decode(value, { stream: true })
        buffer += chunk
        
        // 按行分割
        const lines = buffer.split('\n')
        // 保留最后一行（可能不完整）
        buffer = lines.pop() || ''
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const jsonData = line.substring(6).trim()
            if (jsonData === '[DONE]') {
              return
            }
            try {
              const parsed = JSON.parse(jsonData)
              if (parsed.choices?.[0]?.delta?.content !== undefined) {
                const content = parsed.choices[0].delta.content
                if (content !== null && content !== undefined && content !== '') {
                  onChunk(content)
                }
              }
            } catch (e) {
              console.error('解析JSON失败:', e, 'JSON数据:', jsonData)
            }
          }
        }
      }
      
      // 处理buffer中剩余的数据
      if (buffer.startsWith('data: ')) {
        const jsonData = buffer.substring(6).trim()
        if (jsonData !== '[DONE]') {
          try {
            const parsed = JSON.parse(jsonData)
            if (parsed.choices?.[0]?.delta?.content !== undefined) {
              const content = parsed.choices[0].delta.content
              if (content !== null && content !== undefined && content !== '') {
                onChunk(content)
              }
            }
          } catch (e) {
            console.error('解析最后JSON失败:', e)
          }
        }
      }
    }
  }
  
  // 生成标题
  const generateTitle = async () => {
    if (!state.novelForm.genre || !state.novelForm.theme) {
      ElMessage.warning('请先填写小说类型和主题')
      return
    }
    
    state.loading = true
    try {
      const request: GenerateTitleRequest = {
        genre: state.novelForm.genre as string,
        theme: state.novelForm.theme
      }
      
      const response = await fetch(`${API_BASE_URL}/generate-title`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.title) {
        state.generatedTitle = data.title
        ElMessage.success('标题生成成功')
      } else {
        throw new Error('标题生成失败：响应数据格式错误')
      }
    } catch (error: any) {
      if (error.name !== 'AbortError') {
        handleError(error, '标题生成失败')
      }
    } finally {
      state.loading = false
    }
  }
  
  // 重新生成标题
  const regenerateTitle = async () => {
    state.generatedTitle = ''
    await generateTitle()
  }
  
  // 生成大纲（流式）
  const generateOutline = async () => {
    if (!state.generatedTitle) {
      ElMessage.warning('请先生成标题')
      return
    }
    
    // 重置状态
    state.loading = true
    state.streamingOutlineContent = ''
    state.isStreamingOutline = true
    state.generatedOutline = '' // 清除之前的大纲内容
    
    try {
      const request: GenerateOutlineRequest = {
        genre: state.novelForm.genre as string,
        theme: state.novelForm.theme,
        title: state.generatedTitle
      }
      
      await callStreamAPI('/generate-outline-stream', request, (chunk) => {
        state.streamingOutlineContent += chunk
      })
      
      state.generatedOutline = state.streamingOutlineContent
      ElMessage.success('大纲生成成功')
    } catch (error: any) {
      if (error.name !== 'AbortError') {
        handleError(error, '大纲生成失败')
      }
    } finally {
      state.loading = false
      state.isStreamingOutline = false
    }
  }
  
  // 重新生成大纲
  const regenerateOutline = async () => {
    state.generatedOutline = ''
    state.streamingOutlineContent = ''
    await generateOutline()
  }
  
  // 确认并进入下一步
  const confirmAndNext = () => {
    state.editableTitle = state.editableTitle || state.generatedTitle
    state.editableOutline = state.editableOutline || state.generatedOutline
    
    state.finalTitle = state.editableTitle
    state.finalOutline = state.editableOutline
    
    nextStep()
  }
  
  // 生成章节（流式）
  const generateChapter = async () => {
    if (!state.finalTitle || !state.finalOutline) {
      ElMessage.warning('请先确认标题和大纲')
      return
    }
    
    state.loading = true
    state.streamingContent = ''
    state.isStreaming = true
    
    // 设置当前章节标题
    const chapterNumber = state.chapterForm.number
    state.currentChapterTitle = state.chapterForm.customTitle || `第${chapterNumber}章`
    
    try {
      const request: GenerateChapterRequest = {
        title: state.finalTitle,
        outline: state.finalOutline,
        chapter_number: chapterNumber,
        custom_title: state.chapterForm.customTitle
      }
      
      await callStreamAPI('/generate-chapter-stream', request, (chunk) => {
        state.streamingContent += chunk
      })
      
      state.chapterContent = state.streamingContent
      ElMessage.success(`第${chapterNumber}章生成成功`)
    } catch (error: any) {
      if (error.name !== 'AbortError') {
        handleError(error, '章节生成失败')
      }
    } finally {
      state.loading = false
      state.isStreaming = false
    }
  }
  
  // 生成其他章节
  const generateAnotherChapter = () => {
    state.chapterContent = ''
    state.streamingContent = ''
    state.chapterForm.number = Math.min(state.chapterForm.number + 1, 20)
    state.chapterForm.customTitle = ''
  }
  
  // 重新开始
  const startOver = () => {
    // 中止当前请求
    abortCurrentRequest()
    
    // 重置所有状态
    Object.assign(state, {
      currentStep: 0,
      novelForm: { genre: '', theme: '' },
      chapterForm: { number: 1, customTitle: '' },
      generatedTitle: '',
      generatedOutline: '',
      streamingOutlineContent: '',
      editableTitle: '',
      editableOutline: '',
      finalTitle: '',
      finalOutline: '',
      chapterContent: '',
      streamingContent: '',
      currentChapterTitle: '',
      isStreaming: false,
      isStreamingOutline: false,
      loading: false,
      sessionId: undefined,
      novelId: undefined
    })
  }
  
  // 保存进度（可选实现）
  const saveProgress = () => {
    const progressData = {
      currentStep: state.currentStep,
      novelForm: state.novelForm,
      generatedTitle: state.generatedTitle,
      generatedOutline: state.generatedOutline,
      editableTitle: state.editableTitle,
      editableOutline: state.editableOutline,
      finalTitle: state.finalTitle,
      finalOutline: state.finalOutline
    }
    
    localStorage.setItem('novel-creation-progress', JSON.stringify(progressData))
    ElMessage.success('进度已保存')
  }
  
  // 加载进度（可选实现）
  const loadProgress = () => {
    try {
      const saved = localStorage.getItem('novel-creation-progress')
      if (saved) {
        const progressData = JSON.parse(saved)
        Object.assign(state, progressData)
        ElMessage.success('进度已恢复')
        return true
      }
    } catch (error) {
      console.error('加载进度失败:', error)
    }
    return false
  }
  
  // 清除保存的进度
  const clearProgress = () => {
    localStorage.removeItem('novel-creation-progress')
  }
  
  // 生命周期清理
  const cleanup = () => {
    abortCurrentRequest()
  }
  
  // === 新增：章节保存和管理功能 ===
  
  // 检查是否已有该章节存在
  const checkExistingChapter = async (chapterNumber: number, novelTitle: string) => {
    try {
      const chapters = await getSavedChapters()
      return chapters.find((ch: any) => 
        ch.chapter_number === chapterNumber && 
        ch.novel_title === novelTitle
      )
    } catch (error) {
      console.error('检查章节时出错:', error)
      return null
    }
  }
  
  // 保存章节到后端
  const saveChapterToServer = async () => {
    if (!state.chapterContent || !state.finalTitle || !state.finalOutline) {
      ElMessage.warning('没有可保存的章节内容')
      return false
    }
    
    // 检查是否已存在该章节
    const existingChapter = await checkExistingChapter(state.chapterForm.number, state.finalTitle)
    
    let confirmSave = true
    if (existingChapter) {
      confirmSave = await new Promise((resolve) => {
        ElMessageBox.confirm(
          `第${state.chapterForm.number}章已存在，是否覆盖保存？`,
          '章节已存在',
          {
            confirmButtonText: '覆盖保存',
            cancelButtonText: '取消',
            type: 'warning',
          }
        ).then(() => resolve(true))
          .catch(() => resolve(false))
      })
    }
    
    if (!confirmSave) return false
    
    try {
      const response = await fetch(`${API_BASE_URL}/save-chapter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: state.finalTitle,
          content: state.chapterContent,
          chapter_number: state.chapterForm.number,
          custom_title: state.chapterForm.customTitle,
          genre: state.novelForm.genre,
          theme: state.novelForm.theme,
          outline: state.finalOutline
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.success) {
        ElMessage.success(`第${state.chapterForm.number}章已成功保存到服务器`)
        return true
      } else {
        throw new Error(data.message || '保存失败')
      }
    } catch (error: any) {
      handleError(error, '保存章节失败')
      return false
    }
  }
  
  // 获取已保存的章节列表
  const getSavedChapters = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/saved-chapters`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.success) {
        return data.chapters || []
      } else {
        throw new Error(data.message || '获取章节列表失败')
      }
    } catch (error: any) {
      handleError(error, '获取章节列表失败')
      return []
    }
  }
  
  // 获取特定章节内容
  const getChapterContent = async (chapterId: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chapter/${chapterId}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.success) {
        return data.chapter
      } else {
        throw new Error(data.message || '获取章节内容失败')
      }
    } catch (error: any) {
      handleError(error, '获取章节内容失败')
      return null
    }
  }
  
  // 打开保存的章节
  const openSavedChapter = async (chapterId: string) => {
    try {
      const chapterData = await getChapterContent(chapterId)
      if (!chapterData) {
        ElMessage.error('章节数据不存在')
        return false
      }
      
      // 恢复状态到第5步（章节生成完成）
      state.currentStep = 4
      state.novelForm.genre = chapterData.genre
      state.novelForm.theme = chapterData.theme
      state.generatedTitle = chapterData.novel_title
      state.generatedOutline = chapterData.outline
      state.editableTitle = chapterData.novel_title
      state.editableOutline = chapterData.outline
      state.finalTitle = chapterData.novel_title
      state.finalOutline = chapterData.outline
      state.chapterForm.number = chapterData.chapter_number
      state.chapterForm.customTitle = chapterData.title !== `第${chapterData.chapter_number}章` ? chapterData.title : ''
      state.currentChapterTitle = chapterData.title
      state.chapterContent = chapterData.content
      state.streamingContent = ''
      state.isStreaming = false
      
      ElMessage.success(`已加载章节：${chapterData.title}`)
      return true
    } catch (error: any) {
      handleError(error, '打开章节失败')
      return false
    }
  }
  
  // 修改章节位置
  const updateChapterPosition = async (chapterId: string, newPosition: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/chapter/${chapterId}/position`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          new_position: newPosition
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.success) {
        ElMessage.success(`章节位置已更新为第${newPosition}章`)
        return true
      } else {
        throw new Error(data.message || '位置更新失败')
      }
    } catch (error: any) {
      handleError(error, '修改章节位置失败')
      return false
    }
  }
  
  return {
    // 状态
    state,
    
    // 计算属性
    canProceedToNext,
    currentStepName,
    
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
    startOver,
    saveProgress,
    loadProgress,
    clearProgress,
    cleanup,
    abortCurrentRequest,
    
    // 新增：章节管理功能
    saveChapterToServer,
    getSavedChapters,
    getChapterContent,
    openSavedChapter,
    checkExistingChapter,
    updateChapterPosition
  }
}