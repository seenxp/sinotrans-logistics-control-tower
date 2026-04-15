<template>
  <div class="warehouses-page">
    <n-card title="仓库管理">
      <template #header-extra>
        <n-button type="primary">
          <template #icon>
            <n-icon><add-outline /></n-icon>
          </template>
          添加仓库
        </n-button>
      </template>

      <n-grid :cols="3" :x-gap="16" :y-gap="16">
        <n-grid-item v-for="warehouse in warehouses" :key="warehouse.id">
          <n-card hoverable>
            <template #header>
              <n-space align="center">
                <n-icon size="24" color="#1890ff"><business-outline /></n-icon>
                <span>{{ warehouse.name }}</span>
              </n-space>
            </template>
            <template #header-extra>
              <n-tag :type="warehouse.status === 'active' ? 'success' : 'warning'">
                {{ warehouse.status === 'active' ? '运营中' : '维护中' }}
              </n-tag>
            </template>
            
            <n-descriptions :column="1" label-placement="left">
              <n-descriptions-item label="地址">{{ warehouse.address }}</n-descriptions-item>
              <n-descriptions-item label="城市">{{ warehouse.city }}</n-descriptions-item>
              <n-descriptions-item label="容量">{{ warehouse.capacity }} 吨</n-descriptions-item>
              <n-descriptions-item label="当前库存">{{ warehouse.currentLoad }} 吨</n-descriptions-item>
            </n-descriptions>
            
            <n-progress
              type="line"
              :percentage="Math.round(warehouse.currentLoad / warehouse.capacity * 100)"
              :color="getProgressColor(warehouse.currentLoad / warehouse.capacity)"
              style="margin-top: 16px"
            />
            
            <template #footer>
              <n-space justify="end">
                <n-button size="small" quaternary>详情</n-button>
                <n-button size="small" quaternary type="primary">管理</n-button>
              </n-space>
            </template>
          </n-card>
        </n-grid-item>
      </n-grid>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { AddOutline, BusinessOutline } from '@vicons/ionicons5'

const warehouses = ref([
  { id: 'WH001', name: '北京中央仓库', address: '大兴区物流园区', city: '北京', capacity: 10000, currentLoad: 7500, status: 'active' },
  { id: 'WH002', name: '上海分拨中心', address: '浦东新区自贸区', city: '上海', capacity: 15000, currentLoad: 12000, status: 'active' },
  { id: 'WH003', name: '广州南部中心', address: '白云区物流港', city: '广州', capacity: 8000, currentLoad: 5600, status: 'active' },
  { id: 'WH004', name: '深圳跨境仓库', address: '前海自贸区', city: '深圳', capacity: 12000, currentLoad: 9600, status: 'active' },
  { id: 'WH005', name: '成都西部枢纽', address: '双流区物流园', city: '成都', capacity: 6000, currentLoad: 3600, status: 'active' },
])

function getProgressColor(ratio: number) {
  if (ratio < 0.6) return '#52c41a'
  if (ratio < 0.8) return '#faad14'
  return '#f5222d'
}
</script>

<style scoped>
.warehouses-page { padding: 24px; }
</style>
