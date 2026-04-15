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

    <!-- 添加车辆弹窗 -->
    <n-modal v-model:show="showCreateModal" preset="card" title="添加车辆" style="width: 600px">
      <n-form :model="formData" label-placement="left" label-width="80">
        <n-form-item label="车牌号">
          <n-input v-model:value="formData.plateNumber" placeholder="请输入车牌号" />
        </n-form-item>
        <n-form-item label="车辆类型">
          <n-select v-model:value="formData.type" :options="typeOptions" />
        </n-form-item>
        <n-form-item label="载重(吨)">
          <n-input-number v-model:value="formData.capacity" :min="0" style="width: 100%" />
        </n-form-item>
        <n-form-item label="当前位置">
          <n-input v-model:value="formData.location" placeholder="请输入当前位置" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showCreateModal = false">取消</n-button>
          <n-button type="primary" @click="handleCreate">确定</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 车辆详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="车辆详情" style="width: 600px">
      <n-descriptions :column="2" label-placement="left" bordered v-if="currentVehicle">
        <n-descriptions-item label="车辆编号">{{ currentVehicle.id }}</n-descriptions-item>
        <n-descriptions-item label="车牌号">{{ currentVehicle.plateNumber }}</n-descriptions-item>
        <n-descriptions-item label="类型">{{ getTypeLabel(currentVehicle.type) }}</n-descriptions-item>
        <n-descriptions-item label="载重">{{ currentVehicle.capacity }} 吨</n-descriptions-item>
        <n-descriptions-item label="状态">
          <n-tag :type="getStatusType(currentVehicle.status)">{{ getStatusLabel(currentVehicle.status) }}</n-tag>
        </n-descriptions-item>
        <n-descriptions-item label="当前位置">{{ currentVehicle.location }}</n-descriptions-item>
      </n-descriptions>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showDetailModal = false">关闭</n-button>
          <n-button type="primary" @click="handleEdit(currentVehicle)">编辑</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 编辑车辆弹窗 -->
    <n-modal v-model:show="showEditModal" preset="card" title="编辑车辆" style="width: 600px">
      <n-form :model="editForm" label-placement="left" label-width="80">
        <n-form-item label="车牌号">
          <n-input v-model:value="editForm.plateNumber" />
        </n-form-item>
        <n-form-item label="车辆类型">
          <n-select v-model:value="editForm.type" :options="typeOptions" />
        </n-form-item>
        <n-form-item label="载重(吨)">
          <n-input-number v-model:value="editForm.capacity" :min="0" style="width: 100%" />
        </n-form-item>
        <n-form-item label="状态">
          <n-select v-model:value="editForm.status" :options="statusOptions" />
        </n-form-item>
        <n-form-item label="当前位置">
          <n-input v-model:value="editForm.location" />
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
const currentVehicle = ref<any>(null)

const formData = reactive({
  plateNumber: '',
  type: 'truck',
  capacity: 10,
  location: '',
})

const editForm = reactive({
  plateNumber: '',
  type: '',
  capacity: 0,
  status: '',
  location: '',
})

const typeOptions = [
  { label: '卡车', value: 'truck' },
  { label: '船舶', value: 'ship' },
  { label: '飞机', value: 'plane' },
  { label: '火车', value: 'train' },
]

const statusOptions = [
  { label: '运行中', value: 'active' },
  { label: '空闲', value: 'idle' },
  { label: '维护中', value: 'maintenance' },
]

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
    render: (row: any) => h(NSpace, {}, {
      default: () => [
        h(NButton, { size: 'small', quaternary: true, onClick: () => handleLocate(row) }, { default: () => '定位' }),
        h(NButton, { size: 'small', quaternary: true, type: 'primary', onClick: () => handleView(row) }, { default: () => '详情' }),
      ],
    }),
  },
]

function handleLocate(vehicle: any) {
  message.info(`正在定位车辆 ${vehicle.plateNumber}...`)
}

function handleView(vehicle: any) {
  currentVehicle.value = vehicle
  showDetailModal.value = true
}

function handleEdit(vehicle: any) {
  currentVehicle.value = vehicle
  editForm.plateNumber = vehicle.plateNumber
  editForm.type = vehicle.type
  editForm.capacity = vehicle.capacity
  editForm.status = vehicle.status
  editForm.location = vehicle.location
  showDetailModal.value = false
  showEditModal.value = true
}

function saveEdit() {
  if (currentVehicle.value) {
    const index = vehicles.value.findIndex(v => v.id === currentVehicle.value.id)
    if (index !== -1) {
      vehicles.value[index] = {
        ...vehicles.value[index],
        plateNumber: editForm.plateNumber,
        type: editForm.type,
        capacity: editForm.capacity,
        status: editForm.status,
        location: editForm.location,
      }
      message.success('保存成功')
      showEditModal.value = false
    }
  }
}

function handleCreate() {
  if (!formData.plateNumber || !formData.location) {
    message.error('请填写完整信息')
    return
  }
  
  const newVehicle = {
    id: `V${String(vehicles.value.length + 1).padStart(3, '0')}`,
    plateNumber: formData.plateNumber,
    type: formData.type,
    capacity: formData.capacity,
    status: 'active',
    location: formData.location,
  }
  
  vehicles.value.push(newVehicle)
  message.success('添加成功')
  showCreateModal.value = false
  
  // 重置表单
  formData.plateNumber = ''
  formData.type = 'truck'
  formData.capacity = 10
  formData.location = ''
}
</script>

<style scoped>
.vehicles-page { padding: 24px; }
</style>