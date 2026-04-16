<template>
  <div class="globe-container" ref="globeContainer">
    <!-- 调试信息 -->
    <div style="position: absolute; top: 0; left: 0; color: white; font-size: 12px; z-index: 1000;">
      renderSuccess: {{ renderSuccess }} (value: {{ renderSuccess.value }})
    </div>
    <!-- 降级方案：始终显示，3D地球成功时覆盖 -->
    <div v-show="!renderSuccess" class="globe-fallback">
      <div class="fallback-content">
        <div class="city-grid">
          <div v-for="city in cities" :key="city.name" class="city-card" :class="city.status">
            <div class="city-name">{{ city.name }}</div>
            <div class="city-stats">
              <span>🚗 {{ city.vehicles }}辆</span>
              <span>📦 {{ city.orders }}单</span>
            </div>
          </div>
        </div>
        <div class="route-list">
          <div v-for="route in routes" :key="route.name" class="route-item">
            {{ cities[route.from].name }} → {{ cities[route.to].name }}
          </div>
        </div>
      </div>
    </div>
    <!-- Three.js 3D地球 -->
    <div v-show="renderSuccess" class="globe-canvas" ref="globeCanvas"></div>
    <div v-if="renderSuccess" class="globe-controls">
      <n-button-group>
        <n-button size="small" @click="resetCamera">
          <template #icon><n-icon><refresh-outline /></n-icon></template>
          重置视角
        </n-button>
        <n-button size="small" @click="toggleRotation">
          <template #icon><n-icon><pause-outline v-if="isRotating" /><play-outline v-else /></n-icon></template>
          {{ isRotating ? '暂停' : '旋转' }}
        </n-button>
      </n-button-group>
    </div>
    <div class="globe-info">
      <n-card size="small" class="info-card">
        <n-space vertical :size="8">
          <div class="info-item">
            <span class="label">在线车辆</span>
            <span class="value">{{ vehicleCount }}</span>
          </div>
          <div class="info-item">
            <span class="label">活跃城市</span>
            <span class="value">{{ cityCount }}</span>
          </div>
          <div class="info-item">
            <span class="label">运输线路</span>
            <span class="value">{{ routeCount }}</span>
          </div>
        </n-space>
      </n-card>
    </div>
    <div class="city-tooltip" v-if="selectedCity" :style="tooltipStyle">
      <n-card size="small">
        <template #header>
          <n-space align="center">
            <n-icon size="16" color="#1890ff"><location-outline /></n-icon>
            <span>{{ selectedCity.name }}</span>
          </n-space>
        </template>
        <n-descriptions :column="1" label-placement="left" size="small">
          <n-descriptions-item label="车辆数">{{ selectedCity.vehicles }}</n-descriptions-item>
          <n-descriptions-item label="订单数">{{ selectedCity.orders }}</n-descriptions-item>
          <n-descriptions-item label="状态">
            <n-tag :type="selectedCity.status === 'active' ? 'success' : 'warning'" size="small">
              {{ selectedCity.status === 'active' ? '正常运营' : '繁忙' }}
            </n-tag>
          </n-descriptions-item>
        </n-descriptions>
      </n-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { NButton, NButtonGroup, NCard, NSpace, NDescriptions, NDescriptionsItem, NTag, NIcon } from 'naive-ui'
import { RefreshOutline, PauseOutline, PlayOutline, LocationOutline } from '@vicons/ionicons5'

// 检测WebGL支持
function checkWebGLSupport(): boolean {
  try {
    const canvas = document.createElement('canvas')
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
    return !!gl
  } catch (e) {
    return false
  }
}

const webglSupported = ref(checkWebGLSupport())
const renderSuccess = ref(false) // 渲染成功标志
const globeContainer = ref<HTMLElement | null>(null)
const globeCanvas = ref<HTMLElement | null>(null)

let scene: any
let camera: any
let renderer: any
let controls: any
let earth: any
let atmosphere: any
let clouds: any
let animationId: number | null = null
let isRotating = ref(true)

const selectedCity = ref<any>(null)
const tooltipStyle = ref({ left: '0px', top: '0px' })

// 城市数据
const cities = [
  { name: '北京', lat: 39.9042, lng: 116.4074, vehicles: 45, orders: 1280, status: 'active' },
  { name: '上海', lat: 31.2304, lng: 121.4737, vehicles: 62, orders: 1850, status: 'active' },
  { name: '广州', lat: 23.1291, lng: 113.2644, vehicles: 38, orders: 980, status: 'active' },
  { name: '深圳', lat: 22.5431, lng: 114.0579, vehicles: 42, orders: 1120, status: 'busy' },
  { name: '成都', lat: 30.5728, lng: 104.0668, vehicles: 28, orders: 745, status: 'active' },
  { name: '重庆', lat: 29.5630, lng: 106.5516, vehicles: 25, orders: 680, status: 'active' },
  { name: '杭州', lat: 30.2741, lng: 120.1551, vehicles: 35, orders: 920, status: 'active' },
  { name: '天津', lat: 39.3434, lng: 117.3616, vehicles: 22, orders: 560, status: 'active' },
  { name: '武汉', lat: 30.5928, lng: 114.3055, vehicles: 30, orders: 820, status: 'busy' },
  { name: '西安', lat: 34.3416, lng: 108.9398, vehicles: 18, orders: 420, status: 'active' },
]

// 运输线路
const routes = [
  { from: 0, to: 1, name: '京沪线' },
  { from: 1, to: 6, name: '沪杭线' },
  { from: 2, to: 3, name: '广深线' },
  { from: 0, to: 7, name: '京津线' },
  { from: 4, to: 5, name: '成渝线' },
  { from: 1, to: 8, name: '沪汉线' },
  { from: 0, to: 9, name: '京西线' },
]

const vehicleCount = computed(() => cities.reduce((sum, city) => sum + city.vehicles, 0))
const cityCount = computed(() => cities.length)
const routeCount = computed(() => routes.length)

// Three.js相关 - 只在支持WebGL时加载
let THREE: any = null
let OrbitControls: any = null
let initTimeout: any = null

async function initThreeJS() {
  console.log('[GlobeVisualization] initThreeJS called, webglSupported:', webglSupported.value)
  // 添加超时保护，如果3秒内没有初始化成功，使用降级方案
  initTimeout = setTimeout(() => {
    if (!renderer) {
      console.warn('[GlobeVisualization] Three.js initialization timeout, using fallback')
      webglSupported.value = false
    }
  }, 3000)
  
  if (!webglSupported.value) {
    console.log('[GlobeVisualization] WebGL not supported, skipping Three.js')
    clearTimeout(initTimeout)
    return
  }
  
  try {
    console.log('[GlobeVisualization] Loading Three.js modules...')
    THREE = await import('three')
    const OrbitControlsModule = await import('three/examples/jsm/controls/OrbitControls.js')
    OrbitControls = OrbitControlsModule.OrbitControls
    console.log('[GlobeVisualization] Three.js modules loaded successfully')
    
    // 等待DOM渲染完成
    await new Promise(resolve => setTimeout(resolve, 100))
    
    if (globeCanvas.value) {
      console.log('[GlobeVisualization] Globe canvas element found, initializing scene...')
      initScene()
      // 确保 renderSuccess 设置为 true
      renderSuccess.value = true
      console.log('[GlobeVisualization] renderSuccess forced to true after initScene')
      clearTimeout(initTimeout)
    } else {
      throw new Error('Canvas element not found')
    }
  } catch (error) {
    console.error('[GlobeVisualization] Failed to load Three.js:', error)
    clearTimeout(initTimeout)
    webglSupported.value = false
  }
}

// 经纬度转3D坐标
function latLngToVector3(lat: number, lng: number, radius: number): THREE.Vector3 {
  const phi = (90 - lat) * (Math.PI / 180)
  const theta = (lng + 180) * (Math.PI / 180)
  
  const x = -radius * Math.sin(phi) * Math.cos(theta)
  const y = radius * Math.cos(phi)
  const z = radius * Math.sin(phi) * Math.sin(theta)
  
  return new THREE.Vector3(x, y, z)
}

// 创建地球纹理
function createEarthTexture(): THREE.Texture {
  const canvas = document.createElement('canvas')
  canvas.width = 2048
  canvas.height = 1024
  const ctx = canvas.getContext('2d')!
  
  // 海洋背景
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
  gradient.addColorStop(0, '#0a1628')
  gradient.addColorStop(0.5, '#0d2137')
  gradient.addColorStop(1, '#0a1628')
  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  
  // 绘制大陆轮廓（简化版）
  ctx.fillStyle = '#1e3a5f'
  ctx.strokeStyle = '#2d5a8a'
  ctx.lineWidth = 2
  
  // 亚洲
  ctx.beginPath()
  ctx.ellipse(1400, 400, 300, 200, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // 欧洲
  ctx.beginPath()
  ctx.ellipse(1100, 350, 150, 100, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // 非洲
  ctx.beginPath()
  ctx.ellipse(1100, 550, 120, 150, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // 北美洲
  ctx.beginPath()
  ctx.ellipse(500, 350, 200, 150, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // 南美洲
  ctx.beginPath()
  ctx.ellipse(600, 600, 100, 150, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // 澳洲
  ctx.beginPath()
  ctx.ellipse(1600, 650, 80, 60, 0, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()
  
  // 添加网格线
  ctx.strokeStyle = 'rgba(30, 136, 229, 0.3)'
  ctx.lineWidth = 1
  for (let i = 0; i < canvas.width; i += 128) {
    ctx.beginPath()
    ctx.moveTo(i, 0)
    ctx.lineTo(i, canvas.height)
    ctx.stroke()
  }
  for (let i = 0; i < canvas.height; i += 128) {
    ctx.beginPath()
    ctx.moveTo(0, i)
    ctx.lineTo(canvas.width, i)
    ctx.stroke()
  }
  
  const texture = new THREE.CanvasTexture(canvas)
  texture.needsUpdate = true
  return texture
}

// 创建地球
function createEarth(): THREE.Mesh {
  const geometry = new THREE.SphereGeometry(2, 64, 64)
  const material = new THREE.MeshPhongMaterial({
    map: createEarthTexture(),
    bumpScale: 0.05,
    specular: new THREE.Color(0x333333),
    shininess: 5,
  })
  earth = new THREE.Mesh(geometry, material)
  return earth
}

// 创建大气层
function createAtmosphere(): THREE.Mesh {
  const geometry = new THREE.SphereGeometry(2.1, 64, 64)
  const material = new THREE.ShaderMaterial({
    vertexShader: `
      varying vec3 vNormal;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      varying vec3 vNormal;
      void main() {
        float intensity = pow(0.7 - dot(vNormal, vec3(0.0, 0.0, 1.0)), 2.0);
        gl_FragColor = vec4(0.3, 0.6, 1.0, 1.0) * intensity;
      }
    `,
    blending: THREE.AdditiveBlending,
    side: THREE.BackSide,
    transparent: true,
  })
  atmosphere = new THREE.Mesh(geometry, material)
  return atmosphere
}

// 创建云层
function createClouds(): THREE.Mesh {
  const geometry = new THREE.SphereGeometry(2.05, 64, 64)
  const material = new THREE.MeshPhongMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.15,
    depthWrite: false,
  })
  clouds = new THREE.Mesh(geometry, material)
  return clouds
}

// 创建城市标记
function createCityMarkers(): THREE.Group {
  const group = new THREE.Group()
  
  cities.forEach((city, index) => {
    const position = latLngToVector3(city.lat, city.lng, 2.02)
    
    // 城市点
    const dotGeometry = new THREE.SphereGeometry(0.03, 16, 16)
    const dotMaterial = new THREE.MeshBasicMaterial({ 
      color: city.status === 'active' ? 0x00ff88 : 0xffaa00 
    })
    const dot = new THREE.Mesh(dotGeometry, dotMaterial)
    dot.position.copy(position)
    dot.userData = { cityIndex: index }
    group.add(dot)
    
    // 光环
    const ringGeometry = new THREE.RingGeometry(0.04, 0.06, 32)
    const ringMaterial = new THREE.MeshBasicMaterial({
      color: city.status === 'active' ? 0x00ff88 : 0xffaa00,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.5,
    })
    const ring = new THREE.Mesh(ringGeometry, ringMaterial)
    ring.position.copy(position)
    ring.lookAt(0, 0, 0)
    group.add(ring)
    
    // 脉冲动画光环
    const pulseGeometry = new THREE.RingGeometry(0.06, 0.08, 32)
    const pulseMaterial = new THREE.MeshBasicMaterial({
      color: city.status === 'active' ? 0x00ff88 : 0xffaa00,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.3,
    })
    const pulse = new THREE.Mesh(pulseGeometry, pulseMaterial)
    pulse.position.copy(position)
    pulse.lookAt(0, 0, 0)
    pulse.userData = { isPulse: true, baseScale: 1 }
    group.add(pulse)
  })
  
  return group
}

// 创建运输线路
function createRoutes(): THREE.Group {
  const group = new THREE.Group()
  
  routes.forEach(route => {
    const fromCity = cities[route.from]
    const toCity = cities[route.to]
    
    const startPos = latLngToVector3(fromCity.lat, fromCity.lng, 2.02)
    const endPos = latLngToVector3(toCity.lat, toCity.lng, 2.02)
    
    // 计算曲线控制点
    const midPoint = new THREE.Vector3()
      .addVectors(startPos, endPos)
      .multiplyScalar(0.5)
      .normalize()
      .multiplyScalar(2.5)
    
    // 创建曲线
    const curve = new THREE.QuadraticBezierCurve3(startPos, midPoint, endPos)
    const points = curve.getPoints(50)
    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    
    const material = new THREE.LineBasicMaterial({
      color: 0x00aaff,
      transparent: true,
      opacity: 0.6,
    })
    
    const line = new THREE.Line(geometry, material)
    group.add(line)
    
    // 添加流动粒子
    const particleGeometry = new THREE.SphereGeometry(0.02, 8, 8)
    const particleMaterial = new THREE.MeshBasicMaterial({
      color: 0x00ffff,
      transparent: true,
      opacity: 0.8,
    })
    const particle = new THREE.Mesh(particleGeometry, particleMaterial)
    particle.userData = { curve, progress: Math.random() }
    group.add(particle)
  })
  
  return group
}

// 初始化场景
function initScene() {
  console.log('[GlobeVisualization] initScene started')
  if (!globeCanvas.value) {
    console.error('[GlobeVisualization] globeCanvas.value is null')
    return
  }
  
  const container = globeCanvas.value
  let width = container.clientWidth
  let height = container.clientHeight
  console.log('[GlobeVisualization] Initial container dimensions:', width, height)
  
  // 如果容器尺寸为0，使用默认尺寸
  if (width === 0 || height === 0) {
    console.warn('[GlobeVisualization] Container dimensions are 0, using default size 500x500')
    width = 500
    height = 500
  }
  
  // 创建场景
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x000510)
  
  // 创建相机
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000)
  camera.position.set(0, 2, 5)
  
  // 创建渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(width, height)
  renderer.setPixelRatio(window.devicePixelRatio)
  container.appendChild(renderer.domElement)
  console.log('[GlobeVisualization] WebGL renderer created and appended')
  
  // 创建控制器
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.rotateSpeed = 0.5
  controls.minDistance = 3
  controls.maxDistance = 10
  controls.enablePan = false
  
  // 添加光源
  const ambientLight = new THREE.AmbientLight(0x404040, 0.5)
  scene.add(ambientLight)
  
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
  directionalLight.position.set(5, 3, 5)
  scene.add(directionalLight)
  
  const pointLight = new THREE.PointLight(0x1890ff, 0.5, 20)
  pointLight.position.set(-5, 2, -5)
  scene.add(pointLight)
  
  // 添加星空背景
  const starGeometry = new THREE.BufferGeometry()
  const starCount = 2000
  const positions = new Float32Array(starCount * 3)
  for (let i = 0; i < starCount * 3; i += 3) {
    positions[i] = (Math.random() - 0.5) * 100
    positions[i + 1] = (Math.random() - 0.5) * 100
    positions[i + 2] = (Math.random() - 0.5) * 100
  }
  starGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  const starMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.1,
    transparent: true,
    opacity: 0.8,
  })
  const stars = new THREE.Points(starGeometry, starMaterial)
  scene.add(stars)
  
  // 添加地球组件
  scene.add(createEarth())
  scene.add(createAtmosphere())
  scene.add(createClouds())
  scene.add(createCityMarkers())
  scene.add(createRoutes())
  
  // 添加鼠标交互
  renderer.domElement.addEventListener('mousemove', onMouseMove)
  
  // 标记渲染成功
  renderSuccess.value = true
  console.log('[GlobeVisualization] renderSuccess set to true')
  
  // 开始动画
  console.log('[GlobeVisualization] Starting animation loop')
  animate()
}

// 鼠标移动事件
function onMouseMove(event: MouseEvent) {
  if (!globeCanvas.value) return
  
  const rect = globeCanvas.value.getBoundingClientRect()
  const mouse = new THREE.Vector2(
    ((event.clientX - rect.left) / rect.width) * 2 - 1,
    -((event.clientY - rect.top) / rect.height) * 2 + 1
  )
  
  const raycaster = new THREE.Raycaster()
  raycaster.setFromCamera(mouse, camera)
  
  // 检测城市标记
  const cityMarkers = scene.children.find(obj => obj instanceof THREE.Group && obj.children[0]?.userData?.cityIndex !== undefined)
  if (cityMarkers) {
    const intersects = raycaster.intersectObjects(cityMarkers.children)
    if (intersects.length > 0) {
      const cityIndex = intersects[0].object.userData?.cityIndex
      if (cityIndex !== undefined) {
        selectedCity.value = cities[cityIndex]
        tooltipStyle.value = {
          left: `${event.clientX - rect.left + 20}px`,
          top: `${event.clientY - rect.top}px`,
        }
        return
      }
    }
  }
  
  selectedCity.value = null
}

// 动画循环
function animate() {
  animationId = requestAnimationFrame(animate)
  
  // 地球自转
  if (isRotating.value) {
    earth.rotation.y += 0.001
    clouds.rotation.y += 0.0012
    atmosphere.rotation.y += 0.001
  }
  
  // 更新控制器
  controls.update()
  
  // 更新粒子动画
  scene.traverse((obj) => {
    if (obj.userData?.isPulse) {
      const scale = 1 + Math.sin(Date.now() * 0.003) * 0.3
      obj.scale.set(scale, scale, scale)
      if (obj instanceof THREE.Mesh && obj.material instanceof THREE.MeshBasicMaterial) {
        obj.material.opacity = 0.3 - Math.sin(Date.now() * 0.003) * 0.2
      }
    }
    
    // 流动粒子
    if (obj.userData?.curve) {
      obj.userData.progress += 0.005
      if (obj.userData.progress > 1) obj.userData.progress = 0
      const point = obj.userData.curve.getPoint(obj.userData.progress)
      obj.position.copy(point)
    }
  })
  
  renderer.render(scene, camera)
}

// 重置视角
function resetCamera() {
  camera.position.set(0, 2, 5)
  camera.lookAt(0, 0, 0)
  controls.reset()
}

// 切换旋转
function toggleRotation() {
  isRotating.value = !isRotating.value
}

// 窗口大小变化
function onResize() {
  if (!globeCanvas.value) return
  
  const width = globeCanvas.value.clientWidth
  const height = globeCanvas.value.clientHeight
  
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

onMounted(() => {
  initThreeJS()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', onResize)
  if (initTimeout) {
    clearTimeout(initTimeout)
  }
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  renderer?.dispose()
  controls?.dispose()
})
</script>

<style lang="scss" scoped>
.globe-container {
  position: relative;
  width: 100%;
  height: 500px;
  min-height: 500px;
  background: linear-gradient(135deg, #000510 0%, #0a1628 100%);
  border-radius: 12px;
  overflow: hidden;
}

.globe-canvas {
  width: 100%;
  height: 500px;
  min-height: 500px;
}

// WebGL不支持时的降级样式
.globe-fallback {
  width: 100%;
  height: 500px;
  min-height: 500px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .fallback-content {
    width: 100%;
    
    .city-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
      
      .city-card {
        background: rgba(24, 144, 255, 0.1);
        border: 1px solid rgba(24, 144, 255, 0.3);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        transition: all 0.3s;
        
        &:hover {
          background: rgba(24, 144, 255, 0.2);
          transform: translateY(-2px);
        }
        
        &.busy {
          border-color: rgba(250, 173, 20, 0.5);
          background: rgba(250, 173, 20, 0.1);
        }
        
        .city-name {
          color: #fff;
          font-weight: bold;
          margin-bottom: 8px;
        }
        
        .city-stats {
          display: flex;
          flex-direction: column;
          gap: 4px;
          font-size: 12px;
          color: rgba(255, 255, 255, 0.7);
        }
      }
    }
    
    .route-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      
      .route-item {
        background: rgba(0, 170, 255, 0.2);
        color: #00aaff;
        padding: 6px 12px;
        border-radius: 16px;
        font-size: 12px;
      }
    }
  }
}

.globe-controls {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
}

.globe-info {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 10;
  
  .info-card {
    background: rgba(0, 20, 40, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(24, 144, 255, 0.3);
    
    .info-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      
      .label {
        color: rgba(255, 255, 255, 0.6);
        font-size: 12px;
      }
      
      .value {
        color: #1890ff;
        font-size: 16px;
        font-weight: bold;
      }
    }
  }
}

.city-tooltip {
  position: absolute;
  z-index: 20;
  pointer-events: none;
  
  :deep(.n-card) {
    background: rgba(0, 20, 40, 0.9);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(24, 144, 255, 0.5);
    min-width: 150px;
  }
}
</style>