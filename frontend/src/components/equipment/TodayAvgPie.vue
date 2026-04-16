<template>
  <div class="today-avg-pie">
    <n-grid :cols="2" :x-gap="16">
      <n-grid-item>
        <n-card title="小寻叉平均使用时长">
          <div ref="xiaoxunChartRef" class="chart-container"></div>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card title="小悠盘平均使用时长">
          <div ref="xiaoyouChartRef" class="chart-container"></div>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue'
import { NGrid, NGridItem, NCard } from 'naive-ui'
import * as echarts from 'echarts'

const xiaoxunChartRef = ref<HTMLElement>()
const xiaoyouChartRef = ref<HTMLElement>()
let xiaoxunChart: echarts.ECharts | null = null
let xiaoyouChart: echarts.ECharts | null = null

// 小寻叉数据（模拟数据）
const xiaoxunData = [
  { name: '≤2h', value: 45, itemStyle: { color: '#00C853' } },
  { name: '2-4h', value: 30, itemStyle: { color: '#2196F3' } },
  { name: '4-6h', value: 15, itemStyle: { color: '#FF9800' } },
  { name: '＞6h', value: 10, itemStyle: { color: '#F44336' } }
]

// 小悠盘数据（模拟数据）
const xiaoyouData = [
  { name: '≤2h', value: 38, itemStyle: { color: '#00C853' } },
  { name: '2-4h', value: 35, itemStyle: { color: '#2196F3' } },
  { name: '4-6h', value: 18, itemStyle: { color: '#FF9800' } },
  { name: '＞6h', value: 9, itemStyle: { color: '#F44336' } }
]

function createPieOption(title: string, data: any[]) {
  return {
    title: {
      text: title,
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 'right',
      top: 'middle'
    },
    series: [
      {
        name: '使用时长分布',
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['40%', '55%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
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
        labelLine: {
          show: true
        },
        data: data
      }
    ]
  }
}

onMounted(() => {
  if (xiaoxunChartRef.value) {
    xiaoxunChart = echarts.init(xiaoxunChartRef.value)
    xiaoxunChart.setOption(createPieOption('', xiaoxunData))
  }

  if (xiaoyouChartRef.value) {
    xiaoyouChart = echarts.init(xiaoyouChartRef.value)
    xiaoyouChart.setOption(createPieOption('', xiaoyouData))
  }

  window.addEventListener('resize', handleResize)
})

function handleResize() {
  xiaoxunChart?.resize()
  xiaoyouChart?.resize()
}

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  xiaoxunChart?.dispose()
  xiaoyouChart?.dispose()
})

// 暴露方法供父组件调用
defineExpose({
  updateData: (xiaoxun: any[], xiaoyou: any[]) => {
    if (xiaoxunChart) {
      xiaoxunChart.setOption({ series: [{ data: xiaoxun }] })
    }
    if (xiaoyouChart) {
      xiaoyouChart.setOption({ series: [{ data: xiaoyou }] })
    }
  }
})
</script>

<style scoped>
.today-avg-pie {
  width: 100%;
}

.chart-container {
  height: 280px;
  width: 100%;
}
</style>