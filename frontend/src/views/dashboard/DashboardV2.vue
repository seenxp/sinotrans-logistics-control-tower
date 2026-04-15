<template>
  <div class="dashboard">
    <!-- 顶部KPI卡片 -->
    <section class="kpi-section">
      <div class="kpi-grid">
        <div v-for="kpi in kpiData" :key="kpi.key" class="kpi-card card">
          <div class="kpi-header">
            <span class="kpi-icon" :style="{ background: kpi.iconBg }">
              {{ kpi.icon }}
            </span>
            <span class="badge" :class="kpi.trend === 'up' ? 'badge-success' : 'badge-error'">
              {{ kpi.trend === 'up' ? '↑' : '↓' }} {{ kpi.change }}%
            </span>
          </div>
          <div class="kpi-value text-heading-1">{{ kpi.value }}</div>
          <div class="kpi-label text-caption">{{ kpi.title }}</div>
          <div class="kpi-sparkline">
            <svg viewBox="0 0 100 30" preserveAspectRatio="none">
              <path
                :d="kpi.sparkline"
                fill="none"
                :stroke="kpi.trend === 'up' ? 'var(--success)' : 'var(--error)'"
                stroke-width="2"
              />
            </svg>
          </div>
        </div>
      </div>
    </section>

    <!-- 图表区域 -->
    <section class="charts-section">
      <div class="charts-grid">
        <!-- 订单趋势 -->
        <div class="card chart-card">
          <div class="card-header">
            <div>
              <h3 class="card-title">订单趋势</h3>
              <p class="card-subtitle">过去7天订单量与完成量</p>
            </div>
            <div class="chart-actions">
              <button class="btn btn-sm btn-ghost" :class="{ active: trendRange === '7d' }" @click="trendRange = '7d'">7天</button>
              <button class="btn btn-sm btn-ghost" :class="{ active: trendRange === '30d' }" @click="trendRange = '30d'">30天</button>
            </div>
          </div>
          <div ref="orderTrendChart" class="chart-container"></div>
        </div>

        <!-- 车辆分布 -->
        <div class="card chart-card">
          <div class="card-header">
            <div>
              <h3 class="card-title">车辆分布</h3>
              <p class="card-subtitle">按类型统计车辆数量</p>
            </div>
          </div>
          <div ref="vehicleDistChart" class="chart-container"></div>
        </div>
      </div>
    </section>

    <!-- 地图和告警 -->
    <section class="visualization-section">
      <div class="viz-grid">
        <!-- 物流网络地图 -->
        <div class="card map-card">
          <div class="card-header">
            <div>
              <h3 class="card-title">全国物流网络</h3>
              <p class="card-subtitle">实时车辆位置与运输线路</p>
            </div>
            <div class="flex gap-2">
              <span class="badge badge-lime">
                <span class="status-dot status-dot-success"></span>
                实时数据
              </span>
            </div>
          </div>
          <div class="map-container">
            <!-- 2D地图可视化 -->
            <div class="logistics-map">
              <svg viewBox="0 0 800 500" class="map-svg">
                <!-- 简化的中国地图轮廓 -->
                <path 
                  class="map-outline"
                  d="M200,150 Q250,100 350,120 Q450,80 550,130 Q620,150 650,200 Q680,280 650,350 Q600,420 500,450 Q400,480 300,450 Q200,420 180,350 Q150,280 170,200 Q180,160 200,150"
                  fill="none"
                  stroke="var(--border-subtle)"
                  stroke-width="2"
                />
                
                <!-- 运输线路 -->
                <g class="routes">
                  <path v-for="route in routes" :key="route.name"
                    :d="route.path"
                    fill="none"
                    stroke="var(--brand-purple)"
                    stroke-width="1.5"
                    stroke-dasharray="5,5"
                    opacity="0.6"
                  />
                  <!-- 流动粒子 -->
                  <circle v-for="(particle, idx) in particles" :key="idx"
                    :cx="particle.x"
                    :cy="particle.y"
                    r="4"
                    :fill="particle.color"
                    class="particle"
                  />
                </g>
                
                <!-- 城市节点 -->
                <g class="cities">
                  <g v-for="city in cities" :key="city.name"
                    :transform="`translate(${city.x}, ${city.y})`"
                    class="city-node"
                    @mouseenter="hoveredCity = city"
                    @mouseleave="hoveredCity = null"
                  >
                    <!-- 外圈脉冲 -->
                    <circle r="20" :fill="city.status === 'active' ? 'var(--success)' : 'var(--warning)'" opacity="0.1" class="pulse-ring" />
                    <circle r="14" :fill="city.status === 'active' ? 'var(--success)' : 'var(--warning)'" opacity="0.2" />
                    <!-- 核心点 -->
                    <circle r="6" :fill="city.status === 'active' ? 'var(--success)' : 'var(--warning)'" />
                    <!-- 城市名 -->
                    <text y="28" text-anchor="middle" fill="var(--text-secondary)" font-size="12" font-weight="500">{{ city.name }}</text>
                  </g>
                </g>
              </svg>
              
              <!-- 悬浮信息卡片 -->
              <div v-if="hoveredCity" class="city-tooltip card card-glass" :style="{ left: hoveredCity.x + 'px', top: hoveredCity.y + 'px' }">
                <div class="flex items-center gap-2" style="margin-bottom: 8px;">
                  <span class="status-dot" :class="hoveredCity.status === 'active' ? 'status-dot-success' : 'status-dot-warning'"></span>
                  <span class="text-body-md">{{ hoveredCity.name }}</span>
                </div>
                <div class="flex gap-4 text-small">
                  <span>车辆: {{ hoveredCity.vehicles }}</span>
                  <span>订单: {{ hoveredCity.orders }}</span>
                </div>
              </div>
            </div>
            
            <!-- 统计信息 -->
            <div class="map-stats">
              <div class="stat-item">
                <span class="stat-value">{{ totalVehicles }}</span>
                <span class="stat-label text-micro">在线车辆</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ cities.length }}</span>
                <span class="stat-label text-micro">活跃城市</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ routes.length }}</span>
                <span class="stat-label text-micro">运输线路</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 实时告警 -->
        <div class="card alert-card">
          <div class="card-header">
            <div>
              <h3 class="card-title">实时告警</h3>
              <p class="card-subtitle">需要关注的事件</p>
            </div>
            <span class="badge badge-error">{{ alerts.length }}</span>
          </div>
          <div class="alert-list">
            <div v-for="alert in alerts" :key="alert.id" class="alert-item" :class="'alert-' + alert.severity">
              <div class="alert-indicator">
                <span class="status-dot" :class="getStatusClass(alert.severity)"></span>
              </div>
              <div class="alert-content">
                <div class="alert-message text-body">{{ alert.message }}</div>
                <div class="alert-time text-small">{{ alert.timestamp }}</div>
              </div>
              <button class="btn btn-sm btn-ghost alert-action">处理</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 热门线路 -->
    <section class="routes-section">
      <div class="card">
        <div class="card-header">
          <div>
            <h3 class="card-title">热门线路 TOP 5</h3>
            <p class="card-subtitle">按订单量排序</p>
          </div>
          <button class="btn btn-ghost">查看全部</button>
        </div>
        <table class="table">
          <thead>
            <tr>
              <th>排名</th>
              <th>起点</th>
              <th>终点</th>
              <th>订单量</th>
              <th>平均时效</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="route in topRoutes" :key="route.rank">
              <td>
                <span class="route-rank" :class="'rank-' + route.rank">{{ route.rank }}</span>
              </td>
              <td class="text-body-md">{{ route.origin }}</td>
              <td class="text-body-md">{{ route.destination }}</td>
              <td class="text-mono">{{ route.volume.toLocaleString() }}</td>
              <td>{{ route.avgTime }}</td>
              <td>
                <span class="badge" :class="route.status === 'normal' ? 'badge-success' : 'badge-warning'">
                  {{ route.status === 'normal' ? '正常' : '延误' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components'
import * as echarts from 'echarts'

// 注册ECharts组件
use([CanvasRenderer, LineChart, PieChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

// 响应式数据
const trendRange = ref('7d')
const hoveredCity = ref<any>(null)

// KPI数据
const kpiData = ref([
  { 
    key: 'orders', 
    title: '今日订单', 
    value: '2,580', 
    change: 12.5, 
    trend: 'up',
    icon: '📦',
    iconBg: 'rgba(106, 95, 193, 0.2)',
    sparkline: 'M0,25 L10,20 L20,22 L30,15 L40,18 L50,12 L60,14 L70,8 L80,10 L90,5 L100,8'
  },
  { 
    key: 'vehicles', 
    title: '在线车辆', 
    value: '342', 
    change: 8.3, 
    trend: 'up',
    icon: '🚛',
    iconBg: 'rgba(140, 236, 127, 0.2)',
    sparkline: 'M0,20 L10,18 L20,22 L30,16 L40,14 L50,18 L60,12 L70,10 L80,14 L90,8 L100,6'
  },
  { 
    key: 'delivery', 
    title: '配送完成率', 
    value: '96.8%', 
    change: 2.1, 
    trend: 'up',
    icon: '✅',
    iconBg: 'rgba(194, 239, 78, 0.2)',
    sparkline: 'M0,15 L10,12 L20,14 L30,10 L40,8 L50,10 L60,6 L70,8 L80,5 L90,4 L100,3'
  },
  { 
    key: 'time', 
    title: '平均配送时间', 
    value: '2.4天', 
    change: 5.2, 
    trend: 'down',
    icon: '⏱️',
    iconBg: 'rgba(255, 178, 135, 0.2)',
    sparkline: 'M0,10 L10,12 L20,8 L30,14 L40,10 L50,16 L60,12 L70,18 L80,14 L90,20 L100,18'
  },
])

// 城市数据（带坐标）
const cities = ref([
  { name: '北京', x: 450, y: 150, vehicles: 45, orders: 1280, status: 'active' },
  { name: '上海', x: 520, y: 250, vehicles: 62, orders: 1850, status: 'active' },
  { name: '广州', x: 420, y: 380, vehicles: 38, orders: 980, status: 'active' },
  { name: '深圳', x: 440, y: 400, vehicles: 42, orders: 1120, status: 'busy' },
  { name: '成都', x: 300, y: 280, vehicles: 28, orders: 745, status: 'active' },
  { name: '武汉', x: 420, y: 280, vehicles: 30, orders: 820, status: 'active' },
  { name: '西安', x: 340, y: 200, vehicles: 18, orders: 420, status: 'active' },
  { name: '杭州', x: 530, y: 270, vehicles: 35, orders: 920, status: 'active' },
])

// 路线数据
const routes = computed(() => [
  { name: '京沪线', path: 'M450,150 Q485,200 520,250' },
  { name: '京广线', path: 'M450,150 Q435,265 420,380' },
  { name: '沪深线', path: 'M520,250 Q480,325 440,400' },
  { name: '成武线', path: 'M300,280 L420,280' },
  { name: '京西线', path: 'M450,150 Q395,175 340,200' },
])

// 流动粒子
const particles = ref([
  { x: 470, y: 180, color: 'var(--brand-purple)' },
  { x: 440, y: 220, color: 'var(--brand-purple)' },
  { x: 490, y: 300, color: 'var(--brand-purple)' },
  { x: 360, y: 280, color: 'var(--success)' },
  { x: 400, y: 170, color: 'var(--warning)' },
])

// 计算属性
const totalVehicles = computed(() => cities.value.reduce((sum, city) => sum + city.vehicles, 0))

// 告警数据
const alerts = ref([
  { id: 'ALT001', severity: 'high', message: '上海分拨中心容量即将饱和', timestamp: '5分钟前' },
  { id: 'ALT002', severity: 'medium', message: '北京至上海线路预计延迟2小时', timestamp: '10分钟前' },
  { id: 'ALT003', severity: 'low', message: '华南地区明日有雨，注意货物防护', timestamp: '30分钟前' },
  { id: 'ALT004', severity: 'medium', message: '车辆V003预计5分钟后到达', timestamp: '1小时前' },
])

// 热门线路
const topRoutes = ref([
  { rank: 1, origin: '上海', destination: '北京', volume: 1250, avgTime: '14.5小时', status: 'normal' },
  { rank: 2, origin: '广州', destination: '深圳', volume: 980, avgTime: '2.5小时', status: 'normal' },
  { rank: 3, origin: '北京', destination: '天津', volume: 856, avgTime: '2小时', status: 'delayed' },
  { rank: 4, origin: '成都', destination: '重庆', volume: 745, avgTime: '4小时', status: 'normal' },
  { rank: 5, origin: '杭州', destination: '上海', volume: 698, avgTime: '2小时', status: 'normal' },
])

// 图表引用
const orderTrendChart = ref<HTMLElement | null>(null)
const vehicleDistChart = ref<HTMLElement | null>(null)

let orderChart: echarts.ECharts | null = null
let vehicleChart: echarts.ECharts | null = null

// 状态类名
function getStatusClass(severity: string) {
  const classes: Record<string, string> = {
    'high': 'status-dot-error',
    'medium': 'status-dot-warning',
    'low': 'status-dot-success',
  }
  return classes[severity] || 'status-dot-success'
}

// 初始化订单趋势图
function initOrderTrendChart() {
  if (!orderTrendChart.value) return

  orderChart = echarts.init(orderTrendChart.value)
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#2a1f3d',
      borderColor: '#362d59',
      textStyle: { color: '#ffffff', fontFamily: 'Rubik' },
    },
    legend: {
      data: ['订单量', '完成量'],
      textStyle: { color: '#9ca3af', fontFamily: 'Rubik' },
      top: 0,
      right: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '40px',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      axisLine: { lineStyle: { color: '#362d59' } },
      axisLabel: { color: '#9ca3af', fontFamily: 'Rubik' },
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#362d59' } },
      axisLabel: { color: '#9ca3af', fontFamily: 'Rubik' },
    },
    series: [
      {
        name: '订单量',
        type: 'line',
        smooth: true,
        data: [1800, 2100, 1950, 2300, 2580, 2200, 1900],
        lineStyle: { color: '#6a5fc1', width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(106, 95, 193, 0.4)' },
            { offset: 1, color: 'rgba(106, 95, 193, 0)' },
          ]),
        },
        itemStyle: { color: '#6a5fc1' },
      },
      {
        name: '完成量',
        type: 'line',
        smooth: true,
        data: [1750, 2050, 1900, 2250, 2500, 2150, 1850],
        lineStyle: { color: '#8cec7f', width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(140, 236, 127, 0.4)' },
            { offset: 1, color: 'rgba(140, 236, 127, 0)' },
          ]),
        },
        itemStyle: { color: '#8cec7f' },
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
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: '#2a1f3d',
      borderColor: '#362d59',
      textStyle: { color: '#ffffff', fontFamily: 'Rubik' },
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'center',
      textStyle: { color: '#9ca3af', fontFamily: 'Rubik' },
    },
    series: [
      {
        name: '车辆类型',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#1f1633',
          borderWidth: 3,
        },
        label: {
          show: false,
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 600,
            color: '#ffffff',
            fontFamily: 'Rubik',
          },
        },
        labelLine: {
          show: false,
        },
        data: [
          { value: 245, name: '卡车', itemStyle: { color: '#6a5fc1' } },
          { value: 12, name: '船舶', itemStyle: { color: '#79628c' } },
          { value: 8, name: '飞机', itemStyle: { color: '#c2ef4e' } },
          { value: 15, name: '火车', itemStyle: { color: '#ffb287' } },
        ],
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

// 粒子动画
let particleInterval: number | null = null

function animateParticles() {
  particleInterval = window.setInterval(() => {
    particles.value = particles.value.map(p => ({
      ...p,
      x: p.x + (Math.random() - 0.5) * 2,
      y: p.y + (Math.random() - 0.5) * 2,
    }))
  }, 100)
}

onMounted(async () => {
  await nextTick()
  
  setTimeout(() => {
    initOrderTrendChart()
    initVehicleDistChart()
    animateParticles()
    window.addEventListener('resize', handleResize)
  }, 100)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (particleInterval) {
    clearInterval(particleInterval)
  }
  orderChart?.dispose()
  vehicleChart?.dispose()
})
</script>

<style scoped>
@import '@/styles/design-system.css';

.dashboard {
  padding: var(--space-6);
  max-width: 1200px;
  margin: 0 auto;
}

/* KPI卡片 */
.kpi-section {
  margin-bottom: var(--space-6);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

.kpi-card {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, var(--bg-surface) 0%, rgba(106, 95, 193, 0.1) 100%);
}

.kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}

.kpi-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  font-size: 22px;
}

.kpi-value {
  margin-bottom: var(--space-1);
  color: var(--text-primary);
}

.kpi-label {
  color: var(--text-tertiary);
}

.kpi-sparkline {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 100px;
  height: 40px;
  opacity: 0.4;
}

/* 图表区域 */
.charts-section {
  margin-bottom: var(--space-6);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
}

.chart-card {
  min-height: 350px;
}

.chart-container {
  height: 280px;
  width: 100%;
}

.chart-actions {
  display: flex;
  gap: var(--space-1);
}

.chart-actions .btn.active {
  background: var(--brand-purple);
  color: var(--text-primary);
}

/* 可视化区域 */
.visualization-section {
  margin-bottom: var(--space-6);
}

.viz-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-4);
}

.map-card {
  min-height: 450px;
}

.map-container {
  position: relative;
}

.logistics-map {
  position: relative;
  height: 350px;
  background: linear-gradient(135deg, rgba(106, 95, 193, 0.08) 0%, transparent 100%);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.map-svg {
  width: 100%;
  height: 100%;
}

.map-outline {
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: drawMap 3s ease-out forwards;
}

@keyframes drawMap {
  to {
    stroke-dashoffset: 0;
  }
}

.city-node {
  cursor: pointer;
  transition: transform var(--transition-fast);
}

.city-node:hover {
  transform: scale(1.1);
}

.pulse-ring {
  animation: pulseRing 2s infinite;
}

@keyframes pulseRing {
  0% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.5);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 0.3;
  }
}

.particle {
  animation: particleGlow 1.5s infinite alternate;
}

@keyframes particleGlow {
  from {
    opacity: 0.5;
    r: 3;
  }
  to {
    opacity: 1;
    r: 5;
  }
}

.city-tooltip {
  position: absolute;
  transform: translate(-50%, -120%);
  min-width: 150px;
  z-index: 100;
  pointer-events: none;
}

.map-stats {
  display: flex;
  justify-content: center;
  gap: var(--space-10);
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--border-subtle);
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 28px;
  font-weight: 600;
  color: var(--accent-lime);
}

.stat-label {
  color: var(--text-tertiary);
  margin-top: var(--space-1);
}

/* 告警卡片 */
.alert-card {
  max-height: 450px;
  display: flex;
  flex-direction: column;
}

.alert-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.alert-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3);
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-md);
  border-left: 3px solid transparent;
  transition: all var(--transition-fast);
}

.alert-item:hover {
  background: rgba(255, 255, 255, 0.06);
}

.alert-high {
  border-left-color: var(--error);
}

.alert-medium {
  border-left-color: var(--warning);
}

.alert-low {
  border-left-color: var(--success);
}

.alert-content {
  flex: 1;
}

.alert-message {
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.alert-time {
  color: var(--text-muted);
}

.alert-action {
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.alert-item:hover .alert-action {
  opacity: 1;
}

/* 线路表格 */
.routes-section .card {
  overflow: hidden;
}

.route-rank {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-secondary);
}

.rank-1 {
  background: linear-gradient(135deg, #c2ef4e, #8cec7f);
  color: var(--bg-primary);
}

.rank-2 {
  background: linear-gradient(135deg, #6a5fc1, #79628c);
  color: #ffffff;
}

.rank-3 {
  background: linear-gradient(135deg, #ffb287, #fa7faa);
  color: var(--bg-primary);
}

/* 响应式 */
@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .viz-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: var(--space-4);
  }
  
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
