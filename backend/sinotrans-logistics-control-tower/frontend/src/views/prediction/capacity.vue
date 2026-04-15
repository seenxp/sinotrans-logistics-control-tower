<template>
  <div class="prediction-page">
    <n-card title="运力预测">
      <n-alert type="info" title="功能说明">
        基于TimesFM模型，预测未来运力需求，帮助优化资源配置。
      </n-alert>
      
      <n-divider />
      
      <n-grid :cols="2" :x-gap="16">
        <n-grid-item>
          <n-card title="当前运力">
            <n-statistic label="总运力" :value="280" suffix="辆" />
            <n-progress type="multiple-circle" :percentage="[{ percentage: 78, color: '#1890ff' }]" :stroke-width="8" style="margin-top: 16px" />
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card title="预测需求">
            <n-statistic label="未来7天需求" :value="320" suffix="辆" />
            <n-tag type="warning" style="margin-top: 16px">缺口: 40辆</n-tag>
          </n-card>
        </n-grid-item>
      </n-grid>
      
      <n-divider />
      
      <div ref="chartRef" class="chart-container"></div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import * as echarts from 'echarts'

use([CanvasRenderer, BarChart, LineChart, GridComponent, TooltipComponent, LegendComponent])

const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

onMounted(() => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['当前运力', '预测需求'] },
    xAxis: { type: 'category', data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'] },
    yAxis: { type: 'value' },
    series: [
      { name: '当前运力', type: 'bar', data: [280, 280, 280, 280, 280, 280, 280], itemStyle: { color: '#1890ff' } },
      { name: '预测需求', type: 'line', data: [300, 310, 320, 290, 350, 330, 310], itemStyle: { color: '#faad14' }, smooth: true },
    ],
  })
  window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
  chart?.dispose()
})
</script>

<style scoped>
.prediction-page { padding: 24px; }
.chart-container { height: 400px; }
</style>
