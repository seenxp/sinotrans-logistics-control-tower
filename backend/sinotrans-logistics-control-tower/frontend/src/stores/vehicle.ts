/**
 * 车辆状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { vehicleApi } from '@/services/api'

export interface Vehicle {
  id: string
  plateNumber: string
  vehicleType: 'truck' | 'ship' | 'plane' | 'train'
  capacity: number
  currentLat: number | null
  currentLng: number | null
  status: 'idle' | 'active' | 'maintenance'
  createdAt: string
  updatedAt: string
}

export const useVehicleStore = defineStore('vehicle', () => {
  // 状态
  const vehicles = ref<Vehicle[]>([])
  const loading = ref(false)
  const currentVehicle = ref<Vehicle | null>(null)

  // 计算属性
  const activeVehicles = computed(() =>
    vehicles.value.filter(v => v.status === 'active')
  )
  const idleVehicles = computed(() =>
    vehicles.value.filter(v => v.status === 'idle')
  )
  const vehicleStats = computed(() => ({
    total: vehicles.value.length,
    active: activeVehicles.value.length,
    idle: idleVehicles.value.length,
    maintenance: vehicles.value.filter(v => v.status === 'maintenance').length,
    utilizationRate: vehicles.value.length > 0
      ? Math.round((activeVehicles.value.length / vehicles.value.length) * 100)
      : 0,
  }))

  // 方法
  async function fetchVehicles(params?: { vehicleType?: string; status?: string }) {
    loading.value = true
    try {
      const response = await vehicleApi.getVehicles(params)
      vehicles.value = response
    } catch (error) {
      console.error('获取车辆列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  async function fetchVehicleById(id: string) {
    try {
      const response = await vehicleApi.getVehicleById(id)
      currentVehicle.value = response
      return response
    } catch (error) {
      console.error('获取车辆详情失败:', error)
      return null
    }
  }

  function setCurrentVehicle(vehicle: Vehicle | null) {
    currentVehicle.value = vehicle
  }

  return {
    vehicles,
    loading,
    currentVehicle,
    activeVehicles,
    idleVehicles,
    vehicleStats,
    fetchVehicles,
    fetchVehicleById,
    setCurrentVehicle,
  }
})
