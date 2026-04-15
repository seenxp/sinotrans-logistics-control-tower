<template>
  <div class="not-found">
    <div class="content">
      <h1 class="code">404</h1>
      <h2 class="title">页面不存在</h2>
      <p class="description">抱歉，您访问的页面不存在或已被移除</p>
      <n-button type="primary" @click="goHome">
        返回首页
      </n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('/')
}
</script>

<style lang="scss" scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: var(--bg-layout);

  .content {
    text-align: center;

    .code {
      font-size: 120px;
      font-weight: bold;
      color: var(--primary-color);
      line-height: 1;
      margin-bottom: 16px;
    }

    .title {
      font-size: 24px;
      color: var(--text-primary);
      margin-bottom: 8px;
    }

    .description {
      font-size: 14px;
      color: var(--text-secondary);
      margin-bottom: 24px;
    }
  }
}
</style>
