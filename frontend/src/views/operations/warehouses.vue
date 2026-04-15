<template>
  <div class="warehouses-page">
    <n-card title="仓库管理">
      <template #header-extra>
        <n-button type="primary" @click="handleAdd">
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
                <n-button size="small" quaternary @click="handleDetail(warehouse)">详情</n-button>
                <n-button size="small" quaternary type="primary" @click="handleManage(warehouse)">管理</n-button>
              </n-space>
            </template>
          </n-card>
        </n-grid-item>
      </n-grid>
    </n-card>

    <!-- 添加仓库弹窗 -->
    <n-modal v-model:show="showAddModal" preset="dialog" title="添加仓库" positive-text="确定" negative-text="取消" @positive-click="submitAdd">
      <n-form ref="formRef" :model="formData" label-placement="left" label-width="80">
        <n-form-item label="仓库名称" path="name">
          <n-input v-model:value="formData.name" placeholder="请输入仓库名称" />
        </n-form-item>
        <n-form-item label="地址" path="address">
          <n-input v-model:value="formData.address" placeholder="请输入地址" />
        </n-form-item>
        <n-form-item label="城市" path="city">
          <n-input v-model:value="formData.city" placeholder="请输入城市" />
        </n-form-item>
        <n-form-item label="容量(吨)" path="capacity">
          <n-input-number v-model:value="formData.capacity" :min="0" style="width: 100%" />
        </n-form-item>
      </n-form>
    </n-modal>

    <!-- 仓库详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" :title="currentWarehouse?.name" style="width: 600px;">
      <n-descriptions :column="2" label-placement="left" bordered>
        <n-descriptions-item label="仓库ID">{{ currentWarehouse?.id }}</n-descriptions-item>
        <n-descriptions-item label="状态">
          <n-tag :type="currentWarehouse?.status === 'active' ? 'success' : 'warning'">
            {{ currentWarehouse?.status === 'active' ? '运营中' : '维护中' }}
          </n-tag>
        </n-descriptions-item>
        <n-descriptions-item label="地址">{{ currentWarehouse?.address }}</n-descriptions-item>
        <n-descriptions-item label="城市">{{ currentWarehouse?.city }}</n-descriptions-item>
        <n-descriptions-item label="总容量">{{ currentWarehouse?.capacity }} 吨</n-descriptions-item>
        <n-descriptions-item label="当前库存">{{ currentWarehouse?.currentLoad }} 吨</n-descriptions-item>
        <n-descriptions-item label="使用率">
          <n-progress
            type="line"
            :percentage="Math.round((currentWarehouse?.currentLoad || 0) / (currentWarehouse?.capacity || 1) * 100)"
            :color="getProgressColor((currentWarehouse?.currentLoad || 0) / (currentWarehouse?.capacity || 1))"
          />
        </n-descriptions-item>
      </n-descriptions>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showDetailModal = false">关闭</n-button>
          <n-button type="primary" @click="handleManage(currentWarehouse)">管理</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 仓库管理弹窗 -->
    <n-modal v-model:show="showManageModal" preset="card" :title="`管理 - ${currentWarehouse?.name}`" style="width: 700px;">
      <n-tabs type="line">
        <n-tab-pane name="info" tab="基本信息">
          <n-form label-placement="left" label-width="80">
            <n-form-item label="仓库名称">
              <n-input v-model:value="editForm.name" />
            </n-form-item>
            <n-form-item label="地址">
              <n-input v-model:value="editForm.address" />
            </n-form-item>
            <n-form-item label="城市">
              <n-input v-model:value="editForm.city" />
            </n-form-item>
            <n-form-item label="容量(吨)">
              <n-input-number v-model:value="editForm.capacity" :min="0" style="width: 100%" />
            </n-form-item>
            <n-form-item label="状态">
              <n-select v-model:value="editForm.status" :options="statusOptions" />
            </n-form-item>
          </n-form>
        </n-tab-pane>
        <n-tab-pane name="inventory" tab="库存管理">
          <n-data-table :columns="inventoryColumns" :data="inventoryData" />
        </n-tab-pane>
        <n-tab-pane name="operations" tab="出入库记录">
          <n-data-table :columns="operationColumns" :data="operationData" />
        </n-tab-pane>
      </n-tabs>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showManageModal = false">取消</n-button>
          <n-button type="primary" @click="saveChanges">保存修改</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { useMessage } from 'naive-ui'
import { AddOutline, BusinessOutline } from '@vicons/ionicons5'

const message = useMessage()

const warehouses = ref([
  { id: 'WH001', name: '北京中央仓库', address: '大兴区物流园区', city: '北京', capacity: 10000, currentLoad: 7500, status: 'active' },
  { id: 'WH002', name: '上海分拨中心', address: '浦东新区自贸区', city: '上海', capacity: 15000, currentLoad: 12000, status: 'active' },
  { id: 'WH003', name: '广州南部中心', address: '白云区物流港', city: '广州', capacity: 8000, currentLoad: 5600, status: 'active' },
  { id: 'WH004', name: '深圳跨境仓库', address: '前海自贸区', city: '深圳', capacity: 12000, currentLoad: 9600, status: 'active' },
  { id: 'WH005', name: '成都西部枢纽', address: '双流区物流园', city: '成都', capacity: 6000, currentLoad: 3600, status: 'active' },
])

const showAddModal = ref(false)
const showDetailModal = ref(false)
const showManageModal = ref(false)
const currentWarehouse = ref<any>(null)

const formData = ref({
  name: '',
  address: '',
  city: '',
  capacity: 1000
})

const editForm = ref({
  name: '',
  address: '',
  city: '',
  capacity: 0,
  status: 'active'
})

const statusOptions = [
  { label: '运营中', value: 'active' },
  { label: '维护中', value: 'maintenance' }
]

const inventoryColumns = [
  { title: '货物名称', key: 'name' },
  { title: '数量', key: 'quantity' },
  { title: '重量(吨)', key: 'weight' },
  { title: '入库时间', key: 'time' }
]

const inventoryData = ref([
  { name: '电子产品', quantity: 500, weight: 2.5, time: '2026-04-15 10:00' },
  { name: '服装', quantity: 2000, weight: 5.0, time: '2026-04-14 15:30' },
  { name: '食品', quantity: 300, weight: 3.0, time: '2026-04-14 09:00' },
])

const operationColumns = [
  { title: '类型', key: 'type', render: (row: any) => h('span', { style: { color: row.type === '入库' ? '#52c41a' : '#1890ff' } }, row.type) },
  { title: '货物', key: 'cargo' },
  { title: '数量', key: 'quantity' },
  { title: '时间', key: 'time' }
]

const operationData = ref([
  { type: '入库', cargo: '电子产品', quantity: 500, time: '2026-04-15 10:00' },
  { type: '出库', cargo: '服装', quantity: 800, time: '2026-04-15 08:30' },
  { type: '入库', cargo: '食品', quantity: 300, time: '2026-04-14 15:00' },
])

function getProgressColor(ratio: number) {
  if (ratio < 0.6) return '#52c41a'
  if (ratio < 0.8) return '#faad14'
  return '#f5222d'
}

function handleAdd() {
  formData.value = { name: '', address: '', city: '', capacity: 1000 }
  showAddModal.value = true
}

function submitAdd() {
  if (!formData.value.name || !formData.value.address || !formData.value.city) {
    message.error('请填写完整信息')
    return false
  }
  
  const newWarehouse = {
    id: `WH${String(warehouses.value.length + 1).padStart(3, '0')}`,
    name: formData.value.name,
    address: formData.value.address,
    city: formData.value.city,
    capacity: formData.value.capacity,
    currentLoad: 0,
    status: 'active'
  }
  
  warehouses.value.push(newWarehouse)
  message.success('添加成功')
  showAddModal.value = false
  return true
}

function handleDetail(warehouse: any) {
  currentWarehouse.value = warehouse
  showDetailModal.value = true
}

function handleManage(warehouse: any) {
  currentWarehouse.value = warehouse
  editForm.value = {
    name: warehouse.name,
    address: warehouse.address,
    city: warehouse.city,
    capacity: warehouse.capacity,
    status: warehouse.status
  }
  showDetailModal.value = false
  showManageModal.value = true
}

function saveChanges() {
  if (currentWarehouse.value) {
    const index = warehouses.value.findIndex(w => w.id === currentWarehouse.value.id)
    if (index !== -1) {
      warehouses.value[index] = {
        ...warehouses.value[index],
        name: editForm.value.name,
        address: editForm.value.address,
        city: editForm.value.city,
        capacity: editForm.value.capacity,
        status: editForm.value.status
      }
      message.success('保存成功')
      showManageModal.value = false
    }
  }
}
</script>

<style scoped>
.warehouses-page { padding: 24px; }
</style>