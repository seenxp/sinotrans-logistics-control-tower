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

    <!-- 订单详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="订单详情" style="width: 600px">
      <n-descriptions :column="2" label-placement="left" bordered v-if="currentOrder">
        <n-descriptions-item label="订单编号">{{ currentOrder.id }}</n-descriptions-item>
        <n-descriptions-item label="状态">
          <n-tag :type="getStatusType(currentOrder.status)">{{ getStatusLabel(currentOrder.status) }}</n-tag>
        </n-descriptions-item>
        <n-descriptions-item label="起点">{{ currentOrder.origin }}</n-descriptions-item>
        <n-descriptions-item label="终点">{{ currentOrder.destination }}</n-descriptions-item>
        <n-descriptions-item label="货物类型">{{ currentOrder.cargoType }}</n-descriptions-item>
        <n-descriptions-item label="重量">{{ currentOrder.weight }} kg</n-descriptions-item>
        <n-descriptions-item label="优先级">
          <n-tag :type="getPriorityType(currentOrder.priority)">{{ currentOrder.priority.toUpperCase() }}</n-tag>
        </n-descriptions-item>
        <n-descriptions-item label="创建时间">{{ currentOrder.createdAt }}</n-descriptions-item>
      </n-descriptions>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showDetailModal = false">关闭</n-button>
          <n-button type="primary" @click="handleEdit(currentOrder)">编辑</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 编辑订单弹窗 -->
    <n-modal v-model:show="showEditModal" preset="card" title="编辑订单" style="width: 600px">
      <n-form ref="editFormRef" :model="editForm" label-placement="left" label-width="80">
        <n-form-item label="起点" path="origin">
          <n-input v-model:value="editForm.origin" />
        </n-form-item>
        <n-form-item label="终点" path="destination">
          <n-input v-model:value="editForm.destination" />
        </n-form-item>
        <n-form-item label="货物类型" path="cargoType">
          <n-input v-model:value="editForm.cargoType" />
        </n-form-item>
        <n-form-item label="重量(kg)" path="weight">
          <n-input-number v-model:value="editForm.weight" :min="0" style="width: 100%" />
        </n-form-item>
        <n-form-item label="状态" path="status">
          <n-select v-model:value="editForm.status" :options="statusOptions" />
        </n-form-item>
        <n-form-item label="优先级" path="priority">
          <n-select v-model:value="editForm.priority" :options="priorityOptions" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showEditModal = false">取消</n-button>
          <n-button type="primary" @click="saveEdit">保存</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, h } from 'vue'
import { NTag, NSpace, NButton, useMessage } from 'naive-ui'
import { AddOutline } from '@vicons/ionicons5'

const message = useMessage()
const loading = ref(false)
const showCreateModal = ref(false)
const showDetailModal = ref(false)
const showEditModal = ref(false)
const currentOrder = ref<any>(null)

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

const editForm = reactive({
  origin: '',
  destination: '',
  cargoType: '',
  weight: 0,
  status: '',
  priority: '',
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
  { id: 'ORD001', origin: '北京', destination: '上海', cargoType: '电子产品', weight: 500, status: 'in_transit', priority: 'high', createdAt: '2026-04-15' },
  { id: 'ORD002', origin: '广州', destination: '深圳', cargoType: '服装', weight: 200, status: 'processing', priority: 'normal', createdAt: '2026-04-15' },
  { id: 'ORD003', origin: '成都', destination: '重庆', cargoType: '食品', weight: 300, status: 'pending', priority: 'urgent', createdAt: '2026-04-15' },
  { id: 'ORD004', origin: '杭州', destination: '南京', cargoType: '建材', weight: 800, status: 'delivered', priority: 'low', createdAt: '2026-04-14' },
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
        h(NButton, { size: 'small', quaternary: true, onClick: () => handleView(row) }, { default: () => '查看' }),
        h(NButton, { size: 'small', quaternary: true, type: 'primary', onClick: () => handleEdit(row) }, { default: () => '编辑' }),
      ],
    }),
  },
]

function handleSearch() {
  message.info('查询功能开发中...')
}

function handleReset() {
  filterForm.status = null
  filterForm.priority = null
  message.success('已重置筛选条件')
}

function handlePageChange(page: number) {
  console.log('Page:', page)
}

function handleView(order: any) {
  currentOrder.value = order
  showDetailModal.value = true
}

function handleEdit(order: any) {
  currentOrder.value = order
  editForm.origin = order.origin
  editForm.destination = order.destination
  editForm.cargoType = order.cargoType
  editForm.weight = order.weight
  editForm.status = order.status
  editForm.priority = order.priority
  showDetailModal.value = false
  showEditModal.value = true
}

function saveEdit() {
  if (currentOrder.value) {
    const index = orders.value.findIndex(o => o.id === currentOrder.value.id)
    if (index !== -1) {
      orders.value[index] = {
        ...orders.value[index],
        origin: editForm.origin,
        destination: editForm.destination,
        cargoType: editForm.cargoType,
        weight: editForm.weight,
        status: editForm.status,
        priority: editForm.priority,
      }
      message.success('保存成功')
      showEditModal.value = false
    }
  }
}

function handleCreateOrder() {
  if (!formData.origin || !formData.destination || !formData.cargoType) {
    message.error('请填写完整信息')
    return
  }
  
  const newOrder = {
    id: `ORD${String(orders.value.length + 1).padStart(3, '0')}`,
    origin: formData.origin,
    destination: formData.destination,
    cargoType: formData.cargoType,
    weight: formData.weight,
    status: 'pending',
    priority: formData.priority,
    createdAt: new Date().toISOString().split('T')[0],
  }
  
  orders.value.unshift(newOrder)
  message.success('创建成功')
  showCreateModal.value = false
  
  // 重置表单
  formData.origin = ''
  formData.destination = ''
  formData.cargoType = ''
  formData.weight = 0
  formData.priority = 'normal'
}
</script>

<style lang="scss" scoped>
.orders-page {
  padding: 24px;
}
</style>