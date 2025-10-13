<template>
  <div class="video-player" @click="handleClick">
    <div class="video-container" ref="videoContainer">
      <canvas ref="canvas" :width="width" :height="height"></canvas>
      
      <!-- 通用目标检测框 -->
      <template v-for="(obj, index) in detectedObjects" :key="index">
        <div 
          class="detection-box" 
          :class="{ 'tracking-box': isTrackingEnabled && obj.trackId !== undefined }"
          :style="getBoxStyle(obj.bbox, obj.class)"
          @click.stop="handleObjectClick(obj)"
        >
          <span class="confidence" :style="getLabelStyle(obj.bbox, obj.class)">
            {{ obj.class }} {{ (obj.confidence * 100).toFixed(0) }}%
            <span v-if="getTrackId(obj)" class="track-id">#{{ getTrackId(obj) }}</span>
          </span>
        </div>
      </template>
    </div>
    
    <!-- 摄像头信息 -->
    <div class="camera-info">
      <span class="name">{{ camera.name }}</span>
      <span class="status" :class="camera.status === 1 ? 'online' : 'offline'">
        {{ camera.status === 1 ? '在线' : '离线' }}
      </span>
    </div>
    
    <!-- 检测警告 -->
    <div v-if="hasDetectionAlert" class="detection-alert-overlay" :class="{ 'alert-active': hasDetectionAlert }">
      <!-- 警告容器，应用缩放样式 -->
      <div class="alert-container" :style="alertScaleStyle">
        <!-- 警告图标 -->
        <div class="alert-icon">
          <el-icon><Warning /></el-icon>
        </div>
        
        <!-- 警告信息 -->
        <div class="alert-info">
          <div class="alert-title">
            <span class="warning-text">智慧交通行为检测</span>
            <el-tag :type="getViolenceRiskType(maxRiskLevel)" size="small" class="level-tag">
              风险等级：{{ getViolenceRiskText(maxRiskLevel) }}
            </el-tag>
          </div>
          <div class="alert-details">
            <div class="detail-item">
              <span class="label">位置：</span>
              <span class="value">{{ camera.location || '未知位置' }}</span>
            </div>
                         <div v-for="(result, index) in dangerousDrivingResults" :key="index" class="detail-item">
               <span class="label">交通场景群组{{ result.groupIndex }}：</span>
              <span class="value">
                {{ result.description }}
                <el-tag :type="getViolenceRiskType(result.riskLevel)" size="small" class="ms-2">
                  {{ getViolenceRiskText(result.riskLevel) }}
                </el-tag>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 群组图片显示区域 -->
    <div v-if="groupImages.length > 0" class="group-images-panel" @click.stop>
      <div class="panel-header">
        <span class="panel-title">
          <el-icon><PictureRounded /></el-icon>
          群组截图 ({{ groupImages.length }})
        </span>
        <el-button 
          type="primary" 
          size="small" 
          text 
          @click.stop="toggleGroupImagesPanel"
          class="toggle-btn"
        >
          <el-icon><CaretBottom v-if="groupImagesPanelExpanded" /><CaretRight v-else /></el-icon>
        </el-button>
      </div>
      <div v-show="groupImagesPanelExpanded" class="panel-content">
        <div class="group-images-grid">
          <div 
            v-for="(groupImage, index) in groupImages" 
            :key="index"
            class="group-image-item"
            @click.stop="previewGroupImage(groupImage, index)"
          >
            <div class="image-wrapper">
              <img
                v-if="groupImage.imageBase64"
                :src="`data:image/jpeg;base64,${groupImage.imageBase64}`"
                :alt="`群组${groupImage.groupIndex}`"
                class="group-image"
                @error="handleImageError"
              />
              <div v-else class="image-placeholder">
                <el-icon><Picture /></el-icon>
                <span>无图片</span>
              </div>
            </div>
            <div class="image-label">
              <span class="group-title">群组{{ groupImage.groupIndex }}</span>
              <span v-if="groupImage.bbox" class="bbox-info">
                {{ formatGroupBbox(groupImage.bbox) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import type { Camera } from '@/types/camera'
import wsClient from '@/utils/websocket'
import type { WebSocketMessage } from '@/utils/websocket'
import { ElMessage } from 'element-plus'
import { addDetectionRecord } from '@/api/detection'
import { 
  Warning, 
  PictureRounded, 
  CaretBottom, 
  CaretRight, 
  Picture 
} from '@element-plus/icons-vue'

const props = defineProps<{
  camera: Camera
  isActive: boolean
  serverDrawEnabled?: boolean
  width?: number
  height?: number
}>()

const emit = defineEmits<{
  (e: 'click', camera: Camera): void
}>()

const router = useRouter()
const hasDetectionAlert = ref(false)

// 组件状态
const canvas = ref<HTMLCanvasElement | null>(null)
const ctx = ref<CanvasRenderingContext2D | null>(null)
const videoContainer = ref<HTMLDivElement | null>(null)
const detectedObjects = ref<any[]>([])
const frameCount = ref(0)  // 添加帧计数器
const classColors = ref<Record<string, string>>({}) // 类别颜色配置
const isTrackingEnabled = ref(false) // 是否启用了跟踪功能

// 危险驾驶检测相关状态
const hasDangerousDriving = ref(false) // 是否检测到危险驾驶行为
const dangerousDrivingResults = ref<any[]>([]) // 危险驾驶检测结果
const maxRiskLevel = ref('none') // 最高风险等级
const trafficGroups = ref<any[]>([]) // 交通场景群组信息
const groupImages = ref<any[]>([]) // 群组图片base64数组
const groupImagesPanelExpanded = ref(true) // 群组图片面板是否展开
const currentDrawArea = ref<{ x: number; y: number; width: number; height: number } | null>(null)
// 添加存储实际图像尺寸的变量
const actualImageWidth = ref(0)
const actualImageHeight = ref(0)
// 添加存储检测对象信息的变量，用于显示警告信息，即使serverDrawEnabled为true
const detectionInfo = ref<any[]>([])
// 存储ResizeObserver清理函数
let cleanupResizeObserver: (() => void) | undefined = undefined

  // 计算是否有危险驾驶行为（用于警告显示）
const hasDangerousDrivingAlert = computed(() => {
  return hasDangerousDriving.value && dangerousDrivingResults.value.length > 0
})

// 存储是否已经保存了当前的检测记录，避免重复保存
const alreadySaved = ref(false)

// 保存检测记录
const saveDetectionRecord = async () => {
  try {
          // 如果没有检测到危险驾驶行为或已经保存过，则不保存
    if (!hasDangerousDriving.value || alreadySaved.value) {
      return
    }
    
    // 将canvas转换为base64图像
    const imageBase64 = canvas.value?.toDataURL('image/jpeg').split(',')[1]
    if (!imageBase64) {
      console.error('获取图像数据失败')
      return
    }
    
    // 验证base64字符串是否有效
    if (!isValidBase64(imageBase64)) {
      console.error('生成的base64图像数据无效，无法保存检测记录')
      return
    }
    
                try {
      // 保存检测记录，包含危险驾驶检测结果和相关信息
      await addDetectionRecord({
        cameraId: props.camera.id,
        imageBase64,
        detectionResult: JSON.stringify({
          detectedObjects: detectionInfo.value,
          dangerousDrivingResults: dangerousDrivingResults.value,
          hasDangerousDriving: hasDangerousDriving.value,
          maxRiskLevel: maxRiskLevel.value,
          trafficGroups: trafficGroups.value,
          groupImages: groupImages.value, // 包含群组图片base64数组
          timestamp: new Date().toISOString()
        })
      })
      
      alreadySaved.value = true
    } catch (apiError) {
      console.error('API调用保存检测记录失败:', apiError)
    }
  } catch (error) {
    console.error('保存检测记录失败:', error)
  }
}

// 默认尺寸
const width = props.width || 640
const height = props.height || 480

// 添加一个响应式变量存储容器尺寸
const containerSize = ref({ width: 0, height: 0 })

// 使用ResizeObserver监听容器尺寸变化
const setupResizeObserver = () => {
  if (!videoContainer.value) return
  
  try {
    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        // 更新容器尺寸
        containerSize.value = {
          width: entry.contentRect.width,
          height: entry.contentRect.height
        }
      }
    })
    
    // 开始观察
    resizeObserver.observe(videoContainer.value)
    
    // 返回清理函数
    return () => {
      resizeObserver.disconnect()
    }
  } catch (error) {
    console.error('ResizeObserver不可用:', error)
    return () => {}
  }
}

// 警告信息框样式缩放计算
const alertScaleStyle = computed(() => {
  if (!videoContainer.value) return {}
  
  // 使用当前容器尺寸或最新的响应式容器尺寸
  const containerWidth = containerSize.value.width || videoContainer.value.clientWidth
  const containerHeight = containerSize.value.height || videoContainer.value.clientHeight
  
  // 以标准尺寸为基准（假设1宫格的标准宽度为800px）
  const baseWidth = 800
  
  // 根据容器宽度计算缩放比例
  let scale = Math.max(0.5, Math.min(1, containerWidth / baseWidth))
  
  // 根据容器高度进一步调整缩放比例
  if (containerHeight < 300) {
    scale = Math.min(scale, 0.7) // 对于高度较小的容器，进一步降低缩放比例
  }
  
  // 返回transform样式
  return {
    transform: `scale(${scale})`,
    transformOrigin: 'center center'
  }
})

// 清除画面和检测框
const clearDisplay = () => {
  // 清除画布
  if (ctx.value) {
    ctx.value.fillStyle = '#000'  // 设置为黑色背景
    ctx.value.fillRect(0, 0, width, height)  // 填充整个画布
  }
  // 清除检测框和绘制区域
  detectedObjects.value = []
  detectionInfo.value = [] // 同时清除检测信息
  currentDrawArea.value = null
      // 重置危险驾驶检测状态
      hasDangerousDriving.value = false
      dangerousDrivingResults.value = []
  maxRiskLevel.value = 'none'
      trafficGroups.value = []
  groupImages.value = []
  // 重置图像尺寸信息
  actualImageWidth.value = 0
  actualImageHeight.value = 0
  // 重置帧计数
  frameCount.value = 0
  // 隐藏警告
  hasDetectionAlert.value = false
}

// 处理点击事件
const handleClick = () => {
  emit('click', props.camera)
}

  // 获取危险驾驶风险等级类型
const getViolenceRiskType = (riskLevel: string): 'success' | 'warning' | 'info' | 'danger' | 'primary' => {
  switch (riskLevel) {
    case 'none':
      return 'info'     // 无风险
    case 'low':
      return 'success'  // 低风险
    case 'medium':
      return 'warning'  // 中等风险
    case 'high':
      return 'danger'   // 高风险
    default:
      return 'info'
  }
}

  // 格式化危险驾驶风险等级
const getViolenceRiskText = (riskLevel: string): string => {
  const levels: Record<string, string> = {
    'none': '无风险',
    'low': '低风险',
    'medium': '中等风险',
    'high': '高风险'
  }
  return levels[riskLevel] || '未知'
}

// 处理WebSocket消息
const handleMessage = (message: WebSocketMessage) => {
  if (message.data.cameraId !== props.camera.id) return

  // 处理通用检测结果
  if (message.type === 'detection_result') {
    // 检查是否启用了跟踪功能
    isTrackingEnabled.value = !!message.data.trackingEnabled
    
    frameCount.value++
    
    // 暂存检测对象和颜色配置，用于前端绘制或显示对象信息
    const receivedObjects = message.data.detectedObjects || []
    const receivedColors = message.data.classColors
    
    // 从后端数据中获取图像尺寸
    if (message.data.imageWidth && message.data.imageHeight) {
      actualImageWidth.value = message.data.imageWidth
      actualImageHeight.value = message.data.imageHeight
    } else {
      // 如果没有图像尺寸信息，清空检测对象，避免定位错误
      detectedObjects.value = []
      detectionInfo.value = []
      return
    }
    
    // 如果有图像，更新画布
    if (message.data.frame && typeof message.data.frame === 'string') {
      // 验证base64图像数据是否有效
      if (!isValidBase64(message.data.frame)) {
        console.error('收到无效的base64图像数据')
        return
      }
      
      const image = new Image()
      image.onload = () => {
        if (ctx.value) {
          // 先清除画布
          ctx.value.clearRect(0, 0, width, height)
          
          // 计算保持宽高比的绘制区域
          const drawArea = calculateDrawArea(actualImageWidth.value, actualImageHeight.value, width, height)
          
          // 根据计算的区域绘制图像
          ctx.value.drawImage(
            image, 
            drawArea.x, drawArea.y, 
            drawArea.width, drawArea.height
          )
          
          // 保存绘制区域信息，用于检测框定位
          currentDrawArea.value = drawArea
          
          // 始终保存检测对象信息，用于警告显示
          detectionInfo.value = receivedObjects
          
          // 如果serverDrawEnabled为true，服务器已经绘制了检测框，前端不需要再绘制
          detectedObjects.value = props.serverDrawEnabled ? [] : receivedObjects
          
          // 更新类别颜色配置
          if (receivedColors) {
            classColors.value = receivedColors
          }
          
          // 更新危险驾驶检测信息
          if (message.data.dangerousDrivingResults) {
            dangerousDrivingResults.value = message.data.dangerousDrivingResults
          }
          if (message.data.hasDangerousDriving !== undefined) {
            hasDangerousDriving.value = message.data.hasDangerousDriving
          }
          if (message.data.maxRiskLevel) {
            maxRiskLevel.value = message.data.maxRiskLevel
          }
          if (message.data.trafficGroups) {
            trafficGroups.value = message.data.trafficGroups
          }
          if (message.data.groupImages) {
            groupImages.value = message.data.groupImages
          }
          
          // 显示检测警告（如果检测到危险驾驶行为）
          hasDetectionAlert.value = hasDangerousDriving.value
          
          // 如果检测到危险驾驶行为，保存检测记录
          if (hasDangerousDriving.value) {
            // 重置保存状态
            alreadySaved.value = false
            // 保存检测记录
            saveDetectionRecord()
          }
        }
      }
      
      image.onerror = (e) => {
        console.error('图像加载失败:', e)
      }
      
      try {
        // 处理base64字符串，确保正确的格式
        let base64Data = message.data.frame
        
        // 检查base64数据是否已经包含前缀，避免重复添加
        if (base64Data.startsWith('data:image')) {
          // 已经包含前缀，直接使用
          image.src = base64Data
        } else {
          // 移除可能存在的非base64字符
          base64Data = base64Data.replace(/[^A-Za-z0-9+/=]/g, '')
          // 添加前缀
          image.src = 'data:image/jpeg;base64,' + base64Data
        }
      } catch (error) {
        console.error('设置图像源时发生错误:', error)
      }
    } else {
      console.log('收到的检测结果中没有图像数据')
      clearDisplay()
    }
    return
  }

  // 处理摄像头状态更新
  if (message.type === 'camera_status') {
    console.log('摄像头状态更新:', message.data)
    // 如果摄像头离线，清除画面
    if (message.data.status === 0) {
      clearDisplay()
    }
    return
  }

  // 处理停止流消息
  if (message.type === 'stream_stopped') {
    console.log('收到停止流消息')
    clearDisplay()
    return
  }
}

// 获取对象颜色
const getObjectColor = (className: string): string => {
  // 如果有配置的颜色，使用配置的颜色
  if (classColors.value && classColors.value[className]) {
    return classColors.value[className]
  }
  // 默认返回红色
  return '#FF0000'
}

// 处理检测对象点击
const handleObjectClick = (obj: any) => {
  // 点击对象时先阻止事件冒泡
  ElMessage({
    type: 'info',
    message: `点击了 ${obj.class}${obj.trackId !== undefined ? ' #' + obj.trackId : ''}，置信度: ${(obj.confidence * 100).toFixed(1)}%`,
    duration: 2000
  })
}

// 获取跟踪ID (根据算法端实际使用的trackId)
const getTrackId = (obj: any): number | null => {
  // 根据代码审查，算法端使用的属性名是trackId
  return obj && obj.trackId !== undefined ? obj.trackId : null
}

// 获取检测框样式
const getBoxStyle = (box: number[], className: string) => {
  if (!videoContainer.value || !currentDrawArea.value || !actualImageWidth.value || !actualImageHeight.value) return {}
  
  const [x1, y1, x2, y2] = box
  
  // 获取视频容器的实际可见尺寸
  const containerWidth = videoContainer.value.clientWidth
  const containerHeight = videoContainer.value.clientHeight
  
  const drawArea = currentDrawArea.value
  
  // 重要：我们需要考虑以下因素
  // 1. 原始图像尺寸(actualImageWidth/Height)到Canvas绘制区域(drawArea)的映射
  // 2. Canvas绘制区域在Canvas中的定位(drawArea.x/y)
  // 3. Canvas到容器的缩放比例(containerWidth/Height vs width/height)
  
  // 第一步：将检测框坐标从原始图像空间转换到归一化坐标(0-1范围)
  const normalizedX1 = x1 / actualImageWidth.value
  const normalizedY1 = y1 / actualImageHeight.value
  const normalizedX2 = x2 / actualImageWidth.value
  const normalizedY2 = y2 / actualImageHeight.value
  
  // 第二步：将归一化坐标应用到绘制区域
  const drawX1 = drawArea.x + normalizedX1 * drawArea.width
  const drawY1 = drawArea.y + normalizedY1 * drawArea.height
  const drawX2 = drawArea.x + normalizedX2 * drawArea.width
  const drawY2 = drawArea.y + normalizedY2 * drawArea.height
  
  // 第三步：将Canvas坐标转换为容器像素坐标
  const scaleX = containerWidth / width
  const scaleY = containerHeight / height
  
  const boxLeft = drawX1 * scaleX
  const boxTop = drawY1 * scaleY
  const boxWidth = (drawX2 - drawX1) * scaleX
  const boxHeight = (drawY2 - drawY1) * scaleY
  
  // 使用类别对应的颜色
  const borderColor = getObjectColor(className)
  
  // 检测框太小时设置一个最小可见度，但保持宽高比
  const minDimension = 3 // 允许更小的最小尺寸，但保持宽高比
  let finalBoxWidth = boxWidth
  let finalBoxHeight = boxHeight
  
  // 如果宽度太小，按比例增加尺寸
  if (boxWidth < minDimension) {
    const scale = minDimension / boxWidth
    finalBoxWidth = minDimension
    finalBoxHeight = boxHeight * scale
  }
  
  // 如果高度太小，按比例增加尺寸
  if (boxHeight < minDimension) {
    const scale = minDimension / boxHeight
    finalBoxHeight = minDimension
    finalBoxWidth = finalBoxWidth < minDimension ? boxWidth * scale : finalBoxWidth // 只有当宽度尚未调整时才调整
  }
  

  
  return {
    left: boxLeft + 'px',
    top: boxTop + 'px',
    width: finalBoxWidth + 'px',
    height: finalBoxHeight + 'px',
    borderColor
  }
}

// 获取标签样式
const getLabelStyle = (box: number[], className: string) => {
  if (!videoContainer.value || !currentDrawArea.value || !actualImageWidth.value || !actualImageHeight.value) return {}
  
  const [x1, y1, x2, y2] = box
  const containerWidth = videoContainer.value.clientWidth
  const containerHeight = videoContainer.value.clientHeight
  
  const drawArea = currentDrawArea.value
  
  // 使用与检测框相同的坐标转换逻辑 - 归一化坐标法
  const normalizedX1 = x1 / actualImageWidth.value
  const normalizedY1 = y1 / actualImageHeight.value
  const normalizedX2 = x2 / actualImageWidth.value
  const normalizedY2 = y2 / actualImageHeight.value
  
  // 应用到绘制区域
  const drawX1 = drawArea.x + normalizedX1 * drawArea.width
  const drawY1 = drawArea.y + normalizedY1 * drawArea.height
  const drawX2 = drawArea.x + normalizedX2 * drawArea.width
  const drawY2 = drawArea.y + normalizedY2 * drawArea.height
  
  // Canvas坐标转换为容器像素坐标
  const scaleX = containerWidth / width
  const scaleY = containerHeight / height
  
  const boxLeft = drawX1 * scaleX
  const boxTop = drawY1 * scaleY
  const boxRight = drawX2 * scaleX
  const boxBottom = drawY2 * scaleY
  const boxWidth = boxRight - boxLeft
  
  // 估计标签尺寸
  const className_length = className.length
  const estimatedLabelWidth = Math.max(80, className_length * 10 + 40) // 根据类名长度估计宽度
  
  // 检查边缘情况
  const isNearTop = boxTop < 30
  const isNearRight = containerWidth - boxRight < estimatedLabelWidth
  const isNearLeft = boxLeft < 10
  const isNearBottom = containerHeight - boxBottom < 30
  
  // 获取标签背景颜色
  const bgColor = getObjectColor(className)
  
  // 根据位置调整标签样式
  const style: any = {
    backgroundColor: bgColor,
  }
  
  // 垂直位置调整
  if (isNearTop) {
    if (isNearBottom) {
      // 既靠近顶部又靠近底部（框很大时），放在框内顶部
      style.top = '5px'
      style.bottom = 'auto'
    } else {
      // 靠近顶部，放在底部
      style.top = 'auto'
      style.bottom = '-24px'
    }
  } else {
    // 不靠近顶部，默认放在顶部
    style.top = '-24px'
    style.bottom = 'auto'
  }
  
  // 水平位置调整
  if (isNearRight) {
    if (isNearLeft) {
      // 框横跨大部分屏幕宽度
      style.left = 'auto'
      style.right = '0'
    } else {
      // 靠近右边缘，右对齐
      style.left = 'auto'
      style.right = '0'
    }
  } else if (boxWidth < estimatedLabelWidth && boxLeft + boxWidth/2 > containerWidth/2) {
    // 框较小且在屏幕右半部分，右对齐
    style.left = 'auto'
    style.right = '0'
  } else {
    // 默认左对齐
    style.left = '0'
    style.right = 'auto'
  }
  
  return style
}

// 切换群组图片面板展开状态
const toggleGroupImagesPanel = () => {
  groupImagesPanelExpanded.value = !groupImagesPanelExpanded.value
}

// 预览群组图片
const previewGroupImage = (groupImage: any, index: number) => {
  if (!groupImage.imageBase64) {
    ElMessage.warning('该群组图片不可用')
    return
  }
  
  // 创建图片预览数组
  const previewList = groupImages.value
    .filter(img => img.imageBase64)
    .map(img => `data:image/jpeg;base64,${img.imageBase64}`)
  
  if (previewList.length === 0) {
    ElMessage.warning('没有可预览的图片')
    return
  }
  
  // 找到当前图片在可预览列表中的索引
  const currentIndex = groupImages.value
    .slice(0, index + 1)
    .filter(img => img.imageBase64).length - 1
  
  // 创建图片查看器
  const imageViewer = document.createElement('div')
  imageViewer.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
  `
  
  const img = document.createElement('img')
  img.src = `data:image/jpeg;base64,${groupImage.imageBase64}`
  img.style.cssText = `
    max-width: 90%;
    max-height: 90%;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  `
  
  const closeBtn = document.createElement('button')
  closeBtn.innerHTML = '×'
  closeBtn.style.cssText = `
    position: absolute;
    top: 20px;
    right: 20px;
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    font-size: 30px;
    cursor: pointer;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
  `
  
  const title = document.createElement('div')
  title.innerHTML = `群组${groupImage.groupIndex} 截图`
  title.style.cssText = `
    position: absolute;
    top: 20px;
    left: 20px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    background: rgba(0, 0, 0, 0.5);
    padding: 8px 16px;
    border-radius: 4px;
  `
  
  imageViewer.appendChild(img)
  imageViewer.appendChild(closeBtn)
  imageViewer.appendChild(title)
  document.body.appendChild(imageViewer)
  
  // 关闭事件
  const closeViewer = () => {
    document.body.removeChild(imageViewer)
  }
  
  closeBtn.onclick = closeViewer
  imageViewer.onclick = (e) => {
    if (e.target === imageViewer) closeViewer()
  }
  
  // ESC键关闭
  const handleKeydown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      closeViewer()
      document.removeEventListener('keydown', handleKeydown)
    }
  }
  document.addEventListener('keydown', handleKeydown)
}

// 处理图片加载错误
const handleImageError = (event: Event) => {
  // 群组图片加载失败处理
}

// 格式化群组边界框
const formatGroupBbox = (bbox: number[]): string => {
  if (!Array.isArray(bbox) || bbox.length !== 4) {
    return '无效边界框'
  }
  const [x1, y1, x2, y2] = bbox.map(num => Math.round(num))
  return `${x2 - x1}×${y2 - y1}`
}

// 启动视频流
const startStream = () => {
  if (!wsClient.isConnected()) {
    // 如果WebSocket未连接，先连接WebSocket
    wsClient.connect()
    
    // 创建一个轮询检查，确保在连接成功后发送启动流消息
    const checkConnectionAndStart = () => {
      if (wsClient.isConnected()) {
        // 连接成功，发送启动流消息
        wsClient.send({
          type: 'start_stream',
          data: {
            cameraId: props.camera.id,
            rtspUrl: props.camera.rtspUrl
          }
        })
      } else {
        // 如果仍未连接，延迟再次检查
        setTimeout(checkConnectionAndStart, 500)
      }
    }
    
    // 启动第一次检查
    setTimeout(checkConnectionAndStart, 500)
  } else {
    // WebSocket已连接，直接发送消息
    wsClient.send({
      type: 'start_stream',
      data: {
        cameraId: props.camera.id,
        rtspUrl: props.camera.rtspUrl
      }
    })
  }
}

// 验证base64字符串是否有效
const isValidBase64 = (str: string): boolean => {
  if (!str || typeof str !== 'string') return false
  
  // 如果已经包含前缀，先移除前缀
  if (str.startsWith('data:image')) {
    const parts = str.split(',')
    if (parts.length !== 2) return false
    str = parts[1]
  }
  
  // 检查是否只包含base64合法字符
  const regex = /^[A-Za-z0-9+/=]+$/
  const isValid = regex.test(str)
  

  
  return isValid
}

// 监听激活状态
watch(() => props.isActive, (newValue) => {
  if (newValue) {
    startStream()
  } else {
    // 当摄像头不再激活时，清除画面
    clearDisplay()
  }
})

onMounted(() => {
  // 初始化Canvas
  if (canvas.value) {
    ctx.value = canvas.value.getContext('2d')
    if (!ctx.value) {
      console.error('无法获取Canvas上下文')
    }
  } else {
    console.error('Canvas元素不存在')
  }
  
  // 设置ResizeObserver监听容器尺寸变化
  cleanupResizeObserver = setupResizeObserver()
  
  // 添加消息处理器
  wsClient.addMessageHandler(handleMessage)
  
  // 如果是激活状态，启动视频流
  if (props.isActive) {
    startStream()
  }
  
  // 初始读取一次容器尺寸
  if (videoContainer.value) {
    containerSize.value = {
      width: videoContainer.value.clientWidth,
      height: videoContainer.value.clientHeight
    }
  }
})

onBeforeUnmount(() => {
  // 清除画面
  clearDisplay()
  // 移除消息处理器
  wsClient.removeMessageHandler(handleMessage)
  // 调用清理函数，断开ResizeObserver连接
  if (cleanupResizeObserver) {
    cleanupResizeObserver()
  }
})

// 计算保持宽高比的绘制区域
const calculateDrawArea = (imageWidth: number, imageHeight: number, canvasWidth: number, canvasHeight: number) => {
  // 计算图像和画布的宽高比
  const imageRatio = imageWidth / imageHeight
  const canvasRatio = canvasWidth / canvasHeight
  
  let drawWidth, drawHeight, drawX, drawY
  
  // 如果图像的宽高比大于画布的宽高比，以宽度为准，确保整个图像宽度都在画布内
  if (imageRatio > canvasRatio) {
    drawWidth = canvasWidth
    drawHeight = canvasWidth / imageRatio
    drawX = 0
    drawY = (canvasHeight - drawHeight) / 2
  } 
  // 否则以高度为准，确保整个图像高度都在画布内
  else {
    drawHeight = canvasHeight
    drawWidth = canvasHeight * imageRatio
    drawX = (canvasWidth - drawWidth) / 2
    drawY = 0
  }
  

  
  return { x: drawX, y: drawY, width: drawWidth, height: drawHeight }
}
</script>

<style lang="scss" scoped>
.video-player {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #000;
  border-radius: 8px;
  overflow: hidden;
  
  .video-container {
    position: relative;
    width: 100%;
    height: 100%;
    
    canvas {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
    
    .detection-box {
      position: absolute;
      border: 2px solid #FF0000;
      border-radius: 4px;
      pointer-events: all;
      overflow: visible;
      transition: all 0.2s ease;
      
      // 跟踪框特殊样式
      &.tracking-box {
        border-style: dashed;
        animation: borderPulse 2s infinite;
      }
      
      &:hover {
        border-width: 3px;
        box-shadow: 0 0 8px rgba(255, 0, 0, 0.6);
        z-index: 11; // 确保悬停时在最上层
        
        .confidence {
          font-weight: bold;
          box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
          transform: scale(1.05);
        }
      }
      
      .confidence {
        position: absolute;
        padding: 2px 6px;
        color: #fff;
        font-size: 12px;
        border-radius: 4px;
        background-color: #FF0000;
        white-space: nowrap;
        z-index: 10;
        transition: all 0.2s ease;
        transform-origin: left center;
        cursor: pointer;
        text-shadow: 0 0 2px rgba(0, 0, 0, 0.5); // 添加文字阴影提高可读性
        
        .track-id {
          display: inline-block;
          margin-left: 4px;
          font-weight: bold;
          color: #ffff00; // 黄色使跟踪ID更加突出
          font-size: 12px;
          text-shadow: 0 0 3px rgba(0, 0, 0, 0.7); // 加强阴影使其在任何背景下都清晰可见
        }
      }
    }
  }
  
  .camera-info {
    position: absolute;
    top: 10px;
    left: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 5px 10px;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 4px;
    
    .name {
      color: #fff;
      font-size: 14px;
    }
    
    .status {
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
      
      &.online {
        background-color: #67c23a;
        color: #fff;
      }
      
      &.offline {
        background-color: #909399;
        color: #fff;
      }
    }
  }
  
  .detection-alert-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(to bottom, 
      rgba(59, 130, 246, 0.2), 
      rgba(0, 0, 0, 0.4)
    );
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
    
    &.alert-active {
      opacity: 1;
      pointer-events: auto;
      animation: pulseBackground 2s infinite;
    }

    // 新增警告容器，用于统一应用缩放
    .alert-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: transform 0.3s ease;
      transform-origin: center center;
      width: 100%;
      max-width: 400px; // 设置最大宽度
    }

    .alert-icon {
      margin-bottom: 20px;
      .el-icon {
        font-size: 48px;
        color: #fff;
        animation: pulse 1s infinite;
      }
    }

    .alert-info {
      background: rgba(0, 0, 0, 0.75);
      padding: 15px;
      border-radius: 8px;
      backdrop-filter: blur(4px);
      border: 2px solid #FF0000;
      animation: borderBlink 2s infinite;
      width: 90%;
      max-width: 360px; // 设置最大宽度

      .alert-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;

        .warning-text {
          color: #3b82f6;
          font-size: 20px;
          font-weight: bold;
        }

        .level-tag {
          margin-left: auto;
        }
      }

      .alert-details {
        display: grid;
        gap: 8px;

        .detail-item {
          display: flex;
          align-items: center;
          gap: 8px;

          .label {
            color: #909399;
            min-width: 50px;
          }

          .value {
            color: #fff;
            font-weight: 500;
          }
        }
      }
    }

    .alert-actions {
      margin-top: 15px;

      .action-button {
        animation: shake 1s infinite;
      }
    }
  }
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-2px); }
  75% { transform: translateX(2px); }
}

@keyframes borderBlink {
  0% { border-color: rgba(59, 130, 246, 0.4); box-shadow: 0 0 0 rgba(59, 130, 246, 0); }
  50% { border-color: rgba(59, 130, 246, 1); box-shadow: 0 0 8px rgba(59, 130, 246, 0.4); }
  100% { border-color: rgba(59, 130, 246, 0.4); box-shadow: 0 0 0 rgba(59, 130, 246, 0); }
}

@keyframes pulseBackground {
  0% { background: linear-gradient(to bottom, rgba(59, 130, 246, 0.1), rgba(0, 0, 0, 0.4)); }
  50% { background: linear-gradient(to bottom, rgba(59, 130, 246, 0.3), rgba(0, 0, 0, 0.4)); }
  100% { background: linear-gradient(to bottom, rgba(59, 130, 246, 0.1), rgba(0, 0, 0, 0.4)); }
}

// 添加边框闪烁动画
@keyframes borderPulse {
  0% { border-width: 2px; }
  50% { border-width: 3px; }
  100% { border-width: 2px; }
}

// 群组图片面板样式
.group-images-panel {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.85);
  border-radius: 8px;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  min-width: 280px;
  max-width: 400px;
  max-height: 60vh;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  
  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.05);
    
    .panel-title {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #fff;
      font-size: 14px;
      font-weight: 600;
      
      .el-icon {
        color: #60a5fa;
      }
    }
    
    .toggle-btn {
      padding: 4px;
      min-height: auto;
      color: #fff;
      
      &:hover {
        background: rgba(255, 255, 255, 0.1);
      }
    }
  }
  
  .panel-content {
    padding: 12px;
    max-height: 400px;
    overflow-y: auto;
    
    &::-webkit-scrollbar {
      width: 4px;
    }
    
    &::-webkit-scrollbar-track {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 2px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.3);
      border-radius: 2px;
      
      &:hover {
        background: rgba(255, 255, 255, 0.5);
      }
    }
  }
  
  .group-images-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 10px;
  }
  
  .group-image-item {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
    
    &:hover {
      background: rgba(255, 255, 255, 0.1);
      transform: translateY(-2px);
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
    }
    
    .image-wrapper {
      width: 100%;
      height: 80px;
      position: relative;
      overflow: hidden;
      
      .group-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.2s ease;
      }
      
      .image-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: rgba(255, 255, 255, 0.5);
        font-size: 12px;
        
        .el-icon {
          font-size: 20px;
          margin-bottom: 4px;
        }
      }
    }
    
    .image-label {
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 2px;
      
      .group-title {
        color: #fff;
        font-size: 12px;
        font-weight: 600;
      }
      
      .bbox-info {
        color: rgba(255, 255, 255, 0.7);
        font-size: 10px;
      }
    }
    
    &:hover .group-image {
      transform: scale(1.05);
    }
  }
}
</style> 