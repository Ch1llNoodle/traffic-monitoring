<template>
  <div class="detection-record-container">
    <!-- 页面头部 -->
    <div class="page-header-card">
      <div class="page-title">
        <el-icon class="page-icon"><DataAnalysis /></el-icon>
        <h2>智慧交通记录</h2>
      </div>
      <div class="action-buttons">
        <el-popconfirm
          title="确定要清空所有检测记录吗？此操作不可恢复！"
          confirm-button-text="确定"
          cancel-button-text="取消"
          @confirm="handleClearAll"
        >
          <template #reference>
            <el-button type="danger" class="action-button">
              <el-icon><Delete /></el-icon>
              清空所有记录
            </el-button>
          </template>
        </el-popconfirm>
        <el-button type="danger" @click="handleBatchDelete" :disabled="selectedRecords.length === 0" class="action-button">
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
        <el-button type="primary" @click="refreshRecords" class="action-button">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>
    
    <!-- 搜索栏 -->
    <div class="search-card">
      <div class="search-header">
        <el-icon><Search /></el-icon>
        <span>筛选条件</span>
      </div>
      <div class="search-content">
        <el-form :model="queryParams" inline>
          <el-form-item label="摄像头">
            <el-select v-model="queryParams.cameraId" clearable placeholder="选择摄像头" class="search-select">
              <el-option 
                v-for="camera in cameras" 
                :key="camera.id" 
                :label="camera.name" 
                :value="camera.id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="处理状态">
            <el-select v-model="queryParams.processed" clearable placeholder="选择状态" class="search-select">
              <el-option :value="0" label="未处理">
                <div class="custom-option">
                  <el-tag type="warning" size="small">未处理</el-tag>
                </div>
              </el-option>
              <el-option :value="1" label="已处理">
                <div class="custom-option">
                  <el-tag type="success" size="small">已处理</el-tag>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="检测时间">
            <el-date-picker
              v-model="dateRange"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD"
              class="date-picker"
            />
          </el-form-item>
          <el-form-item class="search-buttons">
            <el-button type="primary" @click="searchRecords" class="search-button">
              <el-icon><Search /></el-icon>
              查询
            </el-button>
            <el-button @click="resetSearch" class="search-button">
              <el-icon><RefreshRight /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    
    <!-- 数据列表 -->
    <div class="data-card">
      <div v-if="records.length === 0 && !loading" class="empty-data">
        <el-empty description="暂无检测记录" :image-size="120">
          <template #image>
            <el-icon class="empty-icon"><PictureFilled /></el-icon>
          </template>
        </el-empty>
      </div>
      
      <el-table
        v-else
        :data="records"
        v-loading="loading"
        border
        stripe
        style="width: 100%"
        @selection-change="handleSelectionChange"
        class="data-table"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }"
        row-key="id"
      >
        <el-table-column type="selection" width="55" fixed="left" />
        <el-table-column type="index" width="60" label="#" fixed="left" align="center" />
        <el-table-column prop="cameraName" label="摄像头" min-width="120" show-overflow-tooltip>
          <template #default="{ row }">
            <div class="camera-name">
              <el-icon><VideoCamera /></el-icon>
              <span>{{ row.cameraName }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="检测时间" min-width="160" sortable>
          <template #default="{ row }">
            <div class="time-cell">
              <el-icon><Timer /></el-icon>
              <span>{{ formatDateTime(row.detectionTime) }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="检测图像" min-width="180" align="center">
          <template #default="{ row }">
            <div class="image-cell">
              <el-image
                :src="row.imageUrl"
                :preview-src-list="[row.imageUrl]"
                fit="cover"
                class="table-image"
                :initial-index="0"
                :preview-teleported="true"
                :z-index="9999"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><PictureRounded /></el-icon>
                    <span>加载失败</span>
                  </div>
                </template>
              </el-image>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag 
              :type="row.processed === 0 ? 'warning' : 'success'"
              effect="light"
              class="status-tag"
            >
              <el-icon v-if="row.processed === 0"><WarningFilled /></el-icon>
              <el-icon v-else><SuccessFilled /></el-icon>
              {{ row.processed === 0 ? '未处理' : '已处理' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <div class="action-column">
              <el-button type="primary" link @click="viewDetail(row)" class="action-link">
                <el-icon><View /></el-icon>
                查看
              </el-button>
              <el-button 
                v-if="row.processed === 0" 
                type="success" 
                link 
                @click="handleProcess(row)"
                class="action-link"
              >
                <el-icon><Edit /></el-icon>
                处理
              </el-button>
              <el-button type="danger" link @click="handleDelete(row)" class="action-link">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="queryParams.current"
          v-model:page-size="queryParams.size"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          background
          class="custom-pagination"
        />
      </div>
    </div>
    
    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="检测记录详情" width="85%" top="3vh" destroy-on-close class="detail-dialog">
      <div v-if="currentRecord" class="record-detail">
        <!-- 顶部信息卡片 -->
        <div class="info-card">
          <div class="info-header">
            <h3>基本信息</h3>
          </div>
          <div class="info-content">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="摄像头">
                <el-tag size="default" type="primary" effect="plain">
                  <el-icon class="mr-5"><VideoCamera /></el-icon>
                  {{ currentRecord.cameraName }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="检测时间">
                <el-icon class="mr-5"><Timer /></el-icon>
                {{ formatDateTime(currentRecord.detectionTime) }}
              </el-descriptions-item>
              <el-descriptions-item label="创建时间">
                <el-icon class="mr-5"><Calendar /></el-icon>
                {{ formatDateTime(currentRecord.createTime) }}
              </el-descriptions-item>
              <el-descriptions-item label="状态">
                <el-tag 
                  :type="currentRecord.processed === 0 ? 'warning' : 'success'"
                  effect="light"
                  size="default"
                >
                  <el-icon class="mr-5">
                    <component :is="currentRecord.processed === 0 ? 'WarningFilled' : 'SuccessFilled'" />
                  </el-icon>
                  {{ currentRecord.processed === 0 ? '未处理' : '已处理' }}
                </el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </div>
        
        <div class="detail-container">
          <!-- 左侧：检测图像 -->
          <div class="detail-left">
            <div class="image-section">
              <div class="section-header">
                <el-icon><Picture /></el-icon>
                <h3>检测图像</h3>
              </div>
              <div class="image-wrapper">
                <el-image
                  :src="currentRecord.imageUrl"
                  :preview-src-list="[currentRecord.imageUrl]"
                  fit="contain"
                  class="detection-image"
                  :preview-teleported="true"
                  :z-index="9999"
                />
              </div>
            </div>
          </div>
          
          <!-- 右侧：检测结果 -->
          <div class="detail-right">
            <div v-if="parsedDetectionResult" class="result-detail">
              <div class="section-header">
                <el-icon><DataAnalysis /></el-icon>
                <h3>检测结果</h3>
              </div>
              
                              <div v-if="parsedDetectionResult.dangerousDrivingResults?.length" class="dangerous-driving-results">
                  <h4><el-icon><Warning /></el-icon> 危险驾驶行为检测结果</h4>
                  <el-table :data="parsedDetectionResult.dangerousDrivingResults" border stripe>
                  <el-table-column prop="groupIndex" label="群组" width="80">
                    <template #default="{ row }">
                      群组{{ row.groupIndex }}
                    </template>
                  </el-table-column>
                  <el-table-column prop="description" label="分析结果" />
                  <el-table-column prop="riskLevel" label="风险等级" width="120">
                    <template #default="{ row }">
                      <el-tag :type="getViolenceRiskType(row.riskLevel)" size="default" effect="light">
                        {{ getViolenceRiskText(row.riskLevel) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="confidence" label="置信度" width="120">
                    <template #default="{ row }">
                      <el-progress 
                        :percentage="Math.round(row.confidence * 100)" 
                        :color="getConfidenceColor(row.confidence)"
                        :stroke-width="14"
                        text-inside
                      />
                    </template>
                  </el-table-column>
                </el-table>
              </div>
              
              <div v-if="getGroupImages().length" class="group-images">
                <h4><el-icon><PictureRounded /></el-icon> 群组截取图片</h4>
                <div class="group-images-grid">
                  <div 
                    v-for="(groupImage, index) in getGroupImages()" 
                    :key="index"
                    class="group-image-card"
                  >
                                                <div class="group-image-header">
                      <span class="group-title">群组{{ groupImage.groupIndex }}</span>
                      <el-tag v-if="groupImage.bbox" size="small" type="info">
                        {{ formatBbox(groupImage.bbox) }}
                      </el-tag>
                    </div>
                    <div class="group-image-content">
                      <el-image
                        v-if="groupImage.imageUrl || groupImage.imageBase64"
                        :src="groupImage.imageUrl || (groupImage.imageBase64 ? `data:image/jpeg;base64,${groupImage.imageBase64}` : '')"
                        :preview-src-list="getGroupImages().map((img: any) => img.imageUrl || (img.imageBase64 ? `data:image/jpeg;base64,${img.imageBase64}` : '')).filter((url: string) => url)"
                        :initial-index="index"
                        fit="contain"
                        class="group-image"
                        :preview-teleported="true"
                        :z-index="9999"
                        lazy
                      >
          <template #placeholder>
            <div class="image-loading">
              <el-icon class="is-loading"><Loading /></el-icon>
              <span>加载中...</span>
            </div>
          </template>
          <template #error>
            <div class="image-error">
              <el-icon><Picture /></el-icon>
              <span>图片加载失败</span>
            </div>
          </template>
        </el-image>
        <div v-else-if="groupImage.uploadError" class="image-error">
          <el-icon><Warning /></el-icon>
          <span>{{ groupImage.uploadError }}</span>
        </div>
        <div v-else class="image-error">
          <el-icon><Picture /></el-icon>
          <span>暂无图片</span>
        </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="parsedDetectionResult.trafficGroups?.length" class="traffic-groups">
                <h4><el-icon><List /></el-icon> 检测到的交通场景群组</h4>
                <el-table :data="parsedDetectionResult.trafficGroups" border stripe class="traffic-groups-table">
                  <el-table-column label="群组编号" min-width="120" align="center">
                    <template #default="{ row, $index }">
                      <el-tag type="primary" size="small">交通场景群组{{ $index + 1 }}</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="memberCount" label="对象数量" min-width="100" align="center">
                    <template #default="{ row }">
                      <el-tag type="info" size="small">{{ row.memberCount }} 个</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column prop="avgConfidence" label="平均置信度" min-width="150" align="center">
                    <template #default="{ row }">
                      <el-progress 
                        :percentage="Math.round(row.avgConfidence * 100)" 
                        :color="getConfidenceColor(row.avgConfidence)"
                        :stroke-width="12"
                        text-inside
                        :show-text="true"
                      />
                    </template>
                  </el-table-column>
                  <el-table-column label="边界框坐标" min-width="200" align="center">
                    <template #default="{ row }">
                      <span class="bbox-text">{{ formatBbox(row.groupBbox) }}</span>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
              
              <div v-if="parsedDetectionResult.detectedObjects?.length" class="detected-objects">
                <h4><el-icon><List /></el-icon> 所有检测对象</h4>
                <el-scrollbar max-height="250px">
                  <el-table :data="parsedDetectionResult.detectedObjects" border stripe>
                    <el-table-column prop="class" label="类型" />
                    <el-table-column prop="confidence" label="置信度">
                      <template #default="{ row }">
                        <el-progress 
                          :percentage="Math.round(row.confidence * 100)" 
                          :color="getConfidenceColor(row.confidence)"
                          :stroke-width="12"
                          text-inside
                        />
                      </template>
                    </el-table-column>
                    <el-table-column label="边界框" width="200">
                      <template #default="{ row }">
                        <span class="bbox-text">{{ formatBbox(row.bbox) }}</span>
                      </template>
                    </el-table-column>
                  </el-table>
                </el-scrollbar>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 处理信息 -->
        <div v-if="currentRecord.processed === 1" class="process-detail">
          <div class="section-header">
            <el-icon><Operation /></el-icon>
            <h3>处理信息</h3>
          </div>
          
          <div class="process-content">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="处理时间">
                <el-icon class="mr-5"><Timer /></el-icon>
                {{ formatDateTime(currentRecord.processTime || '') }}
              </el-descriptions-item>
              <el-descriptions-item label="处理内容" class="description-content">
                <div class="process-message">
                  {{ currentRecord.processContent || '无' }}
                </div>
              </el-descriptions-item>
            </el-descriptions>
            
            <div v-if="currentRecord.processImageUrl" class="process-image-container">
              <div class="section-header sub-header">
                <el-icon><PictureFilled /></el-icon>
                <h4>处理照片</h4>
              </div>
              <div class="image-wrapper">
                <el-image 
                  ref="processImageRef"
                  :src="currentRecord.processImageUrl" 
                  :preview-src-list="[currentRecord.processImageUrl]"
                  :preview-teleported="true"
                  :initial-index="0"
                  :z-index="9999"
                  fit="contain"
                  class="record-process-image"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
          <el-button 
            v-if="currentRecord && currentRecord.processed === 0" 
            type="success" 
            @click="handleProcess(currentRecord)"
          >
            <el-icon class="mr-5"><Edit /></el-icon>
            处理此记录
          </el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 处理记录对话框 -->
    <el-dialog v-model="processDialogVisible" title="处理检测记录" width="600px" class="process-dialog" destroy-on-close>
      <div class="process-dialog-header">
        <el-icon class="process-icon"><Edit /></el-icon>
        <span>请填写处理信息</span>
      </div>
      
      <el-form 
        v-if="processForm"
        :model="processForm" 
        ref="processFormRef" 
        label-width="100px"
        :rules="processRules"
        class="process-form"
      >
        <el-form-item label="处理内容" prop="processContent">
          <el-input 
            v-model="processForm.processContent" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入处理内容..."
            class="process-input"
          />
        </el-form-item>
        
        <el-form-item label="处理照片" prop="processImageFile">
          <el-upload
            class="process-image-uploader"
            :auto-upload="false"
            :show-file-list="true"
            :limit="1"
            accept="image/jpeg,image/png,image/jpg"
            :on-change="handleProcessImageChange"
            :on-exceed="handleExceed"
            :on-remove="handleRemove"
          >
            <el-button type="primary">
              <el-icon><Upload /></el-icon>
              选择图片
            </el-button>
            <template #tip>
              <div class="el-upload__tip">
                可选上传一张处理照片，仅支持 jpg/png 文件
              </div>
            </template>
          </el-upload>
          
          <div v-if="processImageUrl" class="process-image-preview">
            <el-image
              :src="processImageUrl"
              fit="contain"
              style="max-width: 100%; height: 300px; object-fit: contain;"
              :preview-teleported="true"
              :preview-src-list="[processImageUrl]"
              :z-index="9999"
            />
          </div>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="processDialogVisible = false">
            <el-icon><Close /></el-icon>
            取消
          </el-button>
          <el-button type="primary" @click="submitProcess" :loading="processLoading">
            <el-icon><Check /></el-icon>
            确认处理
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, UploadFile } from 'element-plus'
import { 
  Refresh, Delete, VideoCamera, Timer, Picture, Calendar, Warning,
  List, DataAnalysis, Edit, Operation, PictureFilled, Search,
  RefreshRight, SuccessFilled, WarningFilled, View, PictureRounded,
  Upload, Check, Close, Loading
} from '@element-plus/icons-vue'
import { 
  pageDetectionRecords, 
  getDetectionRecordById, 
  updateProcessStatus, 
  deleteDetectionRecord,
  batchDeleteDetectionRecords,
  clearAllDetectionRecords,
  processDetectionRecord,
  type DetectionRecord,
  type DetectionRecordQueryParams,
  type DetectionRecordProcessParams
} from '@/api/detection'
import type { Camera } from '@/types/camera'
import { getCameraList } from '@/api/camera'
import { ElImageViewer } from 'element-plus'

// 查询参数
const queryParams = reactive<DetectionRecordQueryParams>({
  current: 1,
  size: 10
})

// 日期范围
const dateRange = ref<string[]>([])

// 状态
const loading = ref(false)
const records = ref<DetectionRecord[]>([])
const total = ref(0)
const cameras = ref<Camera[]>([])
const detailDialogVisible = ref(false)
const currentRecord = ref<DetectionRecord | null>(null)
// 多选记录
const selectedRecords = ref<DetectionRecord[]>([])

// 处理相关
const processDialogVisible = ref(false)
const processLoading = ref(false)
const processForm = ref<{
  id: number
  processContent: string
  processImageFile?: File
}>()
const processFormRef = ref<FormInstance>()
const processImageUrl = ref('')

// 处理表单验证规则
const processRules = {
  processContent: [
    { required: true, message: '请输入处理内容', trigger: 'blur' },
    { min: 2, max: 500, message: '长度在2到500个字符', trigger: 'blur' }
  ]
}

// 检测结果解析
const parsedDetectionResult = computed(() => {
  if (!currentRecord.value?.detectionResult) return null
  try {
    return JSON.parse(currentRecord.value.detectionResult)
  } catch (e) {
    console.error('解析检测结果失败:', e)
    return null
  }
})

// 图片引用
const processImageRef = ref();

// 初始化
onMounted(async () => {
  await Promise.all([
    loadCameras(),
    fetchRecords()
  ])
})

// 加载摄像头列表
const loadCameras = async () => {
  try {
    const result = await getCameraList({ current: 1, size: 1000 })
    cameras.value = result.records
  } catch (error) {
    console.error('获取摄像头列表失败:', error)
  }
}

// 查询记录
const fetchRecords = async () => {
  loading.value = true
  try {
    // 执行查询
    const result = await pageDetectionRecords(queryParams)
    records.value = result.records
    total.value = result.total
  } catch (error) {
    console.error('获取检测记录失败:', error)
    ElMessage.error('获取检测记录失败')
  } finally {
    loading.value = false
  }
}

// 搜索记录
const searchRecords = () => {
  queryParams.current = 1
  
  // 设置日期范围参数 - 移除此处的手动拼接，直接使用后端处理
  if (dateRange.value && dateRange.value.length === 2) {
    queryParams.startTime = dateRange.value[0]
    queryParams.endTime = dateRange.value[1]
  } else {
    queryParams.startTime = undefined
    queryParams.endTime = undefined
  }
  
  fetchRecords()
}

// 重置搜索
const resetSearch = () => {
  queryParams.current = 1
  queryParams.cameraId = undefined
  queryParams.processed = undefined
  dateRange.value = []
  delete queryParams.startTime
  delete queryParams.endTime
  fetchRecords()
}

// 刷新
const refreshRecords = () => {
  fetchRecords()
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  queryParams.size = size
  fetchRecords()
}

// 页码变化
const handleCurrentChange = (current: number) => {
  queryParams.current = current
  fetchRecords()
}

// 查看详情
const viewDetail = (row: DetectionRecord) => {
  currentRecord.value = row
  detailDialogVisible.value = true
}

// 处理记录
const handleProcess = (row: DetectionRecord) => {
  processForm.value = {
    id: row.id,
    processContent: ''
  }
  processImageUrl.value = ''
  processDialogVisible.value = true
}

// 处理照片变更
const handleProcessImageChange = (file: UploadFile) => {
  // 限制图片大小
  const isLt2M = file.size ? file.size / 1024 / 1024 < 2 : true
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB!')
    return
  }
  
  if (file.raw) {
    processForm.value!.processImageFile = file.raw
    processImageUrl.value = URL.createObjectURL(file.raw)
  }
}

// 超出文件限制
const handleExceed = () => {
  ElMessage.warning('只能上传一张图片')
}

// 移除文件
const handleRemove = () => {
  processForm.value!.processImageFile = undefined
  processImageUrl.value = ''
}

// 提交处理
const submitProcess = async () => {
  if (!processFormRef.value) return
  
  await processFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      processLoading.value = true
      
      // 构建处理参数
      const processParams: DetectionRecordProcessParams = {
        id: Number(processForm.value!.id),
        processed: 1,
        processContent: processForm.value!.processContent
      }
      
      // 如果有处理照片，转换为base64
      if (processForm.value!.processImageFile) {
        processParams.processImageBase64 = await fileToBase64(processForm.value!.processImageFile)
      }
      
      // 调用API处理记录
      await processDetectionRecord(processParams)
      
      ElMessage.success('记录处理成功')
      processDialogVisible.value = false
      
      // 刷新记录列表
      await fetchRecords()
      
      // 如果是从详情页处理的，更新当前记录并刷新详情
      if (currentRecord.value && currentRecord.value.id === processForm.value!.id) {
        const updated = await getDetectionRecordById(processForm.value!.id)
        currentRecord.value = updated
      }
    } catch (error) {
      console.error('处理记录失败:', error)
      ElMessage.error('处理记录失败')
    } finally {
      processLoading.value = false
    }
  })
}

// 文件转base64
const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        // 移除前缀 (例如: "data:image/jpeg;base64,")
        const base64Str = reader.result
        const base64Data = base64Str.split(',')[1]
        resolve(base64Data)
      } else {
        reject(new Error('无法读取文件内容'))
      }
    }
    reader.onerror = reject
  })
}

// 标记为已处理 (简单标记，不使用新功能)
const markAsProcessed = async (row: DetectionRecord) => {
  try {
    await updateProcessStatus(row.id, 1)
    ElMessage.success('标记成功')
    fetchRecords()
    
    // 如果是在详情页操作，也更新当前记录状态
    if (currentRecord.value && currentRecord.value.id === row.id) {
      currentRecord.value.processed = 1
    }
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('更新状态失败')
  }
}

// 删除记录
const handleDelete = (row: DetectionRecord) => {
  ElMessageBox.confirm('确定要删除这条检测记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteDetectionRecord(row.id)
      ElMessage.success('删除成功')
      fetchRecords()
      
      // 如果删除的是当前查看的记录，关闭详情对话框
      if (currentRecord.value && currentRecord.value.id === row.id) {
        detailDialogVisible.value = false
      }
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 表格选择变化
const handleSelectionChange = (selection: DetectionRecord[]) => {
  selectedRecords.value = selection
}

// 批量删除
const handleBatchDelete = () => {
  if (selectedRecords.value.length === 0) {
    ElMessage.warning('请至少选择一条记录')
    return
  }
  
  ElMessageBox.confirm(`确定要删除选中的 ${selectedRecords.value.length} 条检测记录吗？`, '批量删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      const ids = selectedRecords.value.map(record => record.id)
      await batchDeleteDetectionRecords(ids)
      ElMessage.success('批量删除成功')
      fetchRecords()
      
      // 如果当前查看的记录被删除，关闭详情对话框
      if (currentRecord.value && ids.includes(currentRecord.value.id)) {
        detailDialogVisible.value = false
      }
    } catch (error) {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

// 格式化日期时间
const formatDateTime = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
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

// 格式化边界框坐标
const formatBbox = (bbox: number[]): string => {
  if (!bbox || bbox.length !== 4) return '无数据'
  return `(${bbox[0].toFixed(0)}, ${bbox[1].toFixed(0)}, ${bbox[2].toFixed(0)}, ${bbox[3].toFixed(0)})`
}

// 预览处理图片
const previewProcessImage = () => {
  if (currentRecord.value?.processImageUrl && processImageRef.value) {
    processImageRef.value.clickHandler();
  }
}

// 清空所有检测记录
const handleClearAll = async () => {
  try {
    loading.value = true
    const res = await clearAllDetectionRecords()
    if (res) {
      ElMessage.success('已成功清空所有检测记录')
      // 刷新记录列表
      fetchRecords()
    } else {
      ElMessage.error('清空检测记录失败')
    }
  } catch (error) {
    console.error('清空检测记录出错:', error)
    ElMessage.error('清空检测记录出错')
  } finally {
    loading.value = false
  }
}

// 获取置信度颜色
const getConfidenceColor = (confidence: number) => {
  if (confidence >= 0.8) return '#67c23a'
  if (confidence >= 0.5) return '#409eff'
  if (confidence >= 0.3) return '#e6a23c'
  return '#f56c6c'
}

// 获取群组图片（兼容新旧数据结构）
const getGroupImages = () => {
  if (!parsedDetectionResult.value) return []
  
  // 优先使用 groupImages 数组（处理后的数据，包含文件引用信息）
  if (parsedDetectionResult.value.groupImages && parsedDetectionResult.value.groupImages.length > 0) {
    return parsedDetectionResult.value.groupImages
  }
  
  // 如果没有 groupImages，从 dangerousDrivingResults 中提取（向后兼容旧数据）
  // 注意：新数据中 dangerousDrivingResults 只包含 groupImageBase64，不包含文件引用信息
  if (parsedDetectionResult.value.dangerousDrivingResults && parsedDetectionResult.value.dangerousDrivingResults.length > 0) {
    const groupImages: any[] = []
    
    parsedDetectionResult.value.dangerousDrivingResults.forEach((result: any) => {
      if (result.groupImageBase64) {
        groupImages.push({
          groupIndex: result.groupIndex,
          bbox: result.groupBbox,
          imageBase64: result.groupImageBase64
        })
      }
    })
    
    return groupImages
  }
  
  return []
}


</script>

<style lang="scss" scoped>
.detection-record-container {
  padding: 20px;
  
  // 卡片通用样式
  .card-common {
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
    background-color: #fff;
    margin-bottom: 20px;
    overflow: hidden;
    transition: all 0.3s;
    
    &:hover {
      box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
    }
  }
  
  // 页面头部卡片
  .page-header-card {
    @extend .card-common;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-left: 4px solid #3b82f6;
    
    .page-title {
      display: flex;
      align-items: center;
      
      .page-icon {
        font-size: 24px;
        color: #3b82f6;
        margin-right: 12px;
      }
      
      h2 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
        color: #303133;
      }
    }
    
    .action-buttons {
      display: flex;
      gap: 12px;
      
      .action-button {
        display: flex;
        align-items: center;
        gap: 5px;
      }
    }
  }
  
  // 搜索卡片
  .search-card {
    @extend .card-common;
    
    .search-header {
      padding: 12px 20px;
      background-color: #f5f7fa;
      border-bottom: 1px solid #ebeef5;
      display: flex;
      align-items: center;
      
      .el-icon {
        color: #3b82f6;
        margin-right: 6px;
      }
      
      span {
        font-size: 16px;
        font-weight: 600;
        color: #303133;
      }
    }
    
    .search-content {
      padding: 20px;
      
      .el-form {
        display: flex;
        flex-wrap: wrap;
        gap: 10px 20px;
        
        .el-form-item {
          margin-bottom: 10px;
        }
      }
      
      .search-select {
        width: 180px;
      }
      
      .date-picker {
        width: 360px;
      }
      
      .search-buttons {
        margin-left: auto;
        display: flex;
        align-items: flex-end;
        
        .search-button {
          display: flex;
          align-items: center;
          gap: 5px;
        }
      }
      
      .custom-option {
        display: flex;
        align-items: center;
      }
    }
  }
  
  // 数据卡片
  .data-card {
    @extend .card-common;
    padding: 0;
    
    .empty-data {
      padding: 60px 0;
      
      .empty-icon {
        font-size: 60px;
        color: #c0c4cc;
      }
    }
    
    .data-table {
      border-radius: 8px 8px 0 0;
      
      :deep(.el-table__header) {
        thead tr th {
          background-color: #f5f7fa;
          font-weight: 600;
        }
      }
      
      :deep(.el-table__row) {
        transition: all 0.3s;
        
        &:hover {
          background-color: #f0f9ff !important;
        }
      }
      
      .camera-name, .time-cell {
        display: flex;
        align-items: center;
        gap: 8px;
        
        .el-icon {
          color: #1e40af;
        }
      }
      
      .image-cell {
        padding: 5px 0;
        
        .table-image {
          width: 100px;
          height: 60px;
          border-radius: 4px;
          transition: all 0.3s;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          cursor: pointer;
          overflow: hidden;
          
          &:hover {
            transform: scale(1.05);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
          }
        }
        
        .image-error {
          width: 100px;
          height: 60px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          background-color: #f5f7fa;
          border-radius: 4px;
          color: #909399;
          
          .el-icon {
            font-size: 24px;
            margin-bottom: 5px;
          }
          
          span {
            font-size: 12px;
          }
        }
      }
      
      .status-tag {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 2px 8px;
        
        .el-icon {
          margin-right: 2px;
        }
      }
      
      .action-column {
        display: flex;
        justify-content: center;
        gap: 8px;
        
        .action-link {
          display: flex;
          align-items: center;
          
          .el-icon {
            margin-right: 4px;
          }
        }
      }
    }
    
    .pagination-container {
      padding: 15px 20px;
      display: flex;
      justify-content: flex-end;
      border-top: 1px solid #ebeef5;
      
      .custom-pagination {
        padding: 0;
        margin: 0;
      }
    }
  }
  
  // 详情对话框样式
  .detail-dialog {
    :deep(.el-dialog__header) {
      border-bottom: 1px solid #ebeef5;
      padding: 15px 20px;
      margin: 0;
    }
    
    :deep(.el-dialog__body) {
      padding: 20px;
    }
    
    :deep(.el-dialog__footer) {
      border-top: 1px solid #ebeef5;
      padding: 15px 20px;
    }
  }
  
  // 处理对话框样式
  .process-dialog {
    :deep(.el-dialog__header) {
      border-bottom: 1px solid #ebeef5;
      padding: 15px 20px;
      margin: 0;
    }
    
    :deep(.el-dialog__body) {
      padding: 20px;
    }
    
    :deep(.el-dialog__footer) {
      border-top: 1px solid #ebeef5;
      padding: 15px 20px;
    }
    
    .process-dialog-header {
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      padding-bottom: 15px;
      border-bottom: 1px dashed #ebeef5;
      
      .process-icon {
        color: #409eff;
        font-size: 20px;
        margin-right: 8px;
      }
      
      span {
        font-size: 16px;
        color: #303133;
      }
    }
    
    .process-form {
      .process-input {
        font-family: inherit;
      }
    }
  }
  
  // 记录详情样式 - 保持原样
  .record-detail {
    .info-card {
      margin-bottom: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
      overflow: hidden;
      border: 1px solid #ebeef5;
      
      .info-header {
        background-color: #f5f7fa;
        padding: 12px 20px;
        border-bottom: 1px solid #ebeef5;
        
        h3 {
          margin: 0;
          color: #303133;
          font-size: 16px;
          font-weight: 600;
        }
      }
      
      .info-content {
        padding: 20px;
        background-color: #fff;
      }
    }
    
    .detail-container {
      display: flex;
      gap: 20px;
      margin-bottom: 20px;
      
      .detail-left {
        flex: 1;
        min-width: 300px;
      }
      
      .detail-right {
        flex: 1;
        min-width: 300px;
      }
    }
    
    .section-header {
      display: flex;
      align-items: center;
      margin-bottom: 15px;
      padding-bottom: 8px;
      border-bottom: 1px solid #ebeef5;
      
      .el-icon {
        color: #409eff;
        margin-right: 8px;
      }
      
      h3, h4 {
        margin: 0;
        color: #303133;
        font-size: 16px;
        font-weight: 600;
      }
      
      &.sub-header {
        margin-top: 20px;
        border-bottom-style: dashed;
        
        h4 {
          font-size: 15px;
        }
      }
    }
    
    .image-section, .result-detail, .process-detail {
      border-radius: 8px;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
      background-color: #fff;
      overflow: hidden;
      border: 1px solid #ebeef5;
      padding: 20px;
    }
    
    .image-wrapper {
      width: 100%;
      height: 360px;
      display: flex;
      justify-content: center;
      align-items: center;
      border-radius: 8px;
      overflow: hidden;
      background-color: #f8f8f8;
      border: 1px solid #ebeef5;
      
      .detection-image,
      .record-process-image {
        width: 100%;
        height: 100%;
        object-fit: contain;
      }
    }
    
    .high-level-objects,
    .detected-objects,
    .violence-results,
    .person-groups,
    .traffic-groups,
    .group-images {
      margin-top: 20px;
      
      h4 {
        display: flex;
        align-items: center;
        color: #606266;
        font-size: 14px;
        margin-bottom: 10px;
        
        .el-icon {
          margin-right: 5px;
        }
      }
    }
    
    .traffic-groups {
      .traffic-groups-table {
        width: 100%;
        
        :deep(.el-table__header) {
          th {
            background-color: #f5f7fa;
            color: #606266;
            font-weight: 600;
            text-align: center;
          }
        }
        
        :deep(.el-table__body) {
          td {
            text-align: center;
            vertical-align: middle;
          }
        }
        
        .bbox-text {
          font-family: 'Courier New', monospace;
          font-size: 12px;
          color: #606266;
          background-color: #f8f9fa;
          padding: 4px 8px;
          border-radius: 4px;
          border: 1px solid #e4e7ed;
        }
      }
    }
    
    .group-images {
      .group-images-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 15px;
      }
      
      .group-image-card {
        border: 1px solid #e4e7ed;
        border-radius: 8px;
        overflow: hidden;
        background-color: #fff;
        transition: all 0.3s ease;
        
        &:hover {
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          transform: translateY(-2px);
        }
        
        .group-image-header {
          padding: 12px 16px;
          background-color: #f5f7fa;
          border-bottom: 1px solid #e4e7ed;
          display: flex;
          justify-content: space-between;
          align-items: center;
          
          .group-title {
            font-weight: 600;
            color: #303133;
            font-size: 14px;
          }
        }
        
        .group-image-content {
          height: 250px;
          position: relative;
          background-color: #f8f9fa;
          
          .group-image {
            width: 100%;
            height: 100%;
            cursor: pointer;
          }
          
          .image-error,
          .image-loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #909399;
            background-color: #f9f9f9;
            
            .el-icon {
              font-size: 24px;
              margin-bottom: 8px;
            }
            
            span {
              font-size: 12px;
            }
          }
          
          .image-loading {
            color: #409eff;
            
            .el-icon.is-loading {
              animation: rotating 2s linear infinite;
            }
          }
        }
      }
    }
    
    .process-detail {
      margin-top: 20px;
      
      .process-content {
        margin-top: 5px;
      }
      
      .process-message {
        padding: 12px;
        line-height: 1.6;
        background-color: #f9f9f9;
        border-radius: 4px;
        min-height: 60px;
        white-space: pre-line;
      }
      
      .process-image-container {
        margin-top: 20px;
      }
    }
    
    .description-content {
      :deep(.el-descriptions-item__content) {
        padding: 0 !important;
      }
    }
    
    :deep(.el-progress-bar__innerText) {
      font-size: 12px;
    }
    
    h4 {
      font-weight: 600;
      color: #606266;
    }
  }
  
  .mr-5 {
    margin-right: 5px;
  }
  
  :deep(.el-descriptions__label) {
    width: 120px;
  }
  
  :deep(.el-table) {
    --el-table-header-bg-color: #f5f7fa;
  }
  
  .process-image-uploader {
    width: 100%;
    margin-bottom: 15px;
    
    .el-upload__tip {
      font-size: 12px;
      color: #909399;
      margin-top: 5px;
    }
  }
  
  .process-image-preview {
    margin-top: 15px;
    border: 1px dashed #dcdfe6;
    border-radius: 4px;
    padding: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    min-height: 300px;
    background-color: #f9f9f9;
    box-sizing: border-box;
  }
  
  :deep(.el-image-viewer__mask) {
    opacity: 0.8;
  }
  
  :deep(.el-image-viewer__wrapper) {
    z-index: 9999 !important;
  }
}

// 旋转动画
@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

// 响应式布局
@media (max-width: 1200px) {
  .detection-record-container {
    .search-card {
      .search-content {
        .el-form {
          .date-picker {
            width: 300px;
          }
        }
      }
    }
    
    .record-detail {
      .detail-container {
        flex-direction: column;
        
        .detail-left,
        .detail-right {
          width: 100%;
        }
      }
      
      .group-images {
        .group-images-grid {
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 16px;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .detection-record-container {
    .page-header-card {
      flex-direction: column;
      align-items: flex-start;
      
      .page-title {
        margin-bottom: 15px;
      }
      
      .action-buttons {
        width: 100%;
        justify-content: space-between;
      }
    }
    
    .search-card {
      .search-content {
        .el-form {
          flex-direction: column;
          
          .el-form-item {
            width: 100%;
            margin-right: 0;
          }
          
          .search-select,
          .date-picker {
            width: 100%;
          }
          
          .search-buttons {
            width: 100%;
            justify-content: space-between;
          }
        }
      }
    }
    
    .record-detail {
      .group-images {
        .group-images-grid {
          grid-template-columns: 1fr;
          gap: 12px;
        }
        
        .group-image-card {
          .group-image-content {
            height: 220px;
          }
        }
      }
    }
  }
}
</style> 