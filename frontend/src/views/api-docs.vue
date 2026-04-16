<template>
  <div class="api-docs-container">
    <n-card title="开放接口文档" class="api-docs-card">
      <template #header-extra>
        <n-space>
          <n-button type="primary" @click="openInNewTab">
            <template #icon>
              <n-icon><OpenOutline /></n-icon>
            </template>
            新窗口打开
          </n-button>
          <n-button @click="refresh">
            <template #icon>
              <n-icon><RefreshOutline /></n-icon>
            </template>
            刷新
          </n-button>
        </n-space>
      </template>
      
      <div class="api-docs-content">
        <iframe 
          ref="iframeRef"
          :src="apiDocsUrl" 
          class="api-docs-iframe"
          frameborder="0"
          @load="onIframeLoad"
        ></iframe>
        
        <div v-if="loading" class="loading-overlay">
          <n-spin size="large" />
          <p>加载接口文档中...</p>
        </div>
        
        <div v-if="error" class="error-overlay">
          <n-result status="error" title="加载失败" :description="error">
            <template #footer>
              <n-button @click="refresh">重试</n-button>
            </template>
          </n-result>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { NCard, NSpace, NButton, NIcon, NSpin, NResult } from 'naive-ui'
import { OpenOutline, RefreshOutline } from '@vicons/ionicons5'

const iframeRef = ref<HTMLIFrameElement | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

// API文档URL - 使用相对路径，通过Nginx代理
const apiDocsUrl = computed(() => {
  return '/api-docs'
})

// 在新标签页中打开
function openInNewTab() {
  window.open(apiDocsUrl.value, '_blank')
}

// 刷新iframe
function refresh() {
  loading.value = true
  error.value = null
  
  if (iframeRef.value) {
    iframeRef.value.src = apiDocsUrl.value
  }
}

// iframe加载完成
function onIframeLoad() {
  loading.value = false
  
  // 检查是否加载成功
  try {
    if (iframeRef.value && iframeRef.value.contentWindow) {
      const iframeDoc = iframeRef.value.contentDocument || iframeRef.value.contentWindow.document
      if (iframeDoc.title.includes('404') || iframeDoc.body.innerHTML.includes('404 Not Found')) {
        error.value = '接口文档服务未启动或路径错误'
      }
    }
  } catch (e) {
    // 跨域访问会被阻止，这是正常的
    console.log('跨域访问受限，但文档可能已加载')
  }
}

// 组件挂载后检查文档是否可用
onMounted(() => {
  // 给iframe一些时间加载
  setTimeout(() => {
    if (loading.value) {
      // 如果还在加载，可能是网络问题
      console.log('API文档加载中...')
    }
  }, 5000)
})
</script>

<style lang="scss" scoped>
.api-docs-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.api-docs-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  
  :deep(.n-card__content) {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 0;
  }
}

.api-docs-content {
  flex: 1;
  position: relative;
  min-height: 600px;
}

.api-docs-iframe {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.loading-overlay,
.error-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.9);
  z-index: 10;
}

.loading-overlay {
  p {
    margin-top: 16px;
    color: #666;
  }
}
</style>