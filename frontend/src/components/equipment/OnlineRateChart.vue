<template>
  <div class="online-rate-chart">
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 设备在线率数据（模拟数据）
const deviceData = [
  { name: '小悠盘', total: 45, online: 42 },
  { name: '小寻叉', total: 38, online: 35 },
  { name: 'AGV', total: 52, online: 48 },
  { name: 'AGF', total: 28, online: 25 },
  { name: 'CTU', total: 36, online: 33 },
  { name: '自动线体', total: 15, online: 14 },
  { name: 'DWS', total: 12, online: 11 }
]

onMounted(() => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)

  const option = {
    title: {
      text: '各类设备在线率',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: function(params: any) {
        const data = params.data
        return `
          <strong>${data.name}</strong><br/>
          设备总数: ${data.total}<br/>
          在线设备: ${data.online}<br/>
          在线率: ${data.rate}%
        `
      }
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 'right',
      top: 'middle'
    },
    series: [
      {
        name: '设备在线率',
        type: 'pie',
        radius: ['30%', '55%'],
        center: ['40%', '55%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 6,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{d}%',
          fontSize: 11
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold'
          }
        },
        data: deviceData.map(item => ({
          name: item.name,
          value: item.online,
          total: item.total,
          online: item.online,
          rate: ((item.online / item.total) * 100).toFixed(1),
          itemStyle: {
            color: getColorByRate(item.online / item.total)
          }
        }))
      }
    ]
  }

  chart.setOption(option)

  window.addEventListener('resize', handleResize)
})

function getColorByRate(rate: number) {
  if (rate >= 0.9) return '#00C853'
  if (rate >= 0.8) return '#2196F3'
  if (rate >= 0.7) return '#FF9800'
  return '#F44336'
}

function handleResize() {
  chart?.resize()
}

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})

defineExpose({
  updateData: (newData: any[]) => {
    if (chart) {
      chart.setOption({
        series: [{
          data: newData.map(item => ({
            name: item.name,
            value: item.online,
            total: item.total,
            online: item.online,
            rate: ((item.online / item.total) * 100).toFixed(1),
            itemStyle: {
              color: getColorByRate(item.online / item.total)
            }
          }))
        }]
      })
    }
  }
})
</script>

<style scoped>
.online-rate-chart {
  width: 100%;
}

.chart-container {
  height: 350px;
  width: 100%;
}
</style>