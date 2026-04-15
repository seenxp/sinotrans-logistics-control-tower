/**
 * 应用状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 状态
  const isDarkMode = ref(false)
  const sidebarCollapsed = ref(false)
  const loading = ref(false)
  const currentRoute = ref('')

  // 计算属性
  const themeMode = computed(() => (isDarkMode.value ? 'dark' : 'light'))

  // 方法
  function toggleDarkMode() {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
  }

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
    localStorage.setItem('sidebarCollapsed', String(sidebarCollapsed.value))
  }

  function setLoading(status: boolean) {
    loading.value = status
  }

  function initApp() {
    // 从localStorage恢复设置
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme) {
      isDarkMode.value = savedTheme === 'dark'
    }

    const savedSidebar = localStorage.getItem('sidebarCollapsed')
    if (savedSidebar) {
      sidebarCollapsed.value = savedSidebar === 'true'
    }
  }

  return {
    isDarkMode,
    sidebarCollapsed,
    loading,
    currentRoute,
    themeMode,
    toggleDarkMode,
    toggleSidebar,
    setLoading,
    initApp,
  }
})
