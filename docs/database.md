# 数据库设计文档

本系统使用 MySQL 8.0 数据库，采用 `utf8mb4` 字符集，包含以下核心表：

## 1. 用户表 (`user`)

用于管理系统用户与权限。

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

## 2. 摄像头设备表 (`camera`)

记录各监控点信息及 RTSP 连接地址。

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

## 3. 检测记录表 (`detection_record`)

存储 AI 检测产生的结构化数据与关联影像信息。

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
