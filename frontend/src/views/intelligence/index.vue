<template>
  <div class="global-intelligence">
    <div class="intelligence-header">
      <h1>全球情报监控</h1>
      <p>实时全球情报数据，涵盖地缘政治、军事、金融、气候、网络、海事、航空等领域</p>
    </div>
    
    <div class="intelligence-iframe-container">
      <iframe
        :src="worldMonitorUrl"
        frameborder="0"
        class="worldmonitor-iframe"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// WorldMonitor 界面URL
// 可以配置为本地运行的实例或托管版本
const worldMonitorUrl = ref('http://localhost:40002')
</script>

<style lang="scss" scoped>
.global-intelligence {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.intelligence-header {
  margin-bottom: 16px;
  
  h1 {
    font-size: 24px;
    font-weight: 600;
    margin: 0 0 8px 0;
    background: linear-gradient(135deg, #1890ff, #722ed1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  p {
    color: var(--text-color-secondary);
    margin: 0;
    font-size: 14px;
  }
}

.intelligence-iframe-container {
  flex: 1;
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg-component);
  border: 1px solid var(--border-color-split);
}

.worldmonitor-iframe {
  width: 100%;
  height: 100%;
  min-height: calc(100vh - 200px);
}
</style>
