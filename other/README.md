# 辅助资源说明

本目录 (`other/`) 存放非核心微服务的辅助工具与测试资源，主要用于开发和调试。

## 目录结构

```text
other/
└── camera/                         # 摄像头模拟与测试资源
    ├── streaming-media-server/     # RTSP 流媒体服务器 (MediaMTX)
    └── video/                      # 测试用视频片段
```

## 功能说明

### 1. RTSP 流媒体服务器 (`streaming-media-server/`)
该目录包含用于测试的 RTSP 服务器程序及其配置文件。
- **程序**: `mediamtx.exe` (MediaMTX)
- **配置**: `mediamtx.yml`

*注意：此服务用于在本地模拟摄像头 RTSP 推流，供算法服务进行读取测试。*

### 2. 测试视频片段 (`video/`)
存放用于交通检测算法测试的视频样本文件。这些文件可通过 `mediamtx` 配置映射为 RTSP 流供系统调用。
- `video_1.mp4` - `video_4.mp4`：预置的交通场景录像。

---

## 使用指南

如需在开发环境启用模拟摄像头流：
1. 启动 `mediamtx.exe`。
2. 确保 `mediamtx.yml` 中正确配置了对应的视频源路径。
3. 算法服务即可通过配置的 RTSP 地址（如 `rtsp://localhost:8554/<stream_name>`）连接到测试视频流。
