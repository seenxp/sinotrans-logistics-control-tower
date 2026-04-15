<template>
  <n-layout has-sider class="main-layout">
    <!-- 侧边栏 -->
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="220"
      show-trigger
      :collapsed="collapsed"
      @collapse="collapsed = true"
      @expand="collapsed = false"
      class="main-sider"
    >
      <div class="logo">
        <span class="logo-icon">🌐</span>
        <span class="logo-text" v-if="!collapsed">外运物流控制塔</span>
      </div>
      <n-menu
        :collapsed="collapsed"
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="menuOptions"
        :value="activeKey"
        @update:value="handleMenuSelect"
      />
    </n-layout-sider>

    <!-- 主内容区 -->
    <n-layout>
      <!-- 顶部导航 -->
      <n-layout-header bordered class="main-header">
        <div class="header-left">
          <n-breadcrumb>
            <n-breadcrumb-item v-for="item in breadcrumbs" :key="item.path">
              {{ item.title }}
            </n-breadcrumb-item>
          </n-breadcrumb>
        </div>
        <div class="header-right">
          <n-space>
            <n-button quaternary circle @click="refreshData">
              <template #icon>
                <n-icon><refresh-outline /></n-icon>
              </template>
            </n-button>
            <n-button quaternary circle @click="toggleFullscreen">
              <template #icon>
                <n-icon><scan-outline /></n-icon>
              </template>
            </n-button>
            <n-dropdown :options="userOptions" @select="handleUserAction">
              <n-avatar round size="small">
                <n-icon><person-outline /></n-icon>
              </n-avatar>
            </n-dropdown>
          </n-space>
        </div>
      </n-layout-header>

      <!-- 内容区 -->
      <n-layout-content class="main-content">
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NIcon, useMessage, useDialog } from 'naive-ui'
import {
  HomeOutline,
  TrendingUpOutline,
  CarOutline,
  WalletOutline,
  WarningOutline,
  PeopleOutline,
  BusOutline,
  BusinessOutline,
  AnalyticsOutline,
  SettingsOutline,
  RefreshOutline,
  ScanOutline,
  PersonOutline,
} from '@vicons/ionicons5'

const router = useRouter()
const route = useRoute()
const message = useMessage()
const dialog = useDialog()

const collapsed = ref(false)

// 当前激活的菜单项
const activeKey = computed(() => {
  const path = route.path
  if (path.startsWith('/prediction')) return path.split('/')[2] || 'demand'
  if (path.startsWith('/operations')) return path.split('/')[2] || 'orders'
  if (path === '/dashboard') return 'dashboard'
  if (path === '/monitor') return 'monitor'
  if (path === '/data') return 'data'
  return 'dashboard'
})

// 面包屑
const breadcrumbs = computed(() => {
  const path = route.path
  const items = [{ path: '/dashboard', title: '控制台' }]

  if (path.startsWith('/prediction')) {
    items.push({ path: '/prediction', title: '预测分析' })
    const subPath = path.split('/')[2]
    if (subPath === 'demand') items.push({ path: '/prediction/demand', title: '需求预测' })
    else if (subPath === 'capacity') items.push({ path: '/prediction/capacity', title: '运力预测' })
    else if (subPath === 'cost') items.push({ path: '/prediction/cost', title: '成本预测' })
    else if (subPath === 'risk') items.push({ path: '/prediction/risk', title: '风险预测' })
  } else if (path.startsWith('/operations')) {
    items.push({ path: '/operations', title: '运营指挥' })
    const subPath = path.split('/')[2]
    if (subPath === 'orders') items.push({ path: '/operations/orders', title: '订单管理' })
    else if (subPath === 'vehicles') items.push({ path: '/operations/vehicles', title: '车辆管理' })
    else if (subPath === 'warehouses') items.push({ path: '/operations/warehouses', title: '仓库管理' })
  } else if (path === '/monitor') {
    items.push({ path: '/monitor', title: '实时监控' })
  } else if (path === '/data') {
    items.push({ path: '/data', title: '数据治理' })
  }

  return items
})

// 菜单配置
const menuOptions = [
  {
    label: '控制台',
    key: 'dashboard',
    icon: () => h(NIcon, null, { default: () => h(HomeOutline) }),
  },
  {
    label: '实时监控',
    key: 'monitor',
    icon: () => h(NIcon, null, { default: () => h(AnalyticsOutline) }),
  },
  {
    label: '预测分析',
    key: 'prediction',
    icon: () => h(NIcon, null, { default: () => h(TrendingUpOutline) }),
    children: [
      {
        label: '需求预测',
        key: 'demand',
        icon: () => h(NIcon, null, { default: () => h(TrendingUpOutline) }),
      },
      {
        label: '运力预测',
        key: 'capacity',
        icon: () => h(NIcon, null, { default: () => h(CarOutline) }),
      },
      {
        label: '成本预测',
        key: 'cost',
        icon: () => h(NIcon, null, { default: () => h(WalletOutline) }),
      },
      {
        label: '风险预测',
        key: 'risk',
        icon: () => h(NIcon, null, { default: () => h(WarningOutline) }),
      },
    ],
  },
  {
    label: '运营指挥',
    key: 'operations',
    icon: () => h(NIcon, null, { default: () => h(PeopleOutline) }),
    children: [
      {
        label: '订单管理',
        key: 'orders',
        icon: () => h(NIcon, null, { default: () => h(BusOutline) }),
      },
      {
        label: '车辆管理',
        key: 'vehicles',
        icon: () => h(NIcon, null, { default: () => h(CarOutline) }),
      },
      {
        label: '仓库管理',
        key: 'warehouses',
        icon: () => h(NIcon, null, { default: () => h(BusinessOutline) }),
      },
    ],
  },
  {
    label: '数据治理',
    key: 'data',
    icon: () => h(NIcon, null, { default: () => h(AnalyticsOutline) }),
  },
]

// 用户下拉菜单
const userOptions = [
  { label: '个人中心', key: 'profile' },
  { label: '系统设置', key: 'settings' },
  { type: 'divider', key: 'd1' },
  { label: '退出登录', key: 'logout' },
]

// 菜单选择
function handleMenuSelect(key: string) {
  switch (key) {
    case 'dashboard':
      router.push('/dashboard')
      break
    case 'monitor':
      router.push('/monitor')
      break
    case 'demand':
      router.push('/prediction/demand')
      break
    case 'capacity':
      router.push('/prediction/capacity')
      break
    case 'cost':
      router.push('/prediction/cost')
      break
    case 'risk':
      router.push('/prediction/risk')
      break
    case 'orders':
      router.push('/operations/orders')
      break
    case 'vehicles':
      router.push('/operations/vehicles')
      break
    case 'warehouses':
      router.push('/operations/warehouses')
      break
    case 'data':
      router.push('/data')
      break
  }
}

// 刷新数据
function refreshData() {
  message.success('数据已刷新')
  // 触发当前页面刷新
  window.location.reload()
}

// 切换全屏
function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    message.success('已进入全屏模式')
  } else {
    document.exitFullscreen()
    message.success('已退出全屏模式')
  }
}

// 用户操作
function handleUserAction(key: string) {
  switch (key) {
    case 'profile':
      message.info('个人中心功能开发中...')
      break
    case 'settings':
      message.info('系统设置功能开发中...')
      break
    case 'logout':
      dialog.warning({
        title: '退出登录',
        content: '确定要退出登录吗？',
        positiveText: '确定',
        negativeText: '取消',
        onPositiveClick: () => {
          message.success('已退出登录')
        },
      })
      break
  }
}
</script>

<style lang="scss" scoped>
.main-layout {
  height: 100vh;
}

.main-sider {
  .logo {
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid var(--border-color-split);

    .logo-icon {
      font-size: 24px;
      margin-right: 8px;
    }

    .logo-text {
      font-size: 16px;
      font-weight: bold;
      background: linear-gradient(135deg, #1890ff, #722ed1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
  }
}

.main-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: var(--bg-component);
}

.main-content {
  padding: 24px;
  background: var(--bg-layout);
  overflow: auto;
}
</style>