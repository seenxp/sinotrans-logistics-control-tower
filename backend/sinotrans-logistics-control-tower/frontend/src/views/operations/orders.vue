<template>
  <div class="orders-page">
    <n-card title="订单管理">
      <template #header-extra>
        <n-space>
          <n-button type="primary" @click="showCreateModal = true">
            <template #icon>
              <n-icon><add-outline /></n-icon>
            </template>
            新建订单
          </n-button>
        </n-space>
      </template>

      <!-- 搜索过滤 -->
      <n-form inline :model="filterForm">
        <n-form-item label="订单状态">
          <n-select
            v-model:value="filterForm.status"
            :options="statusOptions"
            clearable
            placeholder="全部状态"
            style="width: 150px"
          />
        </n-form-item>
        <n-form-item label="优先级">
          <n-select
            v-model:value="filterForm.priority"
            :options="priorityOptions"
            clearable
            placeholder="全部优先级"
            style="width: 150px"
          />
        </n-form-item>
        <n-form-item>
          <n-button type="primary" @click="handleSearch">查询</n-button>
          <n-button style="margin-left: 8px" @click="handleReset">重置</n-button>
        </n-form-item>
      </n-form>

      <n-divider />

      <!-- 数据表格 -->
      <n-data-table
        :columns="columns"
        :data="orders"
        :loading="loading"
        :pagination="pagination"
        :bordered="false"
        :single-line="false"
        @update:page="handlePageChange"
      />
    </n-card>

    <!-- 创建订单弹窗 -->
    <n-modal v-model:show="showCreateModal" preset="card" title="新建订单" style="width: 600px">
      <n-form ref="formRef" :model="formData" label-placement="left" label-width="80">
        <n-form-item label="起点" path="origin">
          <n-input v-model:value="formData.origin" placeholder="请输入起点" />
        </n-form-item>
        <n-form-item label="终点" path="destination">
          <n-input v-model:value="formData.destination" placeholder="请输入终点" />
        </n-form-item>
        <n-form-item label="货物类型" path="cargoType">
          <n-input v-model:value="formData.cargoType" placeholder="请输入货物类型" />
        </n-form-item>
        <n-form-item label="重量(kg)" path="weight">
          <n-input-number v-model:value="formData.weight" :min="0" style="width: 100%" />
        </n-form-item>
        <n-form-item label="优先级" path="priority">
          <n-select v-model:value="formData.priority" :options="priorityOptions" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showCreateModal = false">取消</n-button>
          <n-button type="primary" @click="handleCreateOrder">确定</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, h } from 'vue'
import { NTag, NSpace, NButton } from 'naive-ui'
import { AddOutline } from '@vicons/ionicons5'

const loading = ref(false)
const showCreateModal = ref(false)

const filterForm = reactive({
  status: null,
  priority: null,
})

const formData = reactive({
  origin: '',
  destination: '',
  cargoType: '',
  weight: 0,
  priority: 'normal',
})

const statusOptions = [
  { label: '待处理', value: 'pending' },
  { label: '处理中', value: 'processing' },
  { label: '运输中', value: 'in_transit' },
  { label: '已送达', value: 'delivered' },
]

const priorityOptions = [
  { label: '低', value: 'low' },
  { label: '普通', value: 'normal' },
  { label: '高', value: 'high' },
  { label: '紧急', value: 'urgent' },
]

const orders = ref([
  { id: 'ORD001', origin: '北京', destination: '上海', cargoType: '电子产品', weight: 500, status: 'in_transit', priority: 'high', createdAt: '2024-04-15' },
  { id: 'ORD002', origin: '广州', destination: '深圳', cargoType: '服装', weight: 200, status: 'processing', priority: 'normal', createdAt: '2024-04-15' },
  { id: 'ORD003', origin: '成都', destination: '重庆', cargoType: '食品', weight: 300, status: 'pending', priority: 'urgent', createdAt: '2024-04-15' },
  { id: 'ORD004', origin: '杭州', destination: '南京', cargoType: '建材', weight: 800, status: 'delivered', priority: 'low', createdAt: '2024-04-14' },
])

const pagination = {
  pageSize: 10,
  showQuickJumper: true,
}

const getStatusType = (status: string) => {
  const types: Record<string, 'default' | 'primary' | 'info' | 'success' | 'warning'> = {
    pending: 'default',
    processing: 'info',
    in_transit: 'primary',
    delivered: 'success',
  }
  return types[status] || 'default'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    in_transit: '运输中',
    delivered: '已送达',
  }
  return labels[status] || status
}

const getPriorityType = (priority: string) => {
  const types: Record<string, 'default' | 'success' | 'warning' | 'error'> = {
    low: 'default',
    normal: 'success',
    high: 'warning',
    urgent: 'error',
  }
  return types[priority] || 'default'
}

const columns = [
  { title: '订单编号', key: 'id', width: 100 },
  { title: '起点', key: 'origin' },
  { title: '终点', key: 'destination' },
  { title: '货物类型', key: 'cargoType' },
  { title: '重量(kg)', key: 'weight' },
  {
    title: '状态',
    key: 'status',
    render: (row: any) => h(NTag, { type: getStatusType(row.status) }, { default: () => getStatusLabel(row.status) }),
  },
  {
    title: '优先级',
    key: 'priority',
    render: (row: any) => h(NTag, { type: getPriorityType(row.priority) }, { default: () => row.priority.toUpperCase() }),
  },
  { title: '创建时间', key: 'createdAt' },
  {
    title: '操作',
    key: 'actions',
    render: (row: any) => h(NSpace, {}, {
      default: () => [
        h(NButton, { size: 'small', quaternary: true }, { default: () => '查看' }),
        h(NButton, { size: 'small', quaternary: true, type: 'primary' }, { default: () => '编辑' }),
      ],
    }),
  },
]

function handleSearch() {
  console.log('Search:', filterForm)
}

function handleReset() {
  filterForm.status = null
  filterForm.priority = null
}

function handlePageChange(page: number) {
  console.log('Page:', page)
}

function handleCreateOrder() {
  console.log('Create order:', formData)
  showCreateModal.value = false
}
</script>

<style lang="scss" scoped>
.orders-page {
  padding: 24px;
}
</style>
