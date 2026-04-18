/**
 * 路由配置
 */
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/dashboard',
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '控制台', icon: 'dashboard' },
      },
      {
        path: 'monitor',
        name: 'Monitor',
        component: () => import('@/views/dashboard/monitor.vue'),
        meta: { title: '实时监控', icon: 'monitor' },
      },
      {
        path: 'prediction',
        name: 'Prediction',
        redirect: '/prediction/demand',
      },
      {
        path: 'prediction/demand',
        name: 'DemandPrediction',
        component: () => import('@/views/prediction/demand.vue'),
        meta: { title: '需求预测' },
      },
      {
        path: 'prediction/capacity',
        name: 'CapacityPrediction',
        component: () => import('@/views/prediction/capacity.vue'),
        meta: { title: '运力预测' },
      },
      {
        path: 'prediction/cost',
        name: 'CostPrediction',
        component: () => import('@/views/prediction/cost.vue'),
        meta: { title: '成本预测' },
      },
      {
        path: 'prediction/risk',
        name: 'RiskPrediction',
        component: () => import('@/views/prediction/risk.vue'),
        meta: { title: '风险预测' },
      },
      {
        path: 'operations',
        name: 'Operations',
        redirect: '/operations/orders',
      },
      {
        path: 'operations/orders',
        name: 'OrderManagement',
        component: () => import('@/views/operations/orders.vue'),
        meta: { title: '订单管理' },
      },
      {
        path: 'operations/vehicles',
        name: 'VehicleManagement',
        component: () => import('@/views/operations/vehicles.vue'),
        meta: { title: '车辆管理' },
      },
      {
        path: 'operations/equipment',
        name: 'EquipmentManagement',
        component: () => import('@/views/operations/equipment.vue'),
        meta: { title: '设备管理' },
      },
      {
        path: 'operations/warehouses',
        name: 'WarehouseManagement',
        component: () => import('@/views/operations/warehouses.vue'),
        meta: { title: '仓库管理' },
      },
      {
        path: 'api-docs',
        name: 'ApiDocs',
        component: () => import('@/views/api-docs.vue'),
        meta: { title: '开放接口' },
      },
      {
        path: 'intelligence',
        name: 'GlobalIntelligence',
        component: () => import('@/views/intelligence/index.vue'),
        meta: { title: '全球情报', icon: 'globe' },
      },
      {
        path: 'data',
        name: 'Data',
        component: () => import('@/views/data/index.vue'),
        meta: { title: '数据治理', icon: 'database' },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/404.vue'),
    meta: { title: '页面不存在' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  },
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  const title = to.meta.title as string
  document.title = title ? `${title} - 外运物流控制塔` : '外运物流控制塔'
  next()
})

export default router