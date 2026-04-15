-- 外运物流控制塔 - 数据库初始化脚本（不使用TimescaleDB）

-- 创建数据库
CREATE DATABASE logistics_control_tower;

-- 连接到数据库
\c logistics_control_tower;

-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 车辆表
CREATE TABLE vehicles (
    id VARCHAR(20) PRIMARY KEY,
    plate_number VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type VARCHAR(20) NOT NULL, -- truck, ship, plane, train
    capacity DECIMAL(10, 2) NOT NULL,
    current_lat DECIMAL(10, 6),
    current_lng DECIMAL(10, 6),
    status VARCHAR(20) DEFAULT 'idle', -- idle, active, maintenance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 仓库表
CREATE TABLE warehouses (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(50),
    lat DECIMAL(10, 6),
    lng DECIMAL(10, 6),
    capacity DECIMAL(10, 2) NOT NULL,
    current_load DECIMAL(10, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 订单表
CREATE TABLE orders (
    id VARCHAR(20) PRIMARY KEY,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    cargo_type VARCHAR(50),
    weight DECIMAL(10, 2),
    volume DECIMAL(10, 2),
    priority VARCHAR(20) DEFAULT 'normal', -- low, normal, high, urgent
    status VARCHAR(20) DEFAULT 'pending', -- pending, processing, in_transit, delivered, cancelled
    vehicle_id VARCHAR(20) REFERENCES vehicles(id),
    estimated_delivery TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 位置追踪表 (时序数据)
CREATE TABLE vehicle_locations (
    time TIMESTAMPTZ NOT NULL,
    vehicle_id VARCHAR(20) NOT NULL,
    lat DECIMAL(10, 6) NOT NULL,
    lng DECIMAL(10, 6) NOT NULL,
    speed DECIMAL(5, 2),
    heading DECIMAL(5, 2)
);

-- 创建索引
CREATE INDEX idx_vehicles_status ON vehicles(status);
CREATE INDEX idx_vehicles_type ON vehicles(vehicle_type);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_priority ON orders(priority);
CREATE INDEX idx_orders_vehicle ON orders(vehicle_id);
CREATE INDEX idx_warehouses_city ON warehouses(city);

-- 插入示例数据
INSERT INTO vehicles (id, plate_number, vehicle_type, capacity, current_lat, current_lng, status) VALUES
('V001', '京A12345', 'truck', 10, 39.9042, 116.4074, 'active'),
('V002', '沪B54321', 'truck', 15, 31.2304, 121.4737, 'active'),
('V003', 'SHIP001', 'ship', 1000, 22.5431, 114.0579, 'active');

INSERT INTO warehouses (id, name, address, city, lat, lng, capacity, current_load) VALUES
('WH001', '北京中央仓库', '大兴区物流园区', '北京', 39.9042, 116.4074, 10000, 7500),
('WH002', '上海分拨中心', '浦东新区自贸区', '上海', 31.2304, 121.4737, 15000, 12000),
('WH003', '广州南部中心', '白云区物流港', '广州', 23.1291, 113.2644, 8000, 5600);

INSERT INTO orders (id, origin, destination, cargo_type, weight, priority, status) VALUES
('ORD001', '北京仓库', '上海客户', '电子产品', 500, 'high', 'in_transit'),
('ORD002', '广州仓库', '深圳客户', '服装', 200, 'normal', 'processing'),
('ORD003', '成都仓库', '重庆客户', '食品', 300, 'urgent', 'pending');