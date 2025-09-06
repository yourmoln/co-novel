import { ref, watch, onMounted } from 'vue'

export type Theme = 'light' | 'dark'

const theme = ref<Theme>('light')
const isDarkMode = ref(false)

export function useTheme() {
  // 获取系统主题偏好
  const getSystemTheme = (): Theme => {
    if (typeof window !== 'undefined' && window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
    return 'light'
  }

  // 从本地存储获取主题
  const getStoredTheme = (): Theme => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('co-novel-theme') as Theme
      return stored || getSystemTheme()
    }
    return 'light'
  }

  // 应用主题到DOM
  const applyTheme = (newTheme: Theme) => {
    if (typeof document !== 'undefined') {
      const root = document.documentElement
      
      // 移除旧的主题类
      root.classList.remove('light-theme', 'dark-theme')
      
      // 添加新的主题类
      root.classList.add(`${newTheme}-theme`)
      
      // 设置data属性（用于CSS选择器）
      root.setAttribute('data-theme', newTheme)
    }
  }

  // 切换主题
  const toggleTheme = () => {
    const newTheme = theme.value === 'light' ? 'dark' : 'light'
    setTheme(newTheme)
  }

  // 设置主题
  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme
    isDarkMode.value = newTheme === 'dark'
    
    // 保存到本地存储
    if (typeof window !== 'undefined') {
      localStorage.setItem('co-novel-theme', newTheme)
    }
    
    // 应用到DOM
    applyTheme(newTheme)
  }

  // 初始化主题
  const initTheme = () => {
    const initialTheme = getStoredTheme()
    setTheme(initialTheme)
    
    // 监听系统主题变化
    if (typeof window !== 'undefined' && window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      mediaQuery.addEventListener('change', (e) => {
        // 只有在用户没有手动设置主题时才自动切换
        const storedTheme = localStorage.getItem('co-novel-theme')
        if (!storedTheme) {
          setTheme(e.matches ? 'dark' : 'light')
        }
      })
    }
  }

  // 监听主题变化
  watch(theme, (newTheme) => {
    applyTheme(newTheme)
  })

  onMounted(() => {
    initTheme()
  })

  return {
    theme,
    isDarkMode,
    toggleTheme,
    setTheme,
    initTheme
  }
}