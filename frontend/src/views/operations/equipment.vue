<template>
  <div class="equipment-management">
    <n-grid :cols="4" :x-gap="16" :y-gap="16">
      <!-- 设备概览统计 -->
      <n-grid-item :span="4">
        <n-card title="设备概览">
          <n-grid :cols="5" :x-gap="16">
            <n-grid-item v-for="stat in equipmentStats" :key="stat.type">
              <n-statistic :label="stat.type" :value="stat.total">
                <template #suffix>
                  <n-tag :type="stat.online > 0 ? 'success' : 'error'" size="small">
                    {{ stat.online }}/{{ stat.total }}
                  </n-tag>
                </template>
              </n-statistic>
            </n-grid-item>
          </n-grid>
        </n-card>
      </n-grid-item>

      <!-- 设备状态分布 -->
      <n-grid-item :span="2">
        <n-card title="设备状态分布">
          <div ref="statusChart" class="chart-container"></div>
        </n-card>
      </n-grid-item>

      <!-- 今日任务运行情况 -->
      <n-grid-item :span="2">
        <n-card title="今日任务运行情况">
          <n-grid :cols="3" :x-gap="16">
            <n-grid-item>
              <n-statistic label="总任务数" :value="taskStats.total">
                <template #suffix>
                  <n-icon size="20" color="#2080f0">
                    <DocumentTextOutline />
                  </n-icon>
                </template>
              </n-statistic>
            </n-grid-item>
            <n-grid-item>
              <n-statistic label="完成任务" :value="taskStats.completed">
                <template #suffix>
                  <n-icon size="20" color="#18a058">
                    <CheckmarkCircleOutline />
                  </n-icon>
                </template>
              </n-statistic>
            </n-grid-item>
            <n-grid-item>
              <n-statistic label="完成率" :value="taskStats.completionRate" :precision="1">
                <template #suffix>%</template>
              </n-statistic>
            </n-grid-item>
          </n-grid>
        </n-card>
      </n-grid-item>

      <!-- 叉车设备列表 -->
      <n-grid-item :span="4">
        <n-card title="叉车设备列表">
          <template #header-extra>
            <n-space>
              <n-select
                v-model:value="warehouseFilter"
                :options="warehouseOptions"
                placeholder="选择库房"
                clearable
                style="width: 200px"
              />
              <n-button type="primary" @click="loadForkliftData">
                <template #icon>
                  <n-icon><RefreshOutline /></n-icon>
                </template>
                刷新
              </n-button>
            </n-space>
          </template>

          <n-data-table
            :columns="columns"
            :data="forkliftList"
            :pagination="pagination"
            :loading="loading"
            :row-class-name="rowClassName"
          />
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, h } from 'vue'
import { 
  NGrid, NGridItem, NCard, NStatistic, NTag, NSpace, 
  NButton, NIcon, NSelect, NDataTable, useMessage 
} from 'naive-ui'
import { 
  DocumentTextOutline, CheckmarkCircleOutline, RefreshOutline,
  HardwareChipOutline 
} from '@vicons/ionicons5'
import * as echarts from 'echarts'
import { equipmentApi } from '@/services/api'

const message = useMessage()

// 设备统计数据
const equipmentStats = ref([
  { type: 'AGV', total: 45, online: 42, offline: 3 },
  { type: 'AGF', total: 28, online: 25, offline: 3 },
  { type: 'CTU', total: 36, online: 33, offline: 3 },
  { type: '盘点机器', total: 15, online: 12, offline: 3 },
  { type: '智能叉车', total: 32, online: 28, offline: 4 },
])

// 任务统计数据
const taskStats = ref({
  total: 1250,
  completed: 1180,
  completionRate: 94.4,
})

// 叉车列表数据
const forkliftList = ref([])
const loading = ref(false)
const warehouseFilter = ref(null)
const statusChart = ref<HTMLElement | null>(null)

// 库房选项
const warehouseOptions = [
  { label: '北京中央仓库', value: 'WH001' },
  { label: '上海分拨中心', value: 'WH002' },
  { label: '广州南部中心', value: 'WH003' },
  { label: '成都西部中心', value: 'WH004' },
  { label: '武汉中部中心', value: 'WH005' },
]

// 分页配置
const pagination = {
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50],
}

// 表格列定义
const columns = [
  {
    title: '叉车编号',
    key: 'FltNo',
    width: 120,
    fixed: 'left',
  },
  {
    title: '叉车名称',
    key: 'FltName',
    width: 120,
  },
  {
    title: '所属库房',
    key: 'WarehouseCode',
    width: 120,
  },
  {
    title: '主控状态',
    key: 'OnlineStatusText',
    width: 100,
    render(row: any) {
      const type = row.OnlineStatusText === '在线' ? 'success' : 'error'
      return h(NTag, { type, size: 'small' }, { default: () => row.OnlineStatusText })
    },
  },
  {
    title: 'SLAM状态',
    key: 'SlamOnLineStatusText',
    width: 100,
    render(row: any) {
      const type = row.SlamOnLineStatusText === '在线' ? 'success' : 'error'
      return h(NTag, { type, size: 'small' }, { default: () => row.SlamOnLineStatusText })
    },
  },
  {
    title: '叉车状态',
    key: 'StatusText',
    width: 100,
    render(row: any) {
      const typeMap: Record<string, string> = {
        '空闲': 'info',
        '执行任务': 'success',
        '故障': 'error',
        '充电中': 'warning',
      }
      const type = typeMap[row.StatusText] || 'default'
      return h(NTag, { type, size: 'small' }, { default: () => row.StatusText })
    },
  },
  {
    title: '叉车型号',
    key: 'ModelText',
    width: 100,
  },
  {
    title: '负责人',
    key: 'Owners',
    width: 100,
  },
  {
    title: '最近在线时间',
    key: 'LastOnlineTime',
    width: 180,
  },
  {
    title: '异常描述',
    key: 'AbnormalDescription',
    width: 150,
    render(row: any) {
      if (row.AbnormalDescription) {
        return h(NTag, { type: 'error', size: 'small' }, { default: () => row.AbnormalDescription })
      }
      return h(NTag, { type: 'success', size: 'small' }, { default: () => '正常' })
    },
  },
]

// 行样式
function rowClassName(row: any) {
  if (row.AbnormalDescription) {
    return 'error-row'
  }
  return ''
}

// 初始化状态分布图表
function initStatusChart() {
  if (!statusChart.value) return
  
  const chart = echarts.init(statusChart.value)
  const option = {
    tooltip: {
      trigger: 'item',
    },
    legend: {
      orient: 'vertical',
      right: 'right',
    },
    series: [
      {
        name: '设备状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
        data: [
          { value: 140, name: '在线', itemStyle: { color: '#18a058' } },
          { value: 16, name: '离线', itemStyle: { color: '#d03050' } },
          { value: 8, name: '故障', itemStyle: { color: '#f0a020' } },
          { value: 22, name: '空闲', itemStyle: { color: '#2080f0' } },
        ],
      },
    ],
  }
  chart.setOption(option)
  
  // 响应窗口大小变化
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

// 加载叉车数据
async function loadForkliftData() {
  loading.value = true
  
  try {
    // 调用后端接口
    const response = await equipmentApi.getForklifts({ warehouseCode: warehouseFilter.value })
    
    if (response.success) {
      forkliftList.value = response.data || []
      message.success('数据加载成功')
    } else {
      // 如果接口调用失败，使用模拟数据
      console.warn('接口调用失败，使用模拟数据:', response.message)
      loadMockData()
    }
  } catch (error) {
    console.error('加载叉车数据失败:', error)
    // 发生错误时使用模拟数据
    loadMockData()
  } finally {
    loading.value = false
  }
}

// 加载模拟数据
function loadMockData() {
  // 模拟API调用延迟
  setTimeout(() => {
    forkliftList.value = [
      {
        Id: 113,
        FltNo: 'F001',
        FltName: 'F001',
        WarehouseCode: 'WH002010',
        OnlineStatusText: '离线',
        SlamOnLineStatusText: '离线',
        ScanOnLineStatusText: '离线',
        StatusText: '空闲',
        UpgradeText: '初始状态',
        Ip: '10.3.75.232',
        SlamIp: '10.125.129.88',
        ModelText: '林德',
        SlamModelText: '镭神1',
        ScanModelText: '默认',
        Owners: '管理员',
        EnabledText: '启用',
        Enabled: true,
        Remark: null,
        SlamVersion: '1.11.18',
        ShelfPushStatus: 0,
        ShelfPushStatusText: '初始状态',
        Model: 'LinDe',
        SlamModel: 'LeiShen1',
        ScanModel: 'Scan1',
        SlamLastPullTime: '2025-02-21 11:22:57',
        ScanLastReportTime: '2026-04-13 10:22:13',
        LastOnlineTime: '2025-09-23 16:23:34',
        PlateNumber: '辽A0F001',
        AbnormalId: '32',
        AbnormalDescription: '故障',
      },
      {
        Id: 114,
        FltNo: 'F002',
        FltName: 'F002',
        WarehouseCode: 'WH002010',
        OnlineStatusText: '在线',
        SlamOnLineStatusText: '在线',
        ScanOnLineStatusText: '在线',
        StatusText: '执行任务',
        UpgradeText: '初始状态',
        Ip: '10.3.75.233',
        SlamIp: '10.125.129.89',
        ModelText: '林德',
        SlamModelText: '镭神1',
        ScanModelText: '默认',
        Owners: '管理员',
        EnabledText: '启用',
        Enabled: true,
        Remark: null,
        SlamVersion: '1.11.18',
        ShelfPushStatus: 0,
        ShelfPushStatusText: '初始状态',
        Model: 'LinDe',
        SlamModel: 'LeiShen1',
        ScanModel: 'Scan1',
        SlamLastPullTime: '2025-02-21 11:22:57',
        ScanLastReportTime: '2026-04-13 10:22:13',
        LastOnlineTime: '2026-04-16 09:45:12',
        PlateNumber: '辽A0F002',
        AbnormalId: '',
        AbnormalDescription: '',
      },
      {
        Id: 115,
        FltNo: 'F003',
        FltName: 'F003',
        WarehouseCode: 'WH001001',
        OnlineStatusText: '在线',
        SlamOnLineStatusText: '在线',
        ScanOnLineStatusText: '在线',
        StatusText: '空闲',
        UpgradeText: '初始状态',
        Ip: '10.3.75.234',
        SlamIp: '10.125.129.90',
        ModelText: '林德',
        SlamModelText: '镭神1',
        ScanModelText: '默认',
        Owners: '操作员A',
        EnabledText: '启用',
        Enabled: true,
        Remark: '正常运行',
        SlamVersion: '1.11.18',
        ShelfPushStatus: 1,
        ShelfPushStatusText: '已下发',
        Model: 'LinDe',
        SlamModel: 'LeiShen1',
        ScanModel: 'Scan1',
        SlamLastPullTime: '2026-04-16 08:30:00',
        ScanLastReportTime: '2026-04-16 09:50:00',
        LastOnlineTime: '2026-04-16 09:50:00',
        PlateNumber: '京A0F003',
        AbnormalId: '',
        AbnormalDescription: '',
      },
    ]
    message.success('数据加载成功（模拟数据）')
  }, 500)
}

// 组件挂载时加载数据
onMounted(() => {
  loadForkliftData()
  initStatusChart()
})
</script>

<style lang="scss" scoped>
.equipment-management {
  padding: 16px;
}

.chart-container {
  height: 300px;
  width: 100%;
}

:deep(.error-row) {
  background-color: rgba(208, 48, 80, 0.1) !important;
}
</style>