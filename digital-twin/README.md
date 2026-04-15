# 外运物流控制塔 - 数字孪生模块

基于DigitalTwinScreen的3D数字孪生可视化模块，为物流控制塔提供实时3D场景展示。

## 功能特性

- 全球物流网络3D可视化
- 实时运力监控
- 3D模型加载与渲染
- 地理空间数据可视化
- 交互式3D场景

## 技术栈

- **3D引擎**: Three.js
- **地理空间**: Cesium.js
- **模型格式**: GLTF/GLB, OBJ, FBX
- **渲染**: WebGL 2.0
- **数据格式**: GeoJSON, KML

## 快速开始

### 环境要求
- Node.js 18+
- 现代浏览器 (Chrome, Firefox, Safari, Edge)
- WebGL 2.0 支持

### 安装步骤

1. 安装依赖
```bash
npm install three @types/three
npm install cesium
npm install @types/cesium
```

2. 配置Cesium Ion
```bash
# 获取Cesium Ion Token
# https://cesium.com/ion/tokens

# 配置环境变量
export CESIUM_ION_TOKEN=your-token-here
```

3. 启动开发服务器
```bash
npm run dev
```

## 模块结构

```
digital-twin/
├── 3d-models/           # 3D模型文件
│   ├── vehicles/       # 车辆模型
│   ├── warehouses/     # 仓库模型
│   ├── containers/     # 集装箱模型
│   └── infrastructure/ # 基础设施模型
├── scenes/              # 场景配置
│   ├── global.json    # 全球场景
│   ├── regional.json  # 区域场景
│   └── local.json     # 本地场景
├── textures/            # 纹理资源
│   ├── terrain/       # 地形纹理
│   ├── buildings/     # 建筑纹理
│   └── vehicles/      # 车辆纹理
├── src/                 # 源代码
│   ├── core/          # 核心引擎
│   ├── loaders/       # 模型加载器
│   ├── renderers/     # 渲染器
│   ├── controls/      # 控制器
│   └── utils/         # 工具函数
├── examples/            # 示例代码
├── docs/                # 文档
└── README.md
```

## 核心功能

### 1. 3D场景管理
```typescript
// 创建场景
const scene = new LogisticsScene({
  container: 'scene-container',
  camera: {
    fov: 60,
    near: 0.1,
    far: 1000000,
  },
  renderer: {
    antialias: true,
    alpha: true,
  },
});

// 添加车辆模型
scene.addVehicle({
  id: 'truck-001',
  model: 'models/truck.glb',
  position: { x: 100, y: 0, z: 100 },
  rotation: { x: 0, y: 45, z: 0 },
});
```

### 2. 地理空间可视化
```typescript
// 初始化Cesium
const viewer = new Cesium.Viewer('cesium-container', {
  terrainProvider: Cesium.createWorldTerrain(),
  baseLayerPicker: false,
  geocoder: false,
  homeButton: false,
  sceneModePicker: false,
  navigationHelpButton: false,
});

// 添加物流点
viewer.entities.add({
  position: Cesium.Cartesian3.fromDegrees(116.3974, 39.9093, 0),
  point: {
    pixelSize: 10,
    color: Cesium.Color.RED,
    outlineColor: Cesium.Color.WHITE,
    outlineWidth: 2,
  },
  label: {
    text: '北京仓库',
    font: '14pt sans-serif',
    style: Cesium.LabelStyle.FILL_AND_OUTLINE,
    outlineWidth: 2,
    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
    pixelOffset: new Cesium.Cartesian2(0, -9),
  },
});
```

### 3. 实时数据更新
```typescript
// 更新车辆位置
function updateVehiclePosition(vehicleId: string, position: Position) {
  const vehicle = scene.getObjectById(vehicleId);
  if (vehicle) {
    vehicle.position.set(position.x, position.y, position.z);
    vehicle.rotation.set(position.rotationX, position.rotationY, position.rotationZ);
  }
}

// 批量更新
function updateVehicles(vehicles: Vehicle[]) {
  vehicles.forEach(vehicle => {
    updateVehiclePosition(vehicle.id, vehicle.position);
  });
}
```

### 4. 交互控制
```typescript
// 轨道控制器
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 100;
controls.maxDistance = 10000;

// 飞行控制器
const flyControls = new FlyControls(camera, renderer.domElement);
flyControls.movementSpeed = 100;
flyControls.rollSpeed = Math.PI / 24;
flyControls.autoForward = false;
flyControls.dragToLook = false;
```

## 3D模型规范

### 模型格式
- **推荐**: GLTF/GLB (Web优化)
- **支持**: OBJ, FBX, DAE
- **纹理**: PNG, JPEG, WebP

### 模型要求
- **面数**: 单个模型 < 100k 三角面
- **纹理**: 分辨率 < 2048x2048
- **动画**: 关键帧动画 < 100帧
- **文件大小**: < 50MB

### 模型优化
```bash
# 使用gltf-pipeline优化
npx gltf-pipeline -i model.glb -o model-optimized.glb

# 使用draco压缩
npx gltf-pipeline -i model.glb -o model-draco.glb --draco.compressionLevel=7
```

## 场景配置

### 场景文件格式
```json
{
  "name": "全球物流网络",
  "description": "全球物流控制塔3D场景",
  "camera": {
    "position": { "x": 0, "y": 1000, "z": 2000 },
    "target": { "x": 0, "y": 0, "z": 0 }
  },
  "lights": [
    {
      "type": "directional",
      "position": { "x": 100, "y": 100, "z": 100 },
      "intensity": 1.0,
      "color": "#ffffff"
    }
  ],
  "objects": [
    {
      "id": "warehouse-beijing",
      "type": "warehouse",
      "model": "models/warehouse.glb",
      "position": { "x": 116.3974, "y": 0, "z": 39.9093 },
      "scale": { "x": 1, "y": 1, "z": 1 }
    }
  ]
}
```

## 性能优化

### 渲染优化
```typescript
// 使用LOD (Level of Detail)
const lod = new THREE.LOD();
for (let i = 0; i < 5; i++) {
  const distance = i * 100;
  const model = createModelWithDetail(i);
  lod.addLevel(model, distance);
}

// 使用实例化
const instanceGeometry = new THREE.InstancedBufferGeometry();
const instanceMaterial = new THREE.MeshBasicMaterial();
const instancedMesh = new THREE.InstancedMesh(
  instanceGeometry,
  instanceMaterial,
  instanceCount
);

// 使用视锥剔除
const frustum = new THREE.Frustum();
const projScreenMatrix = new THREE.Matrix4();
projScreenMatrix.multiplyMatrices(
  camera.projectionMatrix,
  camera.matrixWorldInverse
);
frustum.setFromProjectionMatrix(projScreenMatrix);
```

### 内存优化
```typescript
// 释放资源
function disposeObject(object: THREE.Object3D) {
  if (object instanceof THREE.Mesh) {
    object.geometry.dispose();
    if (Array.isArray(object.material)) {
      object.material.forEach(material => material.dispose());
    } else {
      object.material.dispose();
    }
  }
  object.children.forEach(child => disposeObject(child));
}

// 使用对象池
class ObjectPool {
  private pool: THREE.Object3D[] = [];
  
  get(): THREE.Object3D {
    return this.pool.pop() || this.createObject();
  }
  
  release(object: THREE.Object3D) {
    this.pool.push(object);
  }
}
```

## 数据集成

### 实时数据流
```typescript
// WebSocket连接
const ws = new WebSocket('ws://localhost:8000/ws/vehicles');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateVehicles(data.vehicles);
};

// REST API轮询
async function fetchVehicles() {
  const response = await fetch('/api/v1/vehicles');
  const data = await response.json();
  updateVehicles(data.vehicles);
}
```

### 地理空间数据
```typescript
// 加载GeoJSON
const geojsonData = await fetch('data/routes.geojson').then(r => r.json());
const geojson = new Cesium.GeoJsonDataSource();
await geojson.load(geojsonData);
viewer.dataSources.add(geojson);

// 加载KML
const kml = new Cesium.KmlDataSource();
await kml.load('data/placemarks.kml');
viewer.dataSources.add(kml);
```

## 示例代码

### 基础示例
```html
<!DOCTYPE html>
<html>
<head>
  <title>数字孪生示例</title>
  <style>
    #container {
      width: 100%;
      height: 100vh;
    }
  </style>
</head>
<body>
  <div id="container"></div>
  <script type="module">
    import { LogisticsScene } from './src/core/scene.js';
    
    const scene = new LogisticsScene({
      container: 'container',
    });
    
    // 添加车辆
    scene.addVehicle({
      id: 'truck-001',
      model: 'models/truck.glb',
      position: { x: 0, y: 0, z: 0 },
    });
    
    // 动画循环
    function animate() {
      requestAnimationFrame(animate);
      scene.update();
      scene.render();
    }
    
    animate();
  </script>
</body>
</html>
```

## 故障排除

### 常见问题

1. 模型不显示
   - 检查模型路径
   - 检查模型格式
   - 检查WebGL支持

2. 性能问题
   - 减少模型面数
   - 使用LOD技术
   - 优化纹理大小

3. 内存泄漏
   - 及时释放资源
   - 使用对象池
   - 监控内存使用

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 致谢

本模块基于DigitalTwinScreen项目，感谢开源社区的贡献。

- DigitalTwinScreen仓库: https://github.com/tmqq2333/DigitalTwinScreen