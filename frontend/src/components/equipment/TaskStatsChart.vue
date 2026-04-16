<template>
  <div class="task-stats-chart">
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 任务统计数据（模拟数据）
const taskData = [
  { name: '小悠盘', total: 125, completed: 118, rate: 94.4 },
  { name: '小寻叉', total: 98, completed: 92, rate: 93.9 },
  { name: 'AGV', total: 156, completed: 148, rate: 94.9 },
  { name: 'AGF', total: 78, completed: 72, rate: 92.3 },
  { name: 'CTU', total: 89, completed: 85, rate: 95.5 },
  { name: '自动线体', total: 45, completed: 43, rate: 95.6 },
  { name: 'DWS', total: 32, completed: 30, rate: 93.8 }
]

onMounted(() => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)

  const option = {
    title: {
      text: '各类设备今日任务完成情况',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params: any) {
        const data = params[0].data
        return `
          <strong>${data.name}</strong><br/>
          总任务数: ${data.total}<br/>
          已完成: ${data.completed}<br/>
          完成率: ${data.rate}%
        `
      }
    },
    legend: {
      data: ['总任务数', '已完成'],
      bottom: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: taskData.map(item => item.name),
      axisLabel: {
        interval: 0,
        rotate: 30
      }
    },
    yAxis: {
      type: 'value',
      name: '任务数'
    },
    series: [
      {
        name: '总任务数',
        type: 'bar',
        barWidth: '40%',
        data: taskData.map(item => ({
          value: item.total,
          name: item.name,
          total: item.total,
          completed: item.completed,
          rate: item.rate,
          itemStyle: {
            color: '#E0E0E0'
          }
        }))
      },
      {
        name: '已完成',
        type: 'bar',
        barWidth: '40%',
        barGap: '-100%',
        data: taskData.map(item => ({
          value: item.completed,
          name: item.name,
          total: item.total,
          completed: item.completed,
          rate: item.rate,
          itemStyle: {
            color: getColorByRate(item.rate)
          }
        })),
        label: {
          show: true,
          position: 'top',
          formatter: '{c} ({d}%)',
          fontSize: 10
        }
      }
    ]
  }

  chart.setOption(option)

  window.addEventListener('resize', handleResize)
})

function getColorByRate(rate: number) {
  if (rate >= 95) return '#00C853'
  if (rate >= 90) return '#2196F3'
  if (rate >= 85) return '#FF9800'
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
        series: [
          { data: newData.map(item => ({ value: item.total })) },
          { data: newData.map(item => ({ value: item.completed })) }
        ]
      })
    }
  }
})
</script>

<style scoped>
.task-stats-chart {
  width: 100%;
}

.chart-container {
  height: 300px;
  width: 100%;
}
</style>