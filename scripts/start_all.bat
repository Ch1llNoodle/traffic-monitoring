@echo off
chcp 65001 >nul
title Traffic Monitoring System - 一键启动脚本
echo ============================================================
echo             智慧交通监控系统 - 启动中……
echo ============================================================
:: === 0. 启动 MySQL 数据库 ===
echo [0/7] 启动数据库服务 (MySQL) ...
start cmd /k "mysqld --console"
timeout /t 5 >nul

:: === 1. 前端启动 ===
echo [1/7] 启动前端服务 (Vue) ...
cd .\services\frontend\
start cmd /k "npm run dev"
cd ..\..

:: === 2. 后端启动 ===
echo [2/7] 启动后端服务 (Spring Boot) ...
cd .\services\backend\
start cmd /k "mvn spring-boot:run"
cd ..\..

:: === 3. 算法端启动 ===
echo [3/7] 启动算法端服务 (Flask + YOLO) ...
cd .\services\algorithm\
start "" cmd /k "conda run -n py12 python app.py"
cd ..\..

:: === 4. 文件服务启动 ===
echo [4/7] 启动文件服务 ...
cd .\services\storage\
start cmd /k "web-file-service.exe"
cd ..\..

:: === 5. 启动流媒体服务 ===
echo [5/7] 启动流媒体服务 (mediamtx) ...
cd .\other\camera\streaming-media-server
start cmd /k "mediamtx.exe"
cd ..\..\..

:: === 6. 启动模拟监控视频流 ===
echo [6/7] 启动模拟视频流 ...
cd .\other\camera\video
start cmd /k "ffmpeg -re -stream_loop -1 -i video_1.mp4 -vf scale=640:480 -f rtsp rtsp://localhost:8554/test_video_1"
start cmd /k "ffmpeg -re -stream_loop -1 -i video_2.mp4 -vf scale=640:480 -f rtsp rtsp://localhost:8554/test_video_2"
cd ..\..\..

:: === 7. 打开浏览器访问前端 ===
echo [7/7] 启动完成，正在打开系统首页...
start "" "http://localhost:3000/"

echo ============================================================
echo 所有服务已启动！请在浏览器访问：
echo http://localhost:3000/
echo ============================================================
pause
