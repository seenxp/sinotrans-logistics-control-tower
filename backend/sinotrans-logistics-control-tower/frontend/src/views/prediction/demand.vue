<template>
  <div class="demand-prediction">
    <n-card title="需求预测">
      <template #header-extra>
        <n-space>
          <n-button type="primary" @click="handlePredict">
            <template #icon>
              <n-icon><analytics-outline /></n-icon>
            </template>
            开始预测
          </n-button>
        </n-space>
      </template>

      <n-grid :cols="2" :x-gap="16" :y-gap="16">
        <n-grid-item>
          <n-form-item label="预测天数">
            <n-input-number v-model:value="horizon" :min="1" :max="30" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item>
          <n-form-item label="预测频率">
            <n-select v-model:value="frequency" :options="frequencyOptions" />
          </n-form-item>
        </n-grid-item>
      </n-grid>

      <n-divider />

      <n-card title="历史数据" size="small">
        <div ref="historyChart" class="chart-container"></div>
      </n-card>

      <n-divider />

      <n-card title="预测结果" size="small">
        <n-spin :show="loading">
          <div ref="predictionChart" class="chart-container"></div>
        </n-spin>
      </n-card>

      <n-divider />

      <n-card title="预测详情" size="small">
        <n-data-table
          :columns="columns"
          :data="predictionData"
          :bordered="false"
          :single-line="false"
        />
      </n-card>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
} from 'echarts/components'
import * as echarts from 'echarts'
import { AnalyticsOutline } from '@vicons/ionicons5'

use([CanvasRenderer, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, DataZoomComponent])

const horizon = ref(7)
const frequency = ref('daily')
const loading = ref(false)
const predictionData = ref<any[]>([])

const frequencyOptions = [
  { label: '每日', value: 'daily' },
  { label: '每周', value: 'weekly' },
  { label: '每月', value: 'monthly' },
]

const columns = [
  { title: '日期', key: 'date' },
  { title: '预测值', key: 'value' },
  { title: '下界 (10%)', key: 'lower' },
  { title: '上界 (90%)', key: 'upper' },
]

const historyChart = ref<HTMLElement | null>(null)
const predictionChart = ref<HTMLElement | null>(null)

let histChart: echarts.ECharts | null = null
let predChart: echarts.ECharts | null = null

// 历史数据
const historicalData = [1200, 1350, 1280, 1420, 1380, 1500, 1450, 1580, 1620, 1550, 1700, 1680, 1750, 1800]

function initHistoryChart() {
  if (!historyChart.value) return
  histChart = echarts.init(historyChart.value)
  
  const dates = []
  for (let i = historicalData.length - 1; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    dates.push(date.toLocaleDateString('zh-CN'))
  }
  
  histChart.setOption({
    tooltip: {
      trigger: 'axis',
    },
    xAxis: {
      type: 'category',
      data: dates,
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '需求量',
        type: 'line',
        data: historicalData,
        smooth: true,
        areaStyle: {
          opacity: 0.3,
        },
      },
    ],
  })
}

function initPredictionChart() {
  if (!predictionChart.value) return
  predChart = echarts.init(predictionChart.value)
  predChart.setOption({
    tooltip: {
      trigger: 'axis',
    },
    xAxis: {
      type: 'category',
      data: [],
    },
    yAxis: {
      type: 'value',
    },
    series: [],
  })
}

async function handlePredict() {
  loading.value = true
  
  // 模拟预测
  setTimeout(() => {
    const lastValue = historicalData[historicalData.length - 1]
    const predictions: any[] = []
    const predDates: string[] = []
    const predValues: number[] = []
    const lowerBounds: number[] = []
    const upperBounds: number[] = []
    
    for (let i = 1; i <= horizon.value; i++) {
      const date = new Date()
      date.setDate(date.getDate() + i)
      predDates.push(date.toLocaleDateString('zh-CN'))
      
      const trend = 1 + (Math.random() * 0.1 - 0.03)
      const value = Math.round(lastValue * Math.pow(trend, i))
      const lower = Math.round(value * 0.9)
      const upper = Math.round(value * 1.1)
      
      predValues.push(value)
      lowerBounds.push(lower)
      upperBounds.push(upper)
      
      predictions.push({
        date: date.toLocaleDateString('zh-CN'),
        value,
        lower,
        upper,
      })
    }
    
    predictionData.value = predictions
    
    // 更新图表
    const allDates = [
      ...Array(historicalData.length).fill(0).map((_, i) => {
        const date = new Date()
        date.setDate(date.getDate() - historicalData.length + i + 1)
        return date.toLocaleDateString('zh-CN')
      }),
      ...predDates,
    ]
    
    const allValues = [
      ...historicalData,
      ...predValues,
    ]
    
    predChart?.setOption({
      tooltip: {
        trigger: 'axis',
      },
      legend: {
        data: ['历史数据', '预测值', '置信区间'],
      },
      xAxis: {
        type: 'category',
        data: allDates,
      },
      yAxis: {
        type: 'value',
      },
      dataZoom: [
        {
          type: 'inside',
          start: 0,
          end: 100,
        },
      ],
      series: [
        {
          name: '历史数据',
          type: 'line',
          data: allValues.map((v, i) => i < historicalData.length ? v : null),
          smooth: true,
        },
        {
          name: '预测值',
          type: 'line',
          data: allValues.map((v, i) => i >= historicalData.length ? v : null),
          smooth: true,
          lineStyle: {
            type: 'dashed',
          },
        },
        {
          name: '置信区间',
          type: 'line',
          data: upperBounds,
          smooth: true,
          lineStyle: {
            opacity: 0,
          },
          areaStyle: {
            color: 'rgba(24, 144, 255, 0.2)',
          },
          stack: 'confidence',
        },
      ],
    })
    
    loading.value = false
  }, 1500)
}

function handleResize() {
  histChart?.resize()
  predChart?.resize()
}

onMounted(() => {
  initHistoryChart()
  initPredictionChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  histChart?.dispose()
  predChart?.dispose()
})
</script>

<style lang="scss" scoped>
.demand-prediction {
  padding: 24px;
}

.chart-container {
  height: 300px;
}
</style>
