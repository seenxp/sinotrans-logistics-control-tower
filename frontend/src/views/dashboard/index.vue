<template>
  <div class="dashboard-container">
    <!-- KPI卡片 -->
    <section class="kpi-section">
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <n-grid-item v-for="kpi in kpiData" :key="kpi.key">
          <n-card class="kpi-card">
            <div class="kpi-content">
              <div class="kpi-info">
                <span class="kpi-title">{{ kpi.title }}</span>
                <span class="kpi-value text-number">{{ kpi.value }}</span>
                <span class="kpi-unit" v-if="kpi.unit">{{ kpi.unit }}</span>
              </div>
              <div class="kpi-trend" :class="kpi.trend">
                <n-icon v-if="kpi.trend === 'up'"><arrow-up-outline /></n-icon>
                <n-icon v-else><arrow-down-outline /></n-icon>
                <span>{{ kpi.change }}%</span>
              </div>
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>
    </section>

    <!-- 图表区域 -->
    <section class="chart-section">
      <n-grid :cols="2" :x-gap="16" :y-gap="16">
        <!-- 订单趋势 -->
        <n-grid-item>
          <n-card title="订单趋势" class="chart-card">
            <div ref="orderTrendChart" class="chart-container"></div>
          </n-card>
        </n-grid-item>

        <!-- 车辆分布 -->
        <n-grid-item>
          <n-card title="车辆分布" class="chart-card">
            <div ref="vehicleDistChart" class="chart-container"></div>
          </n-card>
        </n-grid-item>
      </n-grid>
    </section>

    <!-- 3D地球和告警 -->
    <section class="globe-alert-section">
      <n-grid :cols="3" :x-gap="16" :y-gap="16">
        <!-- 3D地球可视化 -->
        <n-grid-item :span="2">
          <n-card title="3D物流网络可视化" class="globe-card">
            <template #header-extra>
              <n-space>
                <n-tag type="info" size="small">Three.js</n-tag>
                <n-tag type="success" size="small">实时数据</n-tag>
              </n-space>
            </template>
            <GlobeVisualization />
          </n-card>
        </n-grid-item>

        <!-- 实时告警 -->
        <n-grid-item>
          <n-card title="实时告警" class="alert-card">
            <template #header-extra>
              <n-badge :value="alerts.length" :max="99" />
            </template>
            <n-list hoverable clickable>
              <n-list-item v-for="alert in alerts" :key="alert.id">
                <template #prefix>
                  <n-tag :type="getAlertType(alert.severity)" size="small">
                    {{ alert.severity }}
                  </n-tag>
                </template>
                <n-thing :title="alert.message" :description="alert.timestamp" />
              </n-list-item>
            </n-list>
          </n-card>
        </n-grid-item>
      </n-grid>
    </section>

    <!-- 热门线路 -->
    <section class="route-section">
      <n-card title="热门线路 TOP 5">
        <template #header-extra>
          <n-button text type="primary">查看全部</n-button>
        </template>
        <n-data-table
          :columns="routeColumns"
          :data="topRoutes"
          :bordered="false"
          :single-line="false"
        />
      </n-card>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components'
import * as echarts from 'echarts'
import {
  ArrowUpOutline,
  ArrowDownOutline,
  GlobeOutline,
} from '@vicons/ionicons5'
import GlobeVisualization from '@/components/GlobeVisualization.vue'

// 注册ECharts组件
use([CanvasRenderer, LineChart, BarChart, PieChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

// KPI数据
const kpiData = ref([
  { key: 'orders', title: '今日订单', value: '2,580', change: 12.5, trend: 'up' },
  { key: 'vehicles', title: '在线车辆', value: '342', change: 8.3, trend: 'up' },
  { key: 'delivery', title: '配送完成率', value: '96.8', unit: '%', change: 2.1, trend: 'up' },
  { key: 'time', title: '平均配送时间', value: '2.4', unit: '天', change: -5.2, trend: 'down' },
])

// 告警数据
const alerts = ref([
  { id: 'ALT001', severity: '中等', message: '北京至上海线路预计延迟2小时', timestamp: '10分钟前' },
  { id: 'ALT002', severity: '高', message: '上海分拨中心容量即将饱和', timestamp: '1小时前' },
  { id: 'ALT003', severity: '低', message: '华南地区明日有雨，注意货物防护', timestamp: '2小时前' },
  { id: 'ALT004', severity: '中等', message: '车辆V003预计5分钟后到达', timestamp: '5分钟前' },
])

// 热门线路
const topRoutes = ref([
  { rank: 1, origin: '上海', destination: '北京', volume: 1250, avgTime: '14.5小时' },
  { rank: 2, origin: '广州', destination: '深圳', volume: 980, avgTime: '2.5小时' },
  { rank: 3, origin: '北京', destination: '天津', volume: 856, avgTime: '2小时' },
  { rank: 4, origin: '成都', destination: '重庆', volume: 745, avgTime: '4小时' },
  { rank: 5, origin: '杭州', destination: '上海', volume: 698, avgTime: '2小时' },
])

const routeColumns = [
  { title: '排名', key: 'rank', width: 80 },
  { title: '起点', key: 'origin' },
  { title: '终点', key: 'destination' },
  { title: '订单量', key: 'volume', sorter: (a: any, b: any) => a.volume - b.volume },
  { title: '平均时效', key: 'avgTime' },
]

// 图表引用
const orderTrendChart = ref<HTMLElement | null>(null)
const vehicleDistChart = ref<HTMLElement | null>(null)

let orderChart: echarts.ECharts | null = null
let vehicleChart: echarts.ECharts | null = null

// 获取告警类型
function getAlertType(severity: string) {
  const types: Record<string, 'error' | 'warning' | 'info'> = {
    '高': 'error',
    '中等': 'warning',
    '低': 'info',
  }
  return types[severity] || 'info'
}

// 初始化订单趋势图
function initOrderTrendChart() {
  if (!orderTrendChart.value) return

  orderChart = echarts.init(orderTrendChart.value)
  const option = {
    tooltip: {
      trigger: 'axis',
    },
    legend: {
      data: ['订单量', '完成量'],
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '订单量',
        type: 'line',
        smooth: true,
        data: [1800, 2100, 1950, 2300, 2580, 2200, 1900],
        areaStyle: {
          opacity: 0.3,
        },
      },
      {
        name: '完成量',
        type: 'line',
        smooth: true,
        data: [1750, 2050, 1900, 2250, 2500, 2150, 1850],
        areaStyle: {
          opacity: 0.3,
        },
      },
    ],
  }
  orderChart.setOption(option)
}

// 初始化车辆分布图
function initVehicleDistChart() {
  if (!vehicleDistChart.value) return

  vehicleChart = echarts.init(vehicleDistChart.value)
  const option = {
    tooltip: {
      trigger: 'item',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: '车辆类型',
        type: 'pie',
        radius: '70%',
        data: [
          { value: 245, name: '卡车' },
          { value: 12, name: '船舶' },
          { value: 8, name: '飞机' },
          { value: 15, name: '火车' },
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  }
  vehicleChart.setOption(option)
}

// 窗口大小变化时重绘图表
function handleResize() {
  orderChart?.resize()
  vehicleChart?.resize()
}

onMounted(async () => {
  await nextTick()
  
  setTimeout(() => {
    initOrderTrendChart()
    initVehicleDistChart()
    window.addEventListener('resize', handleResize)
  }, 100)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  orderChart?.dispose()
  vehicleChart?.dispose()
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  width: 100%;
}

.kpi-section {
  margin-bottom: 24px;
}

.kpi-card {
  .kpi-content {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .kpi-info {
      .kpi-title {
        display: block;
        color: var(--text-secondary);
        font-size: 14px;
        margin-bottom: 8px;
      }

      .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: var(--text-primary);
      }

      .kpi-unit {
        font-size: 14px;
        color: var(--text-secondary);
        margin-left: 4px;
      }
    }

    .kpi-trend {
      display: flex;
      align-items: center;
      font-size: 14px;
      padding: 4px 8px;
      border-radius: 4px;

      &.up {
        color: #52c41a;
        background: rgba(82, 196, 26, 0.1);
      }

      &.down {
        color: #f5222d;
        background: rgba(245, 34, 45, 0.1);
      }
    }
  }
}

.chart-section {
  margin-bottom: 24px;
}

.chart-card {
  .chart-container {
    height: 300px;
  }
}

.globe-alert-section {
  margin-bottom: 24px;
}

.globe-card {
  :deep(.n-card__content) {
    padding: 0;
    height: 500px;
  }
}

.alert-card {
  :deep(.n-list) {
    max-height: 500px;
    overflow-y: auto;
  }
}

.route-section {
  margin-top: 24px;
}
</style>