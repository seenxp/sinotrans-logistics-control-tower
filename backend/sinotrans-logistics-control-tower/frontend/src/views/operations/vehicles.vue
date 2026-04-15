<template>
  <div class="vehicles-page">
    <n-card title="车辆管理">
      <template #header-extra>
        <n-button type="primary" @click="showCreateModal = true">
          <template #icon>
            <n-icon><add-outline /></n-icon>
          </template>
          添加车辆
        </n-button>
      </template>

      <!-- 统计卡片 -->
      <n-grid :cols="4" :x-gap="16" :y-gap="16" style="margin-bottom: 24px">
        <n-grid-item>
          <n-card size="small">
            <n-statistic label="总车辆" :value="280" />
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card size="small">
            <n-statistic label="在线" :value="245" />
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card size="small">
            <n-statistic label="空闲" :value="28" />
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card size="small">
            <n-statistic label="维护中" :value="7" />
          </n-card>
        </n-grid-item>
      </n-grid>

      <!-- 数据表格 -->
      <n-data-table
        :columns="columns"
        :data="vehicles"
        :loading="loading"
        :pagination="pagination"
        :bordered="false"
      />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { NTag, NSpace, NButton } from 'naive-ui'
import { AddOutline } from '@vicons/ionicons5'

const loading = ref(false)
const showCreateModal = ref(false)

const vehicles = ref([
  { id: 'V001', plateNumber: '京A12345', type: 'truck', capacity: 10, status: 'active', location: '北京-上海高速' },
  { id: 'V002', plateNumber: '沪B54321', type: 'truck', capacity: 15, status: 'active', location: '上海分拨中心' },
  { id: 'V003', plateNumber: 'SHIP001', type: 'ship', capacity: 1000, status: 'active', location: '深圳港口' },
  { id: 'V004', plateNumber: '粤C88888', type: 'truck', capacity: 8, status: 'idle', location: '广州仓库' },
  { id: 'V005', plateNumber: 'PLANE01', type: 'plane', capacity: 5, status: 'maintenance', location: '北京机场' },
])

const pagination = { pageSize: 10 }

const getTypeLabel = (type: string) => {
  const labels: Record<string, string> = { truck: '卡车', ship: '船舶', plane: '飞机', train: '火车' }
  return labels[type] || type
}

const getStatusType = (status: string) => {
  const types: Record<string, 'success' | 'default' | 'warning'> = {
    active: 'success',
    idle: 'default',
    maintenance: 'warning',
  }
  return types[status] || 'default'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = { active: '运行中', idle: '空闲', maintenance: '维护中' }
  return labels[status] || status
}

const columns = [
  { title: '车辆编号', key: 'id' },
  { title: '车牌号', key: 'plateNumber' },
  { title: '类型', key: 'type', render: (row: any) => getTypeLabel(row.type) },
  { title: '载重(吨)', key: 'capacity' },
  {
    title: '状态',
    key: 'status',
    render: (row: any) => h(NTag, { type: getStatusType(row.status) }, { default: () => getStatusLabel(row.status) }),
  },
  { title: '当前位置', key: 'location' },
  {
    title: '操作',
    key: 'actions',
    render: () => h(NSpace, {}, {
      default: () => [
        h(NButton, { size: 'small', quaternary: true }, { default: () => '定位' }),
        h(NButton, { size: 'small', quaternary: true, type: 'primary' }, { default: () => '详情' }),
      ],
    }),
  },
]
</script>

<style scoped>
.vehicles-page { padding: 24px; }
</style>
