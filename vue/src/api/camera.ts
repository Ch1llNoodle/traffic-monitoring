import {request} from './request'
import type {
  Camera,
  CameraQueryParams,
  CameraListResult,
  CameraCreateParams,
  CameraUpdateParams,
} from '@/types/camera'

// 获取摄像头列表
export const getCameraList = (params: CameraQueryParams) => {
  return request.get<CameraListResult>('/camera/page', { params })
}

// 获取摄像头详情
export const getCameraById = (id: number) => {
  return request.get<Camera>(`/camera/${id}`)
}

// 创建摄像头
export const createCamera = (data: CameraCreateParams) => {
  return request.post<number>('/camera', data)
}

// 更新摄像头
export const updateCamera = (data: CameraUpdateParams) => {
  return request.put('/camera', data)
}

// 删除摄像头
export const deleteCamera = (id: number) => {
  return request.delete(`/camera/${id}`)
}

// 更新摄像头状态
export const updateCameraStatus = (id: number, status: number) => {
  return request.put<void>(`/camera/${id}/status`, { status })
} 