/**
 * API服务层
 */
import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios'

// 创建axios实例
const apiClient: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 添加token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      switch (status) {
        case 401:
          // 未授权，跳转到登录页
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          console.error('没有权限访问该资源')
          break
        case 404:
          console.error('请求的资源不存在')
          break
        case 500:
          console.error('服务器错误')
          break
        default:
          console.error(data.message || '请求失败')
      }
    }
    return Promise.reject(error)
  }
)

// 车辆API
export const vehicleApi = {
  getVehicles: (params?: any) => apiClient.get('/vehicles', { params }),
  getVehicleById: (id: string) => apiClient.get(`/vehicles/${id}`),
  createVehicle: (data: any) => apiClient.post('/vehicles', data),
  updateVehicle: (id: string, data: any) => apiClient.put(`/vehicles/${id}`, data),
  deleteVehicle: (id: string) => apiClient.delete(`/vehicles/${id}`),
  getVehicleStats: () => apiClient.get('/vehicles/stats/summary'),
}

// 订单API
export const orderApi = {
  getOrders: (params?: any) => apiClient.get('/orders', { params }),
  getOrderById: (id: string) => apiClient.get(`/orders/${id}`),
  createOrder: (data: any) => apiClient.post('/orders', data),
  updateOrder: (id: string, data: any) => apiClient.put(`/orders/${id}`, data),
  deleteOrder: (id: string) => apiClient.delete(`/orders/${id}`),
  getOrderStats: () => apiClient.get('/orders/stats/summary'),
}

// 仓库API
export const warehouseApi = {
  getWarehouses: (params?: any) => apiClient.get('/warehouses', { params }),
  getWarehouseById: (id: string) => apiClient.get(`/warehouses/${id}`),
  createWarehouse: (data: any) => apiClient.post('/warehouses', data),
  updateWarehouse: (id: string, data: any) => apiClient.put(`/warehouses/${id}`, data),
  deleteWarehouse: (id: string) => apiClient.delete(`/warehouses/${id}`),
  getWarehouseStats: () => apiClient.get('/warehouses/stats/summary'),
}

// 预测API
export const predictionApi = {
  predictDemand: (data: any) => apiClient.post('/predictions/demand', data),
  predictCapacity: (data: any) => apiClient.post('/predictions/capacity', data),
  predictCost: (data: any) => apiClient.post('/predictions/cost', data),
  predictRisk: (data: any) => apiClient.post('/predictions/risk', data),
  batchPredict: (data: any[]) => apiClient.post('/predictions/batch', data),
  getModels: () => apiClient.get('/predictions/models'),
}

// 设备API（叉车等）
export const equipmentApi = {
  getForklifts: (params?: any) => apiClient.get('/equipment/forklifts', { params }),
  getForkliftById: (id: string) => apiClient.get(`/equipment/forklifts/${id}`),
  getEquipmentStats: () => apiClient.get('/equipment/stats'),
  getTaskStats: () => apiClient.get('/equipment/tasks/stats'),
}

// 控制台API
export const dashboardApi = {
  getOverview: () => apiClient.get('/dashboard/overview'),
  getRealtime: () => apiClient.get('/dashboard/realtime'),
  getTrends: (days?: number) => apiClient.get('/dashboard/trends', { params: { days } }),
  getDistribution: () => apiClient.get('/dashboard/distribution'),
  getTopRoutes: () => apiClient.get('/dashboard/top-routes'),
  getMapData: () => apiClient.get('/dashboard/map-data'),
}

export default apiClient
