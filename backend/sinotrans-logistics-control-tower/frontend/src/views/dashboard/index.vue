<template>
  <div class="dashboard-container">
    <!-- 顶部导航 -->
    <header class="dashboard-header">
      <div class="header-left">
        <h1 class="logo">
          <span class="logo-icon">🌐</span>
          <span class="logo-text">外运物流控制塔</span>
        </h1>
      </div>
      <div class="header-center">
        <n-breadcrumb>
          <n-breadcrumb-item>控制台</n-breadcrumb-item>
          <n-breadcrumb-item>概览</n-breadcrumb-item>
        </n-breadcrumb>
      </div>
      <div class="header-right">
        <n-space>
          <n-button quaternary circle @click="refreshData">
            <template #icon>
              <n-icon><refresh-outline /></n-icon>
            </template>
          </n-button>
          <n-button quaternary circle @click="toggleFullscreen">
            <template #icon>
              <n-icon><scan-outline /></n-icon>
            </template>
          </n-button>
          <n-dropdown :options="userOptions" @select="handleUserAction">
            <n-avatar round size="small">
              <n-icon><person-outline /></n-icon>
            </n-avatar>
          </n-dropdown>
        </n-space>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="dashboard-main">
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

      <!-- 地图和告警 -->
      <section class="map-alert-section">
        <n-grid :cols="3" :x-gap="16" :y-gap="16">
          <!-- 物流地图 -->
          <n-grid-item :span="2">
            <n-card title="物流网络地图" class="map-card">
              <div ref="mapContainer" class="map-container">
                <div class="map-placeholder">
                  <n-icon size="48" color="#1890ff"><globe-outline /></n-icon>
                  <p>3D物流网络可视化</p>
                  <p class="text-secondary">集成Cesium.js地球可视化</p>
                </div>
              </div>
            </n-card>
          </n-grid-item>

          <!-- 实时告警 -->
          <n-grid-item>
            <n-card title="实时告警" class="alert-card">
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
          <n-data-table
            :columns="routeColumns"
            :data="topRoutes"
            :bordered="false"
            :single-line="false"
          />
        </n-card>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, h } from 'vue'
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
  RefreshOutline,
  ScanOutline,
  PersonOutline,
  ArrowUpOutline,
  ArrowDownOutline,
  GlobeOutline,
} from '@vicons/ionicons5'

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

const userOptions = [
  { label: '个人中心', key: 'profile' },
  { label: '系统设置', key: 'settings' },
  { type: 'divider', key: 'd1' },
  { label: '退出登录', key: 'logout' },
]

// 图表引用
const orderTrendChart = ref<HTMLElement | null>(null)
const vehicleDistChart = ref<HTMLElement | null>(null)
const mapContainer = ref<HTMLElement | null>(null)

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

// 刷新数据
function refreshData() {
  // 重新加载数据
  initOrderTrendChart()
  initVehicleDistChart()
}

// 切换全屏
function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

// 用户操作
function handleUserAction(key: string) {
  console.log('User action:', key)
}

// 窗口大小变化时重绘图表
function handleResize() {
  orderChart?.resize()
  vehicleChart?.resize()
}

onMounted(() => {
  initOrderTrendChart()
  initVehicleDistChart()
  window.addEventListener('resize', handleResize)
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
  height: 100vh;
  background: var(--bg-layout);
  overflow: auto;
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 24px;
  background: var(--bg-component);
  box-shadow: var(--box-shadow-sm);

  .header-left {
    .logo {
      display: flex;
      align-items: center;
      font-size: 20px;
      font-weight: bold;

      .logo-icon {
        margin-right: 8px;
        font-size: 24px;
      }

      .logo-text {
        background: linear-gradient(135deg, #1890ff, #722ed1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }
    }
  }
}

.dashboard-main {
  padding: 24px;
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

.map-card {
  .map-container {
    height: 400px;
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;

    .map-placeholder {
      text-align: center;
      color: #fff;

      p {
        margin-top: 16px;
        font-size: 16px;
      }

      .text-secondary {
        font-size: 14px;
        opacity: 0.7;
      }
    }
  }
}

.alert-card {
  :deep(.n-list) {
    max-height: 400px;
    overflow-y: auto;
  }
}

.route-section {
  margin-top: 24px;
}
</style>
