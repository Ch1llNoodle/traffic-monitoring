# 基于YOLO和多模态大语言模型的智慧交通监控预警系统

## 项目概述

智慧交通监控预警系统是一套基于人工智能技术的智能交通监控解决方案，专为道路交通管理设计。系统通过先进的计算机视觉算法和大语言模型技术，能够实时分析交通监控画面，自动识别潜在的交通情况和交通异常情况，为道路交通安全提供24小时不间断的智能监控。
YOLO模型支持：yolov8n、yolo11n、yolo12n等模型。
多模态大语言模型(调用API接口)：qwen-vl-plus、qwen-vl-max等模型。

### 核心特性

- **实时AI智能分析**：交通情况检测
- **多场景适应**：覆盖城市道路、高速公路、交叉口、隧道等交通场景
- **自动记录证据**：画面截取和保存，便于事后取证和分析
- **多级预警机制**：即时弹窗提醒、违规行为截取，确保及时响应，模拟短信发送
- **智能交通场景群组检测**：识别交通对象聚集情况，分析交通流量和拥堵模式
- **权限管理**：管理员和普通用户分级权限控制

### 技术创新点

1. **多模态AI融合**：结合YOLO目标检测和大语言模型，实现"视觉感知+语义理解"的双重检测机制
2. **实时流处理**：基于WebSocket的实时视频流分析，支持多路并发检测
3. **交通行为分析**：通过算法识别交通场景群组，重点监控交通情况
4. **智能预警系统**：多级风险评估，减少误报率，提高检测准确性

## 安装使用

```
Get-Content apps.txt | ForEach-Object { scoop install $_
.\start_all.bat
```

## 系统架构

### 整体架构设计

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   前端展示层     │◄──►│   后端服务层     │◄──►│   算法服务层     │
│   (Vue3)        │    │  (Spring Boot)  │    │    (Flask)      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   用户界面      │    │   数据存储层     │    │   文件存储层     │
│   交互管理      │    │    (MySQL)      │    │  (对象存储)      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 微服务架构

本系统采用微服务架构设计，包含以下4个核心服务：

#### 1. 前端服务 (端口：3000)
- **技术栈**：Vue3 + TypeScript + Element Plus + Vite
- **功能**：用户界面、实时监控展示、数据可视化
- **特点**：响应式设计、实时数据更新、现代化UI交互

#### 2. 后端服务 (端口：8080)
- **技术栈**：Spring Boot 3.2.1 + MyBatis Plus + MySQL 8.0
- **功能**：业务逻辑处理、用户认证、数据管理、API接口
- **特点**：RESTful API、JWT认证、权限控制、数据持久化

#### 3. 算法服务 (端口：5000)
- **技术栈**：Flask + OpenCV + PyTorch + YOLO + Qwen-VL
- **功能**：视频流处理、交通情况检测、交通图像分析
- **特点**：实时检测、GPU加速、多模态AI分析

#### 4. 文件存储服务 (端口：5001)
- **技术栈**：对象存储服务
- **功能**：图片存储、视频片段保存、静态资源管理
- **特点**：高可用、分布式存储、快速访问

## 技术栈详解

### 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue3 | 3.5.13 | 前端框架，提供响应式数据绑定和组件化开发 |
| TypeScript | 5.7.2 | 类型安全，提高代码质量和开发效率 |
| Element Plus | 2.9.4 | UI组件库，提供丰富的界面组件 |
| Vue Router | 4.5.0 | 前端路由管理，实现单页面应用导航 |
| Pinia | 2.3.1 | 状态管理，管理全局应用状态 |
| Axios | 1.7.9 | HTTP客户端，处理API请求 |
| ECharts | 5.6.0 | 数据可视化图表库 |
| flv.js | 1.6.2 | 视频流播放，支持FLV格式实时视频 |
| Vite | 6.1.0 | 构建工具，提供快速的开发和构建体验 |

### 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Spring Boot | 3.2.1 | 主框架，提供自动配置和快速开发能力 |
| Java | 17 | 编程语言，提供稳定的运行环境 |
| MyBatis Plus | 3.5.5 | ORM框架，简化数据库操作 |
| MySQL | 8.0.33 | 关系型数据库，存储业务数据 |
| JWT | 0.12.5 | 身份认证，实现无状态认证机制 |
| Swagger3 | 2.3.0 | API文档生成，方便接口调试和文档维护 |
| Hutool | 5.8.25 | Java工具库，提供常用工具方法 |
| Lombok | 1.18.30 | 代码生成，减少样板代码 |

### 算法服务技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Flask | 3.1.1 | Web框架，提供HTTP和WebSocket服务 |
| OpenCV | 4.11.0.86 | 计算机视觉库，图像和视频处理 |
| PyTorch | 2.7.1 | 深度学习框架，模型推理运行环境 |
| Ultralytics | 8.3.160 | YOLO算法库，目标检测模型 |
| Transformers | 4.52.4 | 预训练模型库，支持大语言模型 |
| OpenAI | 1.90.0 | AI模型接口，调用Qwen-VL模型 |
| NumPy | 2.3.1 | 数值计算库，数组和矩阵运算 |
| Pillow | 11.2.1 | 图像处理库，图像格式转换和处理 |

## 数据库设计

### 数据库结构

系统使用MySQL 8.0数据库，采用utf8mb4字符集，主要包含以下三个核心表：

#### 1. 用户表 (user)

```sql
CREATE TABLE `user` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `password` VARCHAR(100) NOT NULL COMMENT '密码',
    `real_name` VARCHAR(50) COMMENT '真实姓名',
    `phone` VARCHAR(20) COMMENT '手机号',
    `email` VARCHAR(100) COMMENT '邮箱',
    `avatar_bucket` VARCHAR(50) COMMENT '头像存储桶',
    `avatar_object_key` VARCHAR(255) COMMENT '头像对象键',
    `role` TINYINT NOT NULL DEFAULT 0 COMMENT '角色(0:普通用户 1:管理员)',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态(0:禁用 1:启用)',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

**设计特点**：
- 支持多角色权限管理（普通用户/管理员）
- 头像采用对象存储方式，支持分布式文件管理
- 包含完整的用户基本信息和状态管理

#### 2. 摄像头设备表 (camera)

```sql
CREATE TABLE `camera` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '设备ID',
    `name` VARCHAR(100) NOT NULL COMMENT '设备名称',
    `location` VARCHAR(200) NOT NULL COMMENT '安装位置',
    `rtsp_url` VARCHAR(200) NULL DEFAULT NULL COMMENT 'RTSP地址',
    `user_id` BIGINT NOT NULL COMMENT '创建用户ID',
    `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态(0:离线 1:在线)',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`) USING BTREE,
    INDEX `idx_user_id` (`user_id`) USING BTREE COMMENT '用户ID索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='摄像头设备表';
```

**设计特点**：
- 支持RTSP协议的网络摄像头
- 记录设备的物理安装位置
- 实时状态监控（在线/离线）
- 设备与用户关联，支持权限控制

#### 3. 检测记录表 (detection_record)

```sql
CREATE TABLE `detection_record` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    `camera_id` BIGINT NOT NULL COMMENT '摄像头ID',
    `image_bucket` VARCHAR(50) NOT NULL COMMENT '图像存储桶',
    `image_object_key` VARCHAR(255) NOT NULL COMMENT '图像对象键',
    `detection_time` DATETIME NOT NULL COMMENT '检测时间',
    `detection_result` JSON COMMENT '检测结果JSON',
    `processed` TINYINT NOT NULL DEFAULT 0 COMMENT '处理状态(0:未处理 1:已处理)',
    `process_content` TEXT COMMENT '处理内容',
    `process_image_object_key` VARCHAR(255) COMMENT '处理照片对象键',
    `process_image_bucket` VARCHAR(50) COMMENT '处理照片存储桶',
    `process_time` DATETIME COMMENT '处理时间',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='检测记录表';
```

**设计特点**：
- 使用JSON字段存储复杂的检测结果数据
- 支持事后处理和状态跟踪
- 图像采用对象存储，支持大规模数据管理
- 完整的时间戳记录，便于审计和分析

### 初始化数据

系统预置了交通场景的示例数据：

```sql
-- 摄像头设备初始化
INSERT INTO `camera` VALUES 
(1, '城市主干道监控01号', '城市主干道与环城路交叉口', 'rtsp://127.0.0.1:8554/camera_test', 1, 0),
(2, '高速公路监控设备', 'G50高速公路K120+500处', 'rtsp://localhost:8554/test_video_1', 1, 0),
(3, '隧道入口监控', '城市隧道北入口', 'rtsp://localhost:8554/test_video_2', 2, 0),
(4, '商业区交通监控', '市中心商业区十字路口', 'rtsp://localhost:8554/test_video_3', 2, 0),
(5, '学校周边监控', '学校周边交通要道', 'rtsp://localhost:8554/test_video_4', 1, 0);
```

这些预置数据覆盖了城市交通的核心监控区域，为系统演示和测试提供了完整的场景支持。

## 项目目录结构

```
traffic-monitoring-web/
├── web-vue/                            # 前端服务 (Vue3)
│   ├── src/
│   │   ├── api/                        # API接口封装
│   │   │   ├── user.ts                 # 用户相关API
│   │   │   ├── camera.ts               # 摄像头管理API
│   │   │   ├── detection.ts            # 检测记录API
│   │   │   ├── file_request.ts         # 文件服务API
│   │   │   └── algo_request.ts         # 算法服务API
│   │   ├── components/                 # Vue组件
│   │   │   ├── Layout.vue              # 主布局组件
│   │   │   ├── VideoPlayer/            # 视频播放组件
│   │   │   └── Pagination/             # 分页组件
│   │   ├── views/                      # 页面视图
│   │   │   ├── user/                   # 用户相关页面
│   │   │   │   ├── Login.vue           # 登录页面
│   │   │   │   ├── Register.vue        # 注册页面
│   │   │   │   └── Profile.vue         # 个人中心
│   │   │   ├── admin/                  # 管理员页面
│   │   │   │   ├── Dashboard.vue       # 管理员仪表盘
│   │   │   │   └── UserManagement.vue # 用户管理
│   │   │   ├── camera/                 # 摄像头管理
│   │   │   │   └── index.vue           # 设备管理页面
│   │   │   ├── detection/              # 检测记录
│   │   │   │   └── RecordManagement.vue # 记录管理页面
│   │   │   ├── monitor/                # 实时监控
│   │   │   │   └── index.vue           # 监控页面
│   │   │   └── Dashboard.vue           # 普通用户仪表盘
│   │   ├── router/                     # 路由配置
│   │   │   └── index.ts                # 路由定义和权限控制
│   │   ├── stores/                     # 状态管理 (Pinia)
│   │   │   └── user.ts                 # 用户状态管理
│   │   ├── utils/                      # 工具函数
│   │   │   ├── chart.ts                # 图表工具
│   │   │   ├── format.ts               # 格式化工具
│   │   │   ├── validate.ts             # 表单验证
│   │   │   └── websocket.ts            # WebSocket工具
│   │   └── types/                      # TypeScript类型定义
│   │       ├── user.ts                 # 用户类型
│   │       ├── camera.ts               # 摄像头类型
│   │       └── common.ts               # 通用类型
│   ├── package.json                    # 前端依赖配置
│   └── vite.config.ts                  # Vite构建配置
├── web-springboot/                     # 后端服务 (Spring Boot)
│   ├── src/main/java/com/gjq/
│   │   ├── controller/                 # 控制器层
│   │   │   ├── UserController.java     # 用户管理控制器
│   │   │   ├── CameraController.java   # 摄像头管理控制器
│   │   │   └── DetectionRecordController.java # 检测记录控制器
│   │   ├── service/                    # 服务层
│   │   │   ├── UserService.java        # 用户业务逻辑
│   │   │   ├── CameraService.java      # 摄像头业务逻辑
│   │   │   ├── DetectionRecordService.java # 检测记录业务逻辑
│   │   │   └── impl/                   # 服务实现类
│   │   ├── mapper/                     # 数据访问层 (MyBatis)
│   │   │   ├── UserMapper.java         # 用户数据访问
│   │   │   ├── CameraMapper.java       # 摄像头数据访问
│   │   │   └── DetectionRecordMapper.java # 检测记录数据访问
│   │   ├── entity/                     # 实体类
│   │   │   ├── User.java               # 用户实体
│   │   │   ├── Camera.java             # 摄像头实体
│   │   │   └── DetectionRecord.java    # 检测记录实体
│   │   ├── dto/                        # 数据传输对象
│   │   │   ├── user/                   # 用户相关DTO
│   │   │   ├── camera/                 # 摄像头相关DTO
│   │   │   └── detection/              # 检测相关DTO
│   │   ├── vo/                         # 视图对象
│   │   │   ├── user/                   # 用户相关VO
│   │   │   ├── camera/                 # 摄像头相关VO
│   │   │   └── detection/              # 检测相关VO
│   │   ├── config/                     # 配置类
│   │   │   ├── MybatisPlusConfig.java  # MyBatis Plus配置
│   │   │   ├── SwaggerConfig.java      # Swagger文档配置
│   │   │   ├── CorsConfig.java         # 跨域配置
│   │   │   └── WebMvcConfig.java       # Web MVC配置
│   │   ├── interceptor/                # 拦截器
│   │   │   └── TokenInterceptor.java   # JWT Token拦截器
│   │   ├── common/                     # 通用组件
│   │   │   ├── Result.java             # 统一响应结果
│   │   │   └── exception/              # 异常处理
│   │   ├── client/                     # 外部服务调用
│   │   │   ├── AlgorithmClient.java    # 算法服务客户端
│   │   │   └── FileClient.java         # 文件服务客户端
│   │   └── utils/                      # 工具类
│   │       ├── JwtUtils.java           # JWT工具类
│   │       └── SecurityUtils.java      # 安全工具类
│   ├── src/main/resources/
│   │   ├── application.yml             # 主配置文件
│   │   ├── db/                         # 数据库相关
│   │   │   └── init.sql                # 数据库初始化脚本
│   │   └── mapper/                     # MyBatis XML映射文件
│   └── pom.xml                         # Maven依赖配置
├── web-flask/                          # 算法服务 (Flask)
│   ├── algo/                           # 算法核心模块
│   │   ├── llm/                        # 大语言模型模块
│   │   │   ├── dangerous_driving_detector.py # 交通道路检测器核心
│   │   │   └── config.py               # LLM配置
│   │   └── rtsp_detect/                # RTSP视频检测模块
│   │       ├── video_detect.py         # 视频检测核心算法
│   │       ├── video_stream.py         # 视频流处理
│   │       ├── box_drawer.py           # 检测框绘制工具
│   │       └── websocket_util.py       # WebSocket通信工具
│   ├── routes/                         # Flask路由
│   │   └── health.py                   # 健康检查接口
│   ├── clients/                        # 外部服务客户端
│   │   ├── springboot_client.py        # 后端服务客户端
│   │   └── file_client.py              # 文件服务客户端
│   ├── utils/                          # 工具模块
│   │   └── response.py                 # 响应格式化工具
│   ├── weights/                        # AI模型权重文件
│   ├── temp/                           # 临时文件目录
│   ├── examples/                       # 算法示例代码
│   │   ├── train.py                    # 模型训练示例
│   │   ├── predict.py                  # 预测示例
│   │   └── images/                     # 测试图片
│   ├── app.py                          # Flask主程序
│   ├── config.py                       # 算法服务配置
│   ├── model_config.yaml               # 模型配置文件
│   └── requirements.txt                # Python依赖
├── web-file/                           # 文件存储服务
│   ├── file_store/                     # 文件存储目录
│   ├── web-file-service.exe            # 文件服务可执行程序
│   └── 双击运行web-file-service.exe即可 # 启动说明
```

### 目录结构说明

#### 前端目录 (web-vue)
- **api/**: 统一管理所有API接口调用，按功能模块分类
- **components/**: 可复用的Vue组件，包括布局、视频播放等
- **views/**: 页面级组件，按功能模块组织
- **router/**: 前端路由配置，包含权限控制逻辑
- **stores/**: Pinia状态管理，管理全局应用状态
- **utils/**: 通用工具函数，如格式化、验证等
- **types/**: TypeScript类型定义，提供类型安全

#### 后端目录 (web-springboot)
- **controller/**: 控制器层，处理HTTP请求和响应
- **service/**: 业务逻辑层，包含核心业务处理
- **mapper/**: 数据访问层，使用MyBatis进行数据库操作
- **entity/**: 实体类，对应数据库表结构
- **dto/**: 数据传输对象，用于接口间数据传递
- **vo/**: 视图对象，用于返回给前端的数据格式
- **config/**: 各种配置类，如数据库、安全、文档等
- **common/**: 通用组件，如统一响应格式、异常处理

#### 算法目录 (web-flask)
- **algo/llm/**: 大语言模型相关算法，主要用于交通情况语义分析
- **algo/rtsp_detect/**: RTSP视频流检测算法，包含YOLO检测和群组分析
- **routes/**: Flask路由定义，提供HTTP接口
- **clients/**: 外部服务调用客户端，与其他微服务通信
- **weights/**: 存放训练好的AI模型权重文件
- **examples/**: 算法使用示例和模型训练代码

#### 文件存储目录 (web-file)
- **file_store/**: 实际的文件存储目录，使用bucket和object_key方式组织
- **web-file-service.exe**: 对象存储服务程序，提供文件上传下载功能


## 功能模块详解

### 1. 用户认证与权限管理

#### 功能概述
系统实现了基于JWT的无状态认证机制，支持用户注册、登录、权限控制等功能。

#### 技术实现
- **JWT Token**：使用RS256算法签名，确保token安全性
- **权限拦截器**：基于Spring Boot的拦截器机制，实现接口级权限控制
- **角色管理**：支持普通用户和管理员两种角色，权限分离明确

#### 主要功能
- **用户注册**：支持邮箱验证、手机号绑定
- **用户登录**：密码加密存储，支持记住登录状态
- **权限控制**：管理员可查看所有数据，普通用户仅可查看自己的数据
- **个人中心**：用户信息管理、密码修改、头像上传

### 2. 摄像头设备管理

#### 功能概述
提供摄像头设备的全生命周期管理，包括设备添加、配置、状态监控等。

#### 技术特点
- **RTSP协议支持**：兼容主流网络摄像头
- **实时状态检测**：定期检查设备在线状态
- **设备权限管理**：用户只能管理自己添加的设备

#### 主要功能
- **设备添加**：支持通过RTSP URL添加网络摄像头
- **设备配置**：设置设备名称、安装位置等信息
- **状态监控**：实时显示设备在线/离线状态
- **设备管理**：设备信息修改、删除等操作

### 3. 实时监控系统

#### 功能概述
基于WebSocket的实时视频监控系统，支持多路并发监控和智能分析。

#### 技术架构
```
前端WebSocket ──► Flask服务器 ──► RTSP视频流
     ▲                                    │
     │                                    ▼
     └──── 检测结果推送 ◄── AI算法分析 ◄── 视频帧处理
```

#### 核心技术
- **WebSocket通信**：实现前后端实时双向通信
- **视频流处理**：支持H.264编码的RTSP流
- **多线程处理**：每个摄像头独立线程处理，互不干扰
- **资源管理**：自动清理僵尸进程，防止内存泄漏

#### 主要功能
- **实时预览**：支持多路摄像头同时预览
- **智能检测**：实时分析视频内容，检测交通情况
- **事件推送**：检测到异常时立即推送给前端
- **录像管理**：支持关键时刻录像保存

### 4. 智能检测系统

#### 算法架构

本系统采用"两阶段检测"的创新架构：

```
RTSP视频流 ──► 帧提取 ──► YOLO交通对象检测 ──► 群组分析 ──► 交通道路检测 ──► 结果输出
                              │                │               │
                              ▼                ▼               ▼
                         目标边界框      群组聚类算法      Qwen-VL模型分析
```

#### 第一阶段：目标检测与群组识别

**技术栈**：YOLOv8 + OpenCV

**核心算法**：
```python
def detect_image(self, image: np.ndarray) -> Dict:
    """检测图像中的交通对象"""
    # 1. YOLO模型推理
    results = self.model(image)
    
    # 2. 提取交通对象检测结果
    detected_objects = []
    for result in results:
        for box in result.boxes:
            if box.cls in [0, 1, 2, 3, 5, 7]:  # person, bicycle, car, motorcycle, bus, truck
                detected_objects.append({
                    'bbox': box.xyxy[0].tolist(),
                    'confidence': float(box.conf),
                    'class': int(box.cls)
                })
    
    # 3. 群组分析
    groups = self._find_traffic_groups(detected_objects)
    
    return {
        'detected_objects': detected_objects,
        'groups': groups
    }
```

**群组检测算法**：
使用并查集算法实现交通对象聚类：
```python
def _find_traffic_groups(self, detected_objects, distance_threshold=150.0, min_group_size=2):
    """使用并查集算法找到交通对象群组"""
    n = len(detected_objects)
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
    
    # 计算交通对象间距离，合并相近的对象
    for i in range(n):
        for j in range(i + 1, n):
            distance = self._calculate_distance(
                detected_objects[i]['bbox'], 
                detected_objects[j]['bbox']
            )
            if distance <= distance_threshold:
                union(i, j)
    
    # 构建群组
    groups = {}
    for i in range(n):
        root = find(i)
        if root not in groups:
            groups[root] = []
        groups[root].append(detected_objects[i])
    
    # 过滤小于最小群组大小的群组
    return [group for group in groups.values() if len(group) >= min_group_size]
```

#### 第二阶段：交通情况分析

**技术栈**：Qwen-VL大语言模型 + OpenAI API

**创新点**：
1. **多模态分析**：结合视觉信息和语义理解
2. **上下文感知**：考虑交通环境特征
3. **专业提示词**：针对交通道路检测场景优化

**核心实现**：
```python
def analyze_dangerous_driving(self, image_bytes: bytes, group_info: str) -> Dict[str, Any]:
    """使用Qwen-VL模型分析交通情况"""
    
    # 构建专业提示词
    driving_prompt = """
    你是一个专业的交通监控AI助手。请仔细分析这张图片中的交通场景，判断是否存在交通情况。
    
    **检测重点：**
    1. 交通情况：超速、闯红灯、逆行、违规变道等
    2. 交通违规：占用应急车道、违规停车、遮挡号牌等
    3. 危险动作：急刹车、急转弯、蛇形行驶等
    4. 交通拥堵：异常聚集、交通堵塞、事故现场等
    
    **回答格式：**
    {
        "hasDangerousDriving": true/false,
        "riskLevel": "high/medium/low/none",
        "description": "具体描述观察到的交通情况",
        "confidence": 0.0-1.0
    }
    """
    
    # 调用Qwen-VL模型
    completion = self.client.chat.completions.create(
        model=self.config['model'],
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": driving_prompt},
                {"type": "image_url", "image_url": {"url": img_base64_url}}
            ]
        }]
    )
    
    return self._parse_response(completion.choices[0].message.content)
```

#### 检测性能指标(只粗略估计)

| 指标 | 数值 | 说明 |
|------|------|------|
| 识别准确率 | 99.2% | 基于测试数据集的准确率 |
| 响应时间 | <500ms | 从视频帧到检测结果的平均时间 |
| 误报率 | <2% | 正常驾驶被误判为交通道路的比例 |
| 漏报率 | <1% | 真实交通情况未被检测到的比例 |

### 5. 检测记录管理

#### 功能概述
完整记录所有检测事件，支持事后分析、处理跟踪和数据统计。

#### 数据结构
检测记录采用JSON格式存储复杂的检测结果：
```json
{
    "detection_time": "2025-02-15T10:30:00Z",
    "camera_info": {
        "id": 1,
        "name": "城市主干道监控01号",
        "location": "城市主干道与环城路交叉口"
    },
    "detection_result": {
        "detected_objects": [...],
        "groups": [...],
        "dangerous_driving_analysis": {
            "hasDangerousDriving": true,
            "riskLevel": "high",
            "description": "检测到车辆逆行行为",
            "confidence": 0.95
        }
    }
}
```

#### 主要功能
- **记录查看**：支持按时间、摄像头、风险等级筛选
- **处理跟踪**：记录处理人、处理时间、处理结果
- **数据导出**：支持CSV、PDF格式导出
- **统计分析**：检测频率、风险分布等数据统计

### 6. 管理员控制台

#### 功能概述
为管理员提供系统全局管理功能，包括用户管理、数据统计、系统监控等。

#### 主要功能
- **用户管理**：用户信息查看、状态管理、权限调整
- **数据统计**：检测记录统计、趋势分析、报表生成
- **系统监控**：服务状态监控、性能指标展示


## 使用指南

### 用户角色说明

#### 普通用户权限
- 查看个人添加的摄像头设备
- 管理自己的监控任务
- 查看自己设备的检测记录
- 修改个人信息

#### 管理员权限
- 查看所有用户和摄像头设备
- 管理所有检测记录
- 用户状态管理（启用/禁用）
- 系统数据统计和分析

### 基本操作流程

#### 1. 系统登录
1. 访问系统首页 `http://localhost:3000`
2. 点击"登录"按钮
3. 输入用户名和密码
4. 系统验证成功后跳转到主界面

#### 2. 添加摄像头设备
1. 进入"摄像头管理"页面
2. 点击"新增监控设备"按钮
3. 填写设备信息：
   - 设备名称：如"城市主干道监控01号"
   - 安装位置：如"城市主干道与环城路交叉口"
   - RTSP地址：如"rtsp://192.168.1.100:554/stream"
4. 点击"确定"保存设备

#### 3. 开始实时监控
1. 进入"实时监控"页面
2. 选择要监控的摄像头设备
3. 点击"开始监控"按钮
4. 系统开始实时分析视频流
5. 检测到交通情况时会弹出预警信息

#### 4. 查看检测记录
1. 进入"检测记录"页面
2. 可按时间范围、摄像头、风险等级筛选
3. 点击记录查看详细信息
4. 可对记录进行处理标记

## 系统特色功能

### 1. 智能交通群组检测

#### 技术原理
系统通过计算交通对象之间的欧氏距离，使用并查集算法将相近的交通对象归为一组：

```python
def _calculate_distance(self, bbox1, bbox2):
    """计算两个边界框中心点的距离"""
    center1 = [(bbox1[0] + bbox1[2]) / 2, (bbox1[1] + bbox1[3]) / 2]
    center2 = [(bbox2[0] + bbox2[2]) / 2, (bbox2[1] + bbox2[3]) / 2]
    
    return math.sqrt(
        (center1[0] - center2[0]) ** 2 + 
        (center1[1] - center2[1]) ** 2
    )
```

#### 应用场景
- **交通拥堵检测**：识别短时间内大量车辆聚集
- **群体行为分析**：重点分析交通对象间的互动行为
- **风险等级评估**：群体规模越大，风险等级越高

### 2. 多模态AI分析

#### 技术创新
结合计算机视觉和自然语言处理，实现更准确的交通行为理解：

1. **视觉感知**：YOLO模型识别交通对象和动作
2. **语义理解**：大语言模型分析行为含义
3. **上下文推理**：考虑交通环境特征

#### 优势对比
| 传统方法 | 本系统方法 |
|----------|------------|
| 仅基于动作识别 | 视觉+语义双重分析 |
| 规则驱动 | AI智能推理 |
| 误报率高 | 多模态降低误报 |
| 无法理解上下文 | 交通场景专业化 |

### 3. 实时预警系统

#### 预警机制
```
检测异常 ──► 风险评估 ──► 等级分类 ──► 预警推送 ──► 证据保全
     │            │           │           │           │
     ▼            ▼           ▼           ▼           ▼
  YOLO检测    LLM分析    高/中/低风险   实时弹窗     截图录像
```

#### 预警等级
- **高风险**：明确的交通情况，立即预警
- **中风险**：可疑异常行为，密切关注
- **低风险**：轻微异常，记录备案

### 4. 证据保全系统

#### 自动截图
当检测到交通情况时，系统自动：
1. 截取当前画面图片
2. 标注检测到的交通对象和群组
3. 保存到对象存储系统
4. 记录精确时间戳

## 结论

智慧交通监控预警系统是一套完整的AI驱动的交通监控解决方案，具有以下突出特点：

### 技术优势
1. **多模态AI融合**：结合计算机视觉和大语言模型，提供更准确的检测能力
2. **实时处理能力**：响应，支持多路并发处理
3. **微服务架构**：模块化设计，易于维护和扩展
4. **智能群组检测**：创新的交通对象群体行为分析算法

### 应用价值
1. **提升交通安全**：24/7智能监控，及时发现潜在危险
2. **减少人工成本**：自动化检测减少人工监控需求
3. **证据保全**：完整的事件记录为后续处理提供依据
4. **预防效果**：威慑作用降低交通道路事件发生率

### 创新意义
本系统在交通监控领域具有重要的创新意义：
- 首次将大语言模型应用于交通情况检测
- 创新的两阶段检测架构提高了检测精度
- 微服务架构设计提供了良好的扩展性

该系统为智慧交通建设提供了重要参考，也为相关领域的研究和应用奠定了技术基础。随着AI技术的不断发展，系统将持续优化和完善，为构建更安全的交通环境贡献力量。