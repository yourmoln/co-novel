// 全局类型定义

// 小说类型枚举
export enum NovelGenre {
  FANTASY = '玄幻',
  URBAN = '都市', 
  SCIFI = '科幻',
  WUXIA = '武侠',
  ROMANCE = '言情'
}

// 小说状态枚举
export enum NovelStatus {
  DRAFT = '草稿',
  IN_PROGRESS = '创作中',
  COMPLETED = '已完成',
  PUBLISHED = '已发布'
}

// 章节状态枚举
export enum ChapterStatus {
  DRAFT = '草稿',
  GENERATING = '生成中',
  COMPLETED = '已完成',
  REVIEWED = '已审阅'
}

// 创作步骤枚举
export enum CreationStep {
  BASIC_SETUP = 0,
  TITLE_GENERATION = 1,
  OUTLINE_CREATION = 2,
  CONTENT_REVIEW = 3,
  CHAPTER_GENERATION = 4
}

// 基础接口
export interface BaseEntity {
  id: string
  created_at: string
  updated_at: string
}

// 小说项目接口
export interface NovelProject extends BaseEntity {
  title?: string
  genre: NovelGenre
  theme: string
  outline?: string
  status: NovelStatus
  generated_titles: string[]
  user_edits: Record<string, any>
  total_word_count: number
  chapter_count: number
}

// 章节接口
export interface Chapter extends BaseEntity {
  novel_id: string
  chapter_number: number
  title?: string
  content?: string
  status: ChapterStatus
  word_count: number
  generated_by_ai: boolean
  ai_model_used?: string
  generation_prompt?: string
}

// 创作会话接口
export interface CreationSession extends BaseEntity {
  novel_id: string
  current_step: CreationStep
  session_data: Record<string, any>
  is_active: boolean
  last_activity: string
}

// API响应接口
export interface APIResponse<T = any> {
  success: boolean
  message: string
  data?: T
  error_code?: string
  timestamp: string
}

// 表单接口
export interface NovelForm {
  genre: NovelGenre | ''
  theme: string
}

// 章节表单接口
export interface ChapterForm {
  number: number
  customTitle: string
}

// 创作状态接口
export interface CreationState {
  currentStep: CreationStep
  novelForm: NovelForm
  chapterForm: ChapterForm
  generatedTitle: string
  generatedOutline: string
  editableTitle: string
  editableOutline: string
  finalTitle: string
  finalOutline: string
  chapterContent: string
  currentChapterTitle: string
  
  // 流式状态
  streamingContent: string
  streamingOutlineContent: string
  isStreaming: boolean
  isStreamingOutline: boolean
  loading: boolean
  
  // 会话信息
  sessionId?: string
  novelId?: string
}

// API请求接口
export interface GenerateTitleRequest {
  genre: string
  theme: string
  count?: number
}

export interface GenerateOutlineRequest {
  genre: string
  theme: string
  title: string
}

export interface GenerateChapterRequest {
  title: string
  outline: string
  chapter_number: number
  custom_title?: string
}

// 流式响应处理
export interface StreamChunk {
  id: string
  object: string
  created: number
  model: string
  choices: Array<{
    index: number
    delta: {
      content?: string
      role?: string
    }
    finish_reason?: string
  }>
}

// 错误处理
export interface ErrorInfo {
  code: string
  message: string
  details?: any
}

// 统计信息
export interface Statistics {
  total_novels: number
  total_chapters: number
  total_words: number
  active_sessions: number
  cache_entries: number
  cache_efficiency: number
  genre_distribution: Record<string, number>
  last_updated: string
}

// 工具函数类型
export type StepAction = 'next' | 'prev' | 'update' | 'save'
export type ContentType = 'title' | 'outline' | 'chapter' | 'content'

declare global {
  interface Window {
    // 在这里可以添加全局变量的类型定义
    APP_CONFIG?: {
      API_BASE_URL: string
      VERSION: string
    }
  }
}

export {}
