package org.example.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.example.common.result.Result;
import org.example.entity.Camera;
import org.example.service.CameraService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * 摄像头控制器
 */
@RestController
@RequestMapping("/camera")
public class CameraController {
    
    @Autowired
    private CameraService cameraService;
    
    /**
     * 分页查询摄像头
     */
    @GetMapping("/page")
    public Result<Page<Camera>> pageCamera(
            @RequestParam(defaultValue = "1") Integer current,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String location,
            @RequestParam(required = false) Integer status) {
        
        return Result.success(cameraService.pageCamera(current, size, name, location, status));
    }
    
    /**
     * 获取摄像头详情
     */
    @GetMapping("/{id}")
    public Result<Camera> getCameraById(@PathVariable Long id) {
        Camera camera = cameraService.getCameraById(id);
        if (camera == null) {
            return Result.error("摄像头不存在");
        }
        return Result.success(camera);
    }
    
    /**
     * 创建摄像头
     */
    @PostMapping
    public Result<Long> createCamera(@RequestBody Camera camera) {
        cameraService.createCamera(camera);
        return Result.success(camera.getId());
    }
    
    /**
     * 更新摄像头
     */
    @PutMapping
    public Result<Void> updateCamera(@RequestBody Camera camera) {
        Camera existCamera = cameraService.getCameraById(camera.getId());
        if (existCamera == null) {
            return Result.error("摄像头不存在");
        }
        cameraService.updateCamera(camera);
        return Result.success();
    }
    
    /**
     * 删除摄像头
     */
    @DeleteMapping("/{id}")
    public Result<Void> deleteCamera(@PathVariable Long id) {
        Camera camera = cameraService.getCameraById(id);
        if (camera == null) {
            return Result.error("摄像头不存在");
        }
        cameraService.deleteCamera(id);
        return Result.success();
    }
    
    /**
     * 更新摄像头状态
     */
    @PutMapping("/{id}/status")
    public Result<Void> updateCameraStatus(@PathVariable Long id, @RequestBody Map<String, Integer> params) {
        Camera camera = cameraService.getCameraById(id);
        if (camera == null) {
            return Result.error("摄像头不存在");
        }
        
        cameraService.updateCameraStatus(id, params.get("status"));
        
        return Result.success();
    }
}