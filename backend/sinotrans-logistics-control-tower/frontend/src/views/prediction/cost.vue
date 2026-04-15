<template>
  <div class="prediction-page">
    <n-card title="成本预测">
      <n-alert type="info" title="功能说明">
        基于TimesFM模型，预测未来物流成本趋势，帮助成本控制。
      </n-alert>
      
      <n-divider />
      
      <n-grid :cols="4" :x-gap="16">
        <n-grid-item>
          <n-card>
            <n-statistic label="本月成本" :value="125800" prefix="¥" />
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card>
            <n-statistic label="预测下月" :value="132500" prefix="¥" />
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card>
            <n-statistic label="环比增长" :value="5.3" suffix="%" />
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card>
            <n-statistic label="成本控制" :value="85" suffix="分" />
          </n-card>
        </n-grid-item>
      </n-grid>
      
      <n-divider />
      
      <div ref="chartRef" class="chart-container"></div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import * as echarts from 'echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent])

const chartRef = ref<HTMLElement | null>(null)

onMounted(() => {
  if (!chartRef.value) return
  const chart = echarts.init(chartRef.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['燃油成本', '人工成本', '维护成本', '总成本'] },
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'] },
    yAxis: { type: 'value', axisLabel: { formatter: '¥{value}' } },
    series: [
      { name: '燃油成本', type: 'line', data: [45000, 48000, 46000, 50000, 52000, 49000, 51000, 53000, 50000, 48000, 47000, 46000], smooth: true },
      { name: '人工成本', type: 'line', data: [35000, 35000, 36000, 36000, 37000, 37000, 38000, 38000, 39000, 39000, 40000, 40000], smooth: true },
      { name: '维护成本', type: 'line', data: [15000, 18000, 12000, 20000, 16000, 14000, 19000, 17000, 13000, 15000, 16000, 18000], smooth: true },
      { name: '总成本', type: 'line', data: [95000, 101000, 94000, 106000, 105000, 100000, 108000, 108000, 102000, 102000, 103000, 104000], smooth: true, lineStyle: { width: 3 } },
    ],
  })
  window.addEventListener('resize', () => chart.resize())
})
</script>

<style scoped>
.prediction-page { padding: 24px; }
.chart-container { height: 400px; }
</style>
