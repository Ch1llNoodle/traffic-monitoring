package org.example.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.example.entity.Camera;
import org.example.mapper.CameraMapper;
import org.example.service.CameraService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class CameraServiceImpl implements CameraService {

    @Autowired
    private CameraMapper cameraMapper;

    @Override
    public Page<Camera> pageCamera(Integer current, Integer size, String name, String location, Integer status) {
        Page<Camera> page = new Page<>(current, size);
        QueryWrapper<Camera> wrapper = new QueryWrapper<>();
        
        if (name != null && !name.trim().isEmpty()) {
            wrapper.like("name", name);
        }
        if (location != null && !location.trim().isEmpty()) {
            wrapper.like("location", location);
        }
        if (status != null) {
            wrapper.eq("status", status);
        }
        
        wrapper.orderByDesc("create_time");
        return cameraMapper.selectPage(page, wrapper);
    }

    @Override
    public Camera getCameraById(Long id) {
        return cameraMapper.selectById(id);
    }

    @Override
    public void createCamera(Camera camera) {
        cameraMapper.insert(camera);
    }

    @Override
    public void updateCamera(Camera camera) {
        cameraMapper.updateById(camera);
    }

    @Override
    public void deleteCamera(Long id) {
        cameraMapper.deleteById(id);
    }

    @Override
    public void updateCameraStatus(Long id, Integer status) {
        Camera camera = cameraMapper.selectById(id);
        if (camera != null) {
            camera.setStatus(status);
            cameraMapper.updateById(camera);
        }
    }
}
