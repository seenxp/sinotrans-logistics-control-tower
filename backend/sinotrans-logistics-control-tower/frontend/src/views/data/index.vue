<template>
  <div class="data-page">
    <n-grid :cols="2" :x-gap="16" :y-gap="16">
      <!-- 数据质量 -->
      <n-grid-item>
        <n-card title="数据质量监控">
          <n-progress type="dashboard" :percentage="96.5" :color="#52c41a" />
          <div style="text-align: center; margin-top: 16px">
            <n-tag type="success" size="large">优秀</n-tag>
          </div>
          <n-divider />
          <n-descriptions :column="1" label-placement="left">
            <n-descriptions-item label="完整度">98.5%</n-descriptions-item>
            <n-descriptions-item label="准确度">97.2%</n-descriptions-item>
            <n-descriptions-item label="一致性">95.8%</n-descriptions-item>
            <n-descriptions-item label="及时性">94.5%</n-descriptions-item>
          </n-descriptions>
        </n-card>
      </n-grid-item>

      <!-- 数据血缘 -->
      <n-grid-item>
        <n-card title="数据血缘追踪">
          <div class="blood-graph">
            <div class="node source">数据源</div>
            <div class="arrow">→</div>
            <div class="node process">ETL处理</div>
            <div class="arrow">→</div>
            <div class="node warehouse">数据仓库</div>
            <div class="arrow">→</div>
            <div class="node service">数据服务</div>
          </div>
          <n-divider />
          <n-data-table :columns="columns" :data="bloodData" size="small" />
        </n-card>
      </n-grid-item>

      <!-- 数据安全 -->
      <n-grid-item>
        <n-card title="数据安全管控">
          <n-list>
            <n-list-item>
              <template #prefix>
                <n-icon color="#52c41a"><shield-checkmark-outline /></n-icon>
              </template>
              <n-thing title="访问控制" description="RBAC权限管理已启用" />
            </n-list-item>
            <n-list-item>
              <template #prefix>
                <n-icon color="#52c41a"><lock-closed-outline /></n-icon>
              </template>
              <n-thing title="数据加密" description="AES-256加密存储" />
            </n-list-item>
            <n-list-item>
              <template #prefix>
                <n-icon color="#52c41a"><eye-outline /></n-icon>
              </template>
              <n-thing title="审计日志" description="操作日志已开启" />
            </n-list-item>
            <n-list-item>
              <template #prefix>
                <n-icon color="#faad14"><alert-circle-outline /></n-icon>
              </template>
              <n-thing title="脱敏规则" description="敏感数据已脱敏" />
            </n-list-item>
          </n-list>
        </n-card>
      </n-grid-item>

      <!-- 数据服务 -->
      <n-grid-item>
        <n-card title="数据服务管理">
          <n-data-table :columns="serviceColumns" :data="serviceData" size="small" />
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, h } from 'vue'
import { NTag } from 'naive-ui'
import { ShieldCheckmarkOutline, LockClosedOutline, EyeOutline, AlertCircleOutline } from '@vicons/ionicons5'

const columns = [
  { title: '数据表', key: 'table' },
  { title: '上游依赖', key: 'upstream' },
  { title: '下游应用', key: 'downstream' },
]

const bloodData = ref([
  { table: 'orders', upstream: '原始订单系统', downstream: '订单分析、预测服务' },
  { table: 'vehicles', upstream: 'GPS系统', downstream: '实时监控、调度系统' },
  { table: 'warehouses', upstream: 'WMS系统', downstream: '库存分析、容量预测' },
])

const serviceColumns = [
  { title: '服务名称', key: 'name' },
  { title: '调用次数', key: 'calls' },
  { title: '状态', key: 'status', render: (row: any) => h(NTag, { type: row.status === 'running' ? 'success' : 'error' }, { default: () => row.status === 'running' ? '运行中' : '异常' }) },
]

const serviceData = ref([
  { name: '订单查询API', calls: '125,680', status: 'running' },
  { name: '车辆定位API', calls: '89,450', status: 'running' },
  { name: '库存查询API', calls: '67,230', status: 'running' },
  { name: '预测服务API', calls: '23,150', status: 'running' },
])
</script>

<style scoped>
.data-page {
  padding: 24px;
}

.blood-graph {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 20px 0;
}

.node {
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: bold;
  text-align: center;
}

.node.source { background: #e6f7ff; color: #1890ff; }
.node.process { background: #fff7e6; color: #fa8c16; }
.node.warehouse { background: #f6ffed; color: #52c41a; }
.node.service { background: #f9f0ff; color: #722ed1; }

.arrow {
  font-size: 24px;
  color: #8c8c8c;
}
</style>
