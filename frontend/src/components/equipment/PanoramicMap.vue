<template>
  <div ref="chartRef" class="panoramic-map"></div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 物流园区数据（模拟数据，实际从后端获取）
const parkData = [
  { 
    name: '上海奉贤', 
    value: [121.47, 31.23], 
    symbolSize: 35, 
    itemStyle: { color: '#00C853' },
    deviceCount: 156,
    onlineCount: 142,
    taskCount: 89
  },
  { 
    name: '广州东勤', 
    value: [113.25, 23.13], 
    symbolSize: 28, 
    itemStyle: { color: '#FF9800' },
    deviceCount: 98,
    onlineCount: 85,
    taskCount: 67
  },
  { 
    name: '重庆园区', 
    value: [106.55, 29.56], 
    symbolSize: 30, 
    itemStyle: { color: '#2196F3' },
    deviceCount: 120,
    onlineCount: 108,
    taskCount: 78
  }
]

// 设备类型数据
const deviceTypes = [
  { name: '小悠盘', count: 45, online: 42 },
  { name: '小寻叉', count: 38, online: 35 },
  { name: 'AGV', count: 52, online: 48 },
  { name: 'AGF', count: 28, online: 25 },
  { name: 'CTU', count: 36, online: 33 },
  { name: '自动线体', count: 15, online: 14 },
  { name: 'DWS', count: 12, online: 11 }
]

onMounted(async () => {
  if (!chartRef.value) return

  // 动态加载中国地图JSON
  try {
    const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    const chinaMap = await response.json()
    echarts.registerMap('china', chinaMap)
  } catch (error) {
    console.error('加载中国地图失败:', error)
    // 使用简化的地图配置
  }

  chart = echarts.init(chartRef.value)

  const option = {
    title: {
      text: '全国自动化设备全景图',
      left: 'center',
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: function(params: any) {
        if (params.seriesType === 'scatter') {
          const data = params.data
          return `
            <div style="padding: 8px;">
              <strong>${data.name}</strong><br/>
              设备总数: ${data.deviceCount}<br/>
              在线设备: ${data.onlineCount}<br/>
              当前任务: ${data.taskCount}<br/>
              在线率: ${((data.onlineCount / data.deviceCount) * 100).toFixed(1)}%
            </div>
          `
        }
        return params.name
      }
    },
    visualMap: {
      min: 0,
      max: 100,
      text: ['高在线率', '低在线率'],
      left: 'left',
      bottom: '20px',
      inRange: {
        color: ['#ff4444', '#ffaa00', '#00cc66']
      }
    },
    geo: {
      map: 'china',
      roam: true,
      zoom: 1.2,
      label: {
        show: true,
        fontSize: 10,
        color: '#333'
      },
      itemStyle: {
        areaColor: '#E6F3FF',
        borderColor: '#999',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: {
          areaColor: '#cce5ff'
        }
      }
    },
    series: [
      {
        name: '物流园区',
        type: 'scatter',
        coordinateSystem: 'geo',
        data: parkData,
        symbol: 'circle',
        label: {
          show: true,
          formatter: '{b}',
          position: 'right',
          fontSize: 12,
          color: '#333'
        },
        emphasis: {
          scale: 1.5
        }
      },
      {
        name: '设备分布',
        type: 'effectScatter',
        coordinateSystem: 'geo',
        data: parkData.map(item => ({
          ...item,
          symbolSize: item.onlineCount / 5
        })),
        symbol: 'circle',
        showEffectOn: 'render',
        rippleEffect: {
          brushType: 'stroke',
          scale: 3
        },
        itemStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      }
    ]
  }

  chart.setOption(option)

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

function handleResize() {
  chart?.resize()
}

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})

// 暴露方法供父组件调用
defineExpose({
  updateData: (newData: any[]) => {
    if (chart) {
      chart.setOption({
        series: [
          { data: newData },
          { data: newData.map(item => ({
            ...item,
            symbolSize: item.onlineCount / 5
          }))}
        ]
      })
    }
  }
})
</script>

<style scoped>
.panoramic-map {
  width: 100%;
  height: 520px;
  min-height: 520px;
}
</style>