<template>
  <div class="prediction-container">
    <n-layout has-sider>
      <n-layout-sider bordered width="200">
        <n-menu
          :options="menuOptions"
          :value="activeKey"
          @update:value="handleMenuSelect"
        />
      </n-layout-sider>
      <n-layout-content>
        <router-view />
      </n-layout-content>
    </n-layout>
  </div>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NIcon } from 'naive-ui'
import {
  TrendingUpOutline,
  CarOutline,
  WalletOutline,
  WarningOutline,
} from '@vicons/ionicons5'

const router = useRouter()
const route = useRoute()

const activeKey = ref(route.path.split('/').pop() || 'demand')

const menuOptions = [
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
]

function handleMenuSelect(key: string) {
  activeKey.value = key
  router.push(`/prediction/${key}`)
}
</script>

<style lang="scss" scoped>
.prediction-container {
  height: 100vh;
}
</style>
