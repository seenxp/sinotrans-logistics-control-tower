<template>
  <div class="equipment-dashboard">
    <n-grid :cols="1" :y-gap="16">
      <!-- 全景图（中国地图） -->
      <n-grid-item>
        <n-card title="全景图" class="dashboard-card">
          <template #header-extra>
            <n-space>
              <n-tag type="info">实时数据</n-tag>
              <n-button size="small" @click="refreshMap">
                <template #icon>
                  <n-icon><RefreshOutline /></n-icon>
                </template>
              </n-button>
            </n-space>
          </template>
          <PanoramicMap ref="panoramicMapRef" />
        </n-card>
      </n-grid-item>

      <!-- 今天平均率（两个饼图） -->
      <n-grid-item>
        <n-card title="今天平均率" class="dashboard-card">
          <TodayAvgPie ref="todayAvgPieRef" />
        </n-card>
      </n-grid-item>

      <!-- 今天情况 -->
      <n-grid-item>
        <n-grid :cols="2" :x-gap="16">
          <!-- 各类设备在线率 -->
          <n-grid-item>
            <n-card title="今天情况 - 各类设备在线率" class="dashboard-card">
              <OnlineRateChart ref="onlineRateChartRef" />
            </n-card>
          </n-grid-item>

          <!-- 各类设备任务数 -->
          <n-grid-item>
            <n-card title="今天情况 - 各类设备任务数" class="dashboard-card">
              <TaskStatsChart ref="taskStatsChartRef" />
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-grid-item>

      <!-- 本周情况 -->
      <n-grid-item>
        <n-grid :cols="2" :x-gap="16">
          <!-- 本周各类设备任务数 -->
          <n-grid-item>
            <n-card title="本周情况 - 各类设备任务数" class="dashboard-card">
              <template #header-extra>
                <n-space>
                  <n-select
                    v-model:value="weekParkFilter"
                    :options="parkOptions"
                    placeholder="选择园区"
                    size="small"
                    style="width: 150px"
                  />
                  <n-button size="small" @click="refreshWeekTasks">
                    <template #icon>
                      <n-icon><RefreshOutline /></n-icon>
                    </template>
                  </n-button>
                </n-space>
              </template>
              <TrendChart
                ref="weekTasksChartRef"
                title=""
                time-range="week"
                data-type="tasks"
                :park="weekParkFilter"
              />
            </n-card>
          </n-grid-item>

          <!-- 本周各类设备使用时长 -->
          <n-grid-item>
            <n-card title="本周情况 - 各类设备使用时长" class="dashboard-card">
              <template #header-extra>
                <n-space>
                  <n-select
                    v-model:value="weekDurationParkFilter"
                    :options="parkOptions"
                    placeholder="选择园区"
                    size="small"
                    style="width: 150px"
                  />
                  <n-button size="small" @click="refreshWeekDuration">
                    <template #icon>
                      <n-icon><RefreshOutline /></n-icon>
                    </template>
                  </n-button>
                </n-space>
              </template>
              <TrendChart
                ref="weekDurationChartRef"
                title=""
                time-range="week"
                data-type="duration"
                :park="weekDurationParkFilter"
              />
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-grid-item>

      <!-- 月度情况 -->
      <n-grid-item>
        <n-grid :cols="2" :x-gap="16">
          <!-- 月度各类设备任务数 -->
          <n-grid-item>
            <n-card title="月度情况 - 各类设备任务数" class="dashboard-card">
              <template #header-extra>
                <n-space>
                  <n-select
                    v-model:value="monthParkFilter"
                    :options="parkOptions"
                    placeholder="选择园区"
                    size="small"
                    style="width: 150px"
                  />
                  <n-button size="small" @click="refreshMonthTasks">
                    <template #icon>
                      <n-icon><RefreshOutline /></n-icon>
                    </template>
                  </n-button>
                </n-space>
              </template>
              <TrendChart
                ref="monthTasksChartRef"
                title=""
                time-range="month"
                data-type="tasks"
                :park="monthParkFilter"
              />
            </n-card>
          </n-grid-item>

          <!-- 月度各类设备使用时长 -->
          <n-grid-item>
            <n-card title="月度情况 - 各类设备使用时长" class="dashboard-card">
              <template #header-extra>
                <n-space>
                  <n-select
                    v-model:value="monthDurationParkFilter"
                    :options="parkOptions"
                    placeholder="选择园区"
                    size="small"
                    style="width: 150px"
                  />
                  <n-button size="small" @click="refreshMonthDuration">
                    <template #icon>
                      <n-icon><RefreshOutline /></n-icon>
                    </template>
                  </n-button>
                </n-space>
              </template>
              <TrendChart
                ref="monthDurationChartRef"
                title=""
                time-range="month"
                data-type="duration"
                :park="monthDurationParkFilter"
              />
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-grid-item>

      <!-- 设备列表 -->
      <n-grid-item>
        <n-card title="设备实时状态列表" class="dashboard-card">
          <template #header-extra>
            <n-space>
              <n-select
                v-model:value="deviceTypeFilter"
                :options="deviceTypeOptions"
                placeholder="设备类型"
                clearable
                size="small"
                style="width: 120px"
              />
              <n-select
                v-model:value="parkFilter"
                :options="parkOptions"
                placeholder="选择园区"
                clearable
                size="small"
                style="width: 150px"
              />
              <n-select
                v-model:value="statusFilter"
                :options="statusOptions"
                placeholder="设备状态"
                clearable
                size="small"
                style="width: 120px"
              />
              <n-button type="primary" size="small" @click="loadDeviceList">
                <template #icon>
                  <n-icon><RefreshOutline /></n-icon>
                </template>
                刷新
              </n-button>
            </n-space>
          </template>

          <n-data-table
            :columns="columns"
            :data="deviceList"
            :pagination="pagination"
            :loading="loading"
            :row-class-name="rowClassName"
            size="small"
          />
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import {
  NGrid, NGridItem, NCard, NTag, NButton, NIcon, NSpace,
  NSelect, NDataTable, useMessage
} from 'naive-ui'
import { RefreshOutline } from '@vicons/ionicons5'
import PanoramicMap from '@/components/equipment/PanoramicMap.vue'
import TodayAvgPie from '@/components/equipment/TodayAvgPie.vue'
import OnlineRateChart from '@/components/equipment/OnlineRateChart.vue'
import TrendChart from '@/components/equipment/TrendChart.vue'
import TaskStatsChart from '@/components/equipment/TaskStatsChart.vue'

const message = useMessage()

// 组件引用
const panoramicMapRef = ref()
const todayAvgPieRef = ref()
const onlineRateChartRef = ref()
const weekTasksChartRef = ref()
const weekDurationChartRef = ref()
const monthTasksChartRef = ref()
const monthDurationChartRef = ref()
const taskStatsChartRef = ref()

// 筛选条件
const weekParkFilter = ref('all')
const weekDurationParkFilter = ref('all')
const monthParkFilter = ref('all')
const monthDurationParkFilter = ref('all')
const deviceTypeFilter = ref(null)
const parkFilter = ref(null)
const statusFilter = ref(null)

// 园区选项
const parkOptions = [
  { label: '全部园区', value: 'all' },
  { label: '上海奉贤', value: 'shanghai' },
  { label: '广州东勤', value: 'guangzhou' },
  { label: '重庆园区', value: 'chongqing' }
]

// 设备类型选项
const deviceTypeOptions = [
  { label: '小悠盘', value: 'xiaoyou' },
  { label: '小寻叉', value: 'xiaoxun' },
  { label: 'AGV', value: 'agv' },
  { label: 'AGF', value: 'agf' },
  { label: 'CTU', value: 'ctu' },
  { label: '自动线体', value: 'autoLine' },
  { label: 'DWS', value: 'dws' }
]

// 设备状态选项
const statusOptions = [
  { label: '在线', value: 'online' },
  { label: '离线', value: 'offline' },
  { label: '故障', value: 'error' },
  { label: '空闲', value: 'idle' },
  { label: '执行任务', value: 'working' }
]

// 设备列表数据
const deviceList = ref([])
const loading = ref(false)

// 分页配置
const pagination = {
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50]
}

// 表格列定义
const columns = [
  {
    title: '设备编号',
    key: 'deviceId',
    width: 100,
    fixed: 'left'
  },
  {
    title: '设备名称',
    key: 'deviceName',
    width: 120
  },
  {
    title: '设备类型',
    key: 'deviceType',
    width: 100,
    render(row: any) {
      const typeMap: Record<string, string> = {
        'xiaoyou': '小悠盘',
        'xiaoxun': '小寻叉',
        'agv': 'AGV',
        'agf': 'AGF',
        'ctu': 'CTU',
        'autoLine': '自动线体',
        'dws': 'DWS'
      }
      return h(NTag, { size: 'small' }, { default: () => typeMap[row.deviceType] || row.deviceType })
    }
  },
  {
    title: '所属园区',
    key: 'park',
    width: 100
  },
  {
    title: '设备状态',
    key: 'status',
    width: 100,
    render(row: any) {
      const statusMap: Record<string, { text: string; type: string }> = {
        'online': { text: '在线', type: 'success' },
        'offline': { text: '离线', type: 'error' },
        'error': { text: '故障', type: 'warning' },
        'idle': { text: '空闲', type: 'info' },
        'working': { text: '执行任务', type: 'success' }
      }
      const status = statusMap[row.status] || { text: row.status, type: 'default' }
      return h(NTag, { type: status.type as any, size: 'small' }, { default: () => status.text })
    }
  },
  {
    title: '当前任务',
    key: 'currentTask',
    width: 120
  },
  {
    title: '今日任务数',
    key: 'todayTasks',
    width: 100
  },
  {
    title: '今日使用时长',
    key: 'todayDuration',
    width: 120,
    render(row: any) {
      return `${row.todayDuration}分钟`
    }
  },
  {
    title: '最近在线时间',
    key: 'lastOnlineTime',
    width: 150
  }
]

// 行样式
function rowClassName(row: any) {
  if (row.status === 'error') {
    return 'error-row'
  }
  if (row.status === 'offline') {
    return 'offline-row'
  }
  return ''
}

// 刷新地图
function refreshMap() {
  panoramicMapRef.value?.updateData([])
  message.success('地图数据已刷新')
}

// 刷新本周任务
function refreshWeekTasks() {
  weekTasksChartRef.value?.refresh()
  message.success('本周任务数据已刷新')
}

// 刷新本周时长
function refreshWeekDuration() {
  weekDurationChartRef.value?.refresh()
  message.success('本周时长数据已刷新')
}

// 刷新月度任务
function refreshMonthTasks() {
  monthTasksChartRef.value?.refresh()
  message.success('月度任务数据已刷新')
}

// 刷新月度时长
function refreshMonthDuration() {
  monthDurationChartRef.value?.refresh()
  message.success('月度时长数据已刷新')
}

// 加载设备列表
async function loadDeviceList() {
  loading.value = true

  try {
    // 模拟API调用
    setTimeout(() => {
      deviceList.value = generateMockDeviceList()
      loading.value = false
      message.success('设备列表加载成功')
    }, 500)
  } catch (error) {
    console.error('加载设备列表失败:', error)
    loading.value = false
    message.error('加载设备列表失败')
  }
}

// 生成模拟设备列表数据
function generateMockDeviceList() {
  const devices = []
  const types = ['xiaoyou', 'xiaoxun', 'agv', 'agf', 'ctu', 'autoLine', 'dws']
  const parks = ['上海奉贤', '广州东勤', '重庆园区']
  const statuses = ['online', 'offline', 'error', 'idle', 'working']
  const tasks = ['入库作业', '出库作业', '盘点作业', '搬运作业', '扫描作业', '']

  for (let i = 1; i <= 50; i++) {
    const type = types[Math.floor(Math.random() * types.length)]
    const status = statuses[Math.floor(Math.random() * statuses.length)]
    const park = parks[Math.floor(Math.random() * parks.length)]

    devices.push({
      deviceId: `${type.toUpperCase()}-${String(i).padStart(4, '0')}`,
      deviceName: `${type === 'xiaoyou' ? '小悠盘' : type === 'xiaoxun' ? '小寻叉' : type.toUpperCase()}-${i}`,
      deviceType: type,
      park: park,
      status: status,
      currentTask: status === 'working' ? tasks[Math.floor(Math.random() * (tasks.length - 1))] : '-',
      todayTasks: Math.floor(Math.random() * 50) + 10,
      todayDuration: Math.floor(Math.random() * 480) + 60,
      lastOnlineTime: new Date(Date.now() - Math.random() * 3600000).toLocaleString()
    })
  }

  return devices
}

// 组件挂载时加载数据
onMounted(() => {
  loadDeviceList()
})
</script>

<style lang="scss" scoped>
.equipment-dashboard {
  padding: 16px;
  background: #f5f7fa;
  min-height: 100vh;
}

.dashboard-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

  :deep(.n-card__content) {
    padding: 16px;
  }
}

:deep(.error-row) {
  background-color: rgba(244, 67, 54, 0.1) !important;
}

:deep(.offline-row) {
  background-color: rgba(158, 158, 158, 0.1) !important;
}
</style>