<template>
  <div class="prediction-page">
    <n-card title="风险预测">
      <n-alert type="warning" title="风险预警">
        基于TimesFM模型，预测潜在风险，提前预警。
      </n-alert>
      
      <n-divider />
      
      <n-grid :cols="3" :x-gap="16">
        <n-grid-item>
          <n-card title="天气风险">
            <n-progress type="dashboard" :percentage="35" :color="getColor(35)" />
            <p style="text-align: center; margin-top: 16px; color: #52c41a;">低风险</p>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card title="交通风险">
            <n-progress type="dashboard" :percentage="58" :color="getColor(58)" />
            <p style="text-align: center; margin-top: 16px; color: #faad14;">中等风险</p>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card title="运营风险">
            <n-progress type="dashboard" :percentage="22" :color="getColor(22)" />
            <p style="text-align: center; margin-top: 16px; color: #52c41a;">低风险</p>
          </n-card>
        </n-grid-item>
      </n-grid>
      
      <n-divider />
      
      <n-card title="风险预警列表">
        <n-data-table :columns="columns" :data="riskData" />
      </n-card>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { NTag } from 'naive-ui'

const getColor = (value: number) => {
  if (value < 40) return '#52c41a'
  if (value < 70) return '#faad14'
  return '#f5222d'
}

const columns = [
  { title: '风险类型', key: 'type' },
  { 
    title: '风险等级', 
    key: 'level', 
    render: (row: any) => {
      const types: Record<string, 'success' | 'warning' | 'error'> = { 
        '低': 'success', 
        '中': 'warning', 
        '高': 'error' 
      }
      return h(NTag, { type: types[row.level] }, { default: () => row.level })
    }
  },
  { title: '影响范围', key: 'scope' },
  { title: '建议措施', key: 'action' },
]

const riskData = ref([
  { type: '天气风险', level: '低', scope: '华南地区', action: '正常运营' },
  { type: '交通风险', level: '中', scope: '京沪高速', action: '备选路线' },
  { type: '容量风险', level: '中', scope: '上海仓库', action: '增加运力' },
  { type: '延误风险', level: '低', scope: '成都-重庆', action: '加强监控' },
])
</script>

<style scoped>
.prediction-page { padding: 24px; }
</style>