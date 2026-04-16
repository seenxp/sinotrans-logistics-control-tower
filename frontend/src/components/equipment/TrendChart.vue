<template>
  <div class="trend-chart">
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

interface Props {
  title?: string
  timeRange?: 'week' | 'month'
  dataType?: 'tasks' | 'duration'
  park?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '设备趋势图',
  timeRange: 'week',
  dataType: 'tasks',
  park: 'all'
})

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 设备类型
const deviceTypes = ['小悠盘', '小寻叉', 'AGV', 'AGF', 'CTU', '自动线体', 'DWS']

// 生成日期数据
function generateDateData() {
  const dates: string[] = []
  const now = new Date()
  
  if (props.timeRange === 'week') {
    for (let i = 6; i >= 0; i--) {
      const date = new Date(now)
      date.setDate(date.getDate() - i)
      dates.push(`${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`)
    }
  } else {
    for (let i = 11; i >= 0; i--) {
      const date = new Date(now)
      date.setMonth(date.getMonth() - i)
      dates.push(`${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`)
    }
  }
  
  return dates
}

// 生成模拟数据
function generateMockData() {
  const dates = generateDateData()
  const series: any[] = []
  
  const colors = ['#00C853', '#2196F3', '#FF9800', '#9C27B0', '#F44336', '#00BCD4', '#795548']
  
  deviceTypes.forEach((device, index) => {
    const data: number[] = []
    
    dates.forEach(() => {
      if (props.dataType === 'tasks') {
        // 任务数数据
        data.push(Math.floor(Math.random() * 100) + 50)
      } else {
        // 使用时长数据（分钟）
        data.push(Math.floor(Math.random() * 300) + 120)
      }
    })
    
    series.push({
      name: device,
      type: 'line',
      smooth: true,
      data: data,
      itemStyle: {
        color: colors[index % colors.length]
      },
      lineStyle: {
        width: 2
      },
      symbol: 'circle',
      symbolSize: 6
    })
  })
  
  // 如果是任务数，添加异常任务线
  if (props.dataType === 'tasks') {
    const abnormalData: number[] = []
    dates.forEach(() => {
      abnormalData.push(Math.floor(Math.random() * 15) + 5)
    })
    
    series.push({
      name: '异常任务',
      type: 'line',
      smooth: true,
      data: abnormalData,
      itemStyle: {
        color: '#F44336'
      },
      lineStyle: {
        width: 2,
        type: 'dashed'
      },
      symbol: 'diamond',
      symbolSize: 8
    })
  }
  
  return { dates, series }
}

function getOption() {
  const { dates, series } = generateMockData()
  
  const yAxisConfig: any[] = []
  
  if (props.dataType === 'tasks') {
    yAxisConfig.push({
      type: 'value',
      name: '任务数',
      position: 'left',
      axisLine: {
        show: true,
        lineStyle: {
          color: '#5470C6'
        }
      },
      axisLabel: {
        formatter: '{value}'
      }
    })
  } else {
    yAxisConfig.push({
      type: 'value',
      name: '平均使用时长(分钟)',
      position: 'left',
      axisLine: {
        show: true,
        lineStyle: {
          color: '#5470C6'
        }
      },
      axisLabel: {
        formatter: '{value} min'
      }
    })
  }
  
  return {
    title: {
      text: props.title,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      type: 'scroll',
      bottom: 10,
      data: [...deviceTypes, ...(props.dataType === 'tasks' ? ['异常任务'] : [])]
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
      boundaryGap: false,
      data: dates,
      axisLabel: {
        rotate: dates.length > 7 ? 45 : 0
      }
    },
    yAxis: yAxisConfig,
    series: series,
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      },
      {
        start: 0,
        end: 100,
        handleIcon: 'path://M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '80%',
        handleStyle: {
          color: '#fff',
          shadowBlur: 3,
          shadowColor: 'rgba(0, 0, 0, 0.6)',
          shadowOffsetX: 2,
          shadowOffsetY: 2
        }
      }
    ]
  }
}

onMounted(() => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  chart.setOption(getOption())
  
  window.addEventListener('resize', handleResize)
})

watch(() => [props.timeRange, props.dataType, props.park], () => {
  if (chart) {
    chart.setOption(getOption(), true)
  }
})

function handleResize() {
  chart?.resize()
}

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})

defineExpose({
  refresh: () => {
    if (chart) {
      chart.setOption(getOption(), true)
    }
  }
})
</script>

<style scoped>
.trend-chart {
  width: 100%;
}

.chart-container {
  height: 350px;
  width: 100%;
}
</style>