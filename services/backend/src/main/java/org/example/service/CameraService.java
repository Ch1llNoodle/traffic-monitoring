package org.example.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import org.example.entity.Camera;

public interface CameraService {
    Page<Camera> pageCamera(Integer current, Integer size, String name, String location, Integer status);
    Camera getCameraById(Long id);
    void createCamera(Camera camera);
    void updateCamera(Camera camera);
    void deleteCamera(Long id);
    void updateCameraStatus(Long id, Integer status);
}
