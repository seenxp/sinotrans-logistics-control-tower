/**
 * 订单状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { orderApi } from '@/services/api'

export interface Order {
  id: string
  origin: string
  destination: string
  cargoType: string
  weight: number
  volume: number | null
  priority: 'low' | 'normal' | 'high' | 'urgent'
  status: 'pending' | 'processing' | 'in_transit' | 'delivered' | 'cancelled'
  vehicleId: string | null
  estimatedDelivery: string | null
  createdAt: string
  updatedAt: string
}

export const useOrderStore = defineStore('order', () => {
  // 状态
  const orders = ref<Order[]>([])
  const loading = ref(false)
  const currentOrder = ref<Order | null>(null)

  // 计算属性
  const pendingOrders = computed(() =>
    orders.value.filter(o => o.status === 'pending')
  )
  const inTransitOrders = computed(() =>
    orders.value.filter(o => o.status === 'in_transit')
  )
  const deliveredOrders = computed(() =>
    orders.value.filter(o => o.status === 'delivered')
  )
  const orderStats = computed(() => ({
    total: orders.value.length,
    pending: pendingOrders.value.length,
    inTransit: inTransitOrders.value.length,
    delivered: deliveredOrders.value.length,
    completionRate: orders.value.length > 0
      ? Math.round((deliveredOrders.value.length / orders.value.length) * 100)
      : 0,
  }))

  // 方法
  async function fetchOrders(params?: { status?: string; priority?: string }) {
    loading.value = true
    try {
      const response = await orderApi.getOrders(params)
      orders.value = response
    } catch (error) {
      console.error('获取订单列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  async function fetchOrderById(id: string) {
    try {
      const response = await orderApi.getOrderById(id)
      currentOrder.value = response
      return response
    } catch (error) {
      console.error('获取订单详情失败:', error)
      return null
    }
  }

  function setCurrentOrder(order: Order | null) {
    currentOrder.value = order
  }

  return {
    orders,
    loading,
    currentOrder,
    pendingOrders,
    inTransitOrders,
    deliveredOrders,
    orderStats,
    fetchOrders,
    fetchOrderById,
    setCurrentOrder,
  }
})
