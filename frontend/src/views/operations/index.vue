<template>
  <div class="operations-container">
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
import { DocumentTextOutline, CarOutline, HomeOutline, HardwareChipOutline } from '@vicons/ionicons5'

const router = useRouter()
const route = useRoute()

const activeKey = ref(route.path.split('/').pop() || 'orders')

const menuOptions = [
  {
    label: '订单管理',
    key: 'orders',
    icon: () => h(NIcon, null, { default: () => h(DocumentTextOutline) }),
  },
  {
    label: '车辆管理',
    key: 'vehicles',
    icon: () => h(NIcon, null, { default: () => h(CarOutline) }),
  },
  {
    label: '设备管理',
    key: 'equipment',
    icon: () => h(NIcon, null, { default: () => h(HardwareChipOutline) }),
  },
  {
    label: '仓库管理',
    key: 'warehouses',
    icon: () => h(NIcon, null, { default: () => h(HomeOutline) }),
  },
]

function handleMenuSelect(key: string) {
  activeKey.value = key
  router.push(`/operations/${key}`)
}
</script>

<style lang="scss" scoped>
.operations-container {
  height: 100vh;
}
</style>
