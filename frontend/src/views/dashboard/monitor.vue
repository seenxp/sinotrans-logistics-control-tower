<template>
  <div class="monitor-container">
    <n-grid :cols="24" :x-gap="16" :y-gap="16">
      <!-- 实时统计 -->
      <n-grid-item :span="6">
        <n-card title="实时订单">
          <div class="stat-value text-number">{{ realtimeData.orders }}</div>
          <div class="stat-label">今日新增订单</div>
        </n-card>
      </n-grid-item>
      <n-grid-item :span="6">
        <n-card title="在途车辆">
          <div class="stat-value text-number">{{ realtimeData.vehicles }}</div>
          <div class="stat-label">当前在线车辆</div>
        </n-card>
      </n-grid-item>
      <n-grid-item :span="6">
        <n-card title="待处理">
          <div class="stat-value text-number warning">{{ realtimeData.pending }}</div>
          <div class="stat-label">等待处理订单</div>
        </n-card>
      </n-grid-item>
      <n-grid-item :span="6">
        <n-card title="今日完成">
          <div class="stat-value text-number success">{{ realtimeData.completed }}</div>
          <div class="stat-label">已完成订单</div>
        </n-card>
      </n-grid-item>

      <!-- 3D地球 -->
      <n-grid-item :span="16">
        <n-card title="全球物流网络">
          <div ref="globeContainer" class="globe-container">
            <div class="globe-placeholder">
              <n-icon size="64" color="#1890ff"><globe-outline /></n-icon>
              <p>3D地球可视化</p>
              <p class="hint">集成Three.js + Cesium.js</p>
            </div>
          </div>
        </n-card>
      </n-grid-item>

      <!-- 实时告警 -->
      <n-grid-item :span="8">
        <n-card title="实时告警">
          <n-scrollbar style="max-height: 400px">
            <n-timeline>
              <n-timeline-item
                v-for="alert in alerts"
                :key="alert.id"
                :type="getTimelineType(alert.severity)"
                :title="alert.message"
                :time="alert.time"
              />
            </n-timeline>
          </n-scrollbar>
        </n-card>
      </n-grid-item>

      <!-- 运力利用率 -->
      <n-grid-item :span="8">
        <n-card title="运力利用率">
          <div ref="utilizationChart" class="chart-container"></div>
        </n-card>
      </n-grid-item>

      <!-- 区域订单分布 -->
      <n-grid-item :span="8">
        <n-card title="区域订单分布">
          <div ref="regionChart" class="chart-container"></div>
        </n-card>
      </n-grid-item>

      <!-- 实时订单流 -->
      <n-grid-item :span="8">
        <n-card title="实时订单流">
          <div ref="flowChart" class="chart-container"></div>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, GaugeChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from 'echarts/components'
import * as echarts from 'echarts'
import { GlobeOutline } from '@vicons/ionicons5'

use([CanvasRenderer, LineChart, GaugeChart, PieChart, TitleComponent, TooltipComponent, LegendComponent])

// 实时数据
const realtimeData = ref({
  orders: 2580,
  vehicles: 342,
  pending: 56,
  completed: 2456,
})

// 告警数据
const alerts = ref([
  { id: 1, severity: 'high', message: '车辆V001异常停车', time: '2分钟前' },
  { id: 2, severity: 'medium', message: '上海仓库容量告警', time: '15分钟前' },
  { id: 3, severity: 'low', message: '广州地区天气预警', time: '30分钟前' },
  { id: 4, severity: 'medium', message: '订单ORD001配送延迟', time: '45分钟前' },
  { id: 5, severity: 'high', message: '车辆V003故障预警', time: '1小时前' },
])

// 图表引用
const globeContainer = ref<HTMLElement | null>(null)
const utilizationChart = ref<HTMLElement | null>(null)
const regionChart = ref<HTMLElement | null>(null)
const flowChart = ref<HTMLElement | null>(null)

let utilChart: echarts.ECharts | null = null
let regChart: echarts.ECharts | null = null
let fChart: echarts.ECharts | null = null

function getTimelineType(severity: string) {
  const types: Record<string, 'error' | 'warning' | 'info' | 'success'> = {
    high: 'error',
    medium: 'warning',
    low: 'info',
  }
  return types[severity] || 'info'
}

function initUtilizationChart() {
  if (!utilizationChart.value) return
  utilChart = echarts.init(utilizationChart.value)
  utilChart.setOption({
    series: [
      {
        type: 'gauge',
        progress: {
          show: true,
          width: 18,
        },
        axisLine: {
          lineStyle: {
            width: 18,
          },
        },
        axisTick: {
          show: false,
        },
        splitLine: {
          length: 15,
          lineStyle: {
            width: 2,
            color: '#999',
          },
        },
        pointer: {
          icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
          length: '12%',
          width: 20,
          offsetCenter: [0, '-60%'],
          itemStyle: {
            color: 'auto',
          },
        },
        axisLabel: {
          color: 'inherit',
          distance: 25,
          fontSize: 14,
        },
        detail: {
          valueAnimation: true,
          formatter: '{value}%',
          color: 'inherit',
          fontSize: 24,
        },
        data: [{ value: 78, name: '运力利用率' }],
      },
    ],
  })
}

function initRegionChart() {
  if (!regionChart.value) return
  regChart = echarts.init(regionChart.value)
  regChart.setOption({
    tooltip: {
      trigger: 'item',
    },
    series: [
      {
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
          { value: 1048, name: '华东' },
          { value: 735, name: '华南' },
          { value: 580, name: '华北' },
          { value: 484, name: '西南' },
          { value: 300, name: '其他' },
        ],
      },
    ],
  })
}

function initFlowChart() {
  if (!flowChart.value) return
  fChart = echarts.init(flowChart.value)
  
  const data = []
  for (let i = 0; i < 50; i++) {
    data.push(Math.random() * 100 + 50)
  }
  
  fChart.setOption({
    xAxis: {
      type: 'category',
      show: false,
    },
    yAxis: {
      type: 'value',
      show: false,
    },
    series: [
      {
        data: data,
        type: 'line',
        smooth: true,
        symbol: 'none',
        areaStyle: {
          opacity: 0.5,
        },
      },
    ],
  })
}

function handleResize() {
  utilChart?.resize()
  regChart?.resize()
  fChart?.resize()
}

// 实时更新数据
let updateTimer: number | null = null

function updateRealtimeData() {
  realtimeData.value.orders += Math.floor(Math.random() * 10)
  realtimeData.value.vehicles = 340 + Math.floor(Math.random() * 20)
  realtimeData.value.pending = 50 + Math.floor(Math.random() * 20)
  realtimeData.value.completed += Math.floor(Math.random() * 5)
}

onMounted(() => {
  initUtilizationChart()
  initRegionChart()
  initFlowChart()
  window.addEventListener('resize', handleResize)
  
  // 定时更新数据
  updateTimer = window.setInterval(updateRealtimeData, 3000)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  utilChart?.dispose()
  regChart?.dispose()
  fChart?.dispose()
  
  if (updateTimer) {
    clearInterval(updateTimer)
  }
})
</script>

<style lang="scss" scoped>
.monitor-container {
  padding: 24px;
  background: var(--bg-layout);
  min-height: 100vh;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: var(--primary-color);
  margin: 16px 0 8px;
  
  &.warning {
    color: var(--warning-color);
  }
  
  &.success {
    color: var(--success-color);
  }
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.globe-container {
  height: 400px;
  background: linear-gradient(135deg, #0c1445, #1a237e);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .globe-placeholder {
    text-align: center;
    color: #fff;
    
    p {
      margin-top: 16px;
      font-size: 18px;
    }
    
    .hint {
      font-size: 14px;
      opacity: 0.7;
    }
  }
}

.chart-container {
  height: 250px;
}
</style>
