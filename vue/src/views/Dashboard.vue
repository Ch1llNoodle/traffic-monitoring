<!-- 仪表盘页面 -->
<template>
  <div class="dashboard">
    <div class="welcome-section">
      <div class="welcome-header">
        <div class="welcome-info">
          <h1 class="welcome-title">智慧交通监控预警系统</h1>
          <p class="welcome-subtitle">
            欢迎回来，<strong>{{ userInfo?.realName || userInfo?.username }}</strong>
          </p>
          <p class="current-date">{{ currentDate }}</p>
        </div>
        <div class="welcome-icon">
          <el-icon :size="80" color="#3b82f6"><Monitor /></el-icon>
        </div>
      </div>
    </div>
    
    <div class="quick-actions">
      <h3>快速操作</h3>
      <el-row :gutter="30">
        <el-col :span="6">
                     <el-card shadow="hover" class="action-card" @click="navigateTo('/monitor')">
             <div class="action-content">
               <el-icon :size="32" color="#059669"><Monitor /></el-icon>
               <h4>实时监控</h4>
               <p>查看交通监控画面</p>
             </div>
           </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="action-card" @click="navigateTo('/camera')">
            <div class="action-content">
              <el-icon :size="32" color="#1e40af"><VideoCamera /></el-icon>
              <h4>监控设备</h4>
              <p>管理监控摄像头</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="action-card" @click="navigateTo('/detection/record')">
            <div class="action-content">
              <el-icon :size="32" color="#dc2626"><Warning /></el-icon>
              <h4>交通记录</h4>
              <p>查看检测记录</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="action-card" @click="navigateTo('/profile')">
            <div class="action-content">
              <el-icon :size="32" color="#ea580c"><User /></el-icon>
              <h4>个人中心</h4>
              <p>管理个人信息</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 系统介绍 -->
    <div class="system-intro">
      <el-row :gutter="24">
        <el-col :span="16">
          <el-card shadow="hover" class="intro-card">
            <template #header>
              <div class="card-header">
                <el-icon :size="24" color="#3b82f6"><InfoFilled /></el-icon>
                <h3>关于智慧交通监控预警系统</h3>
              </div>
            </template>
            <div class="intro-content">
              <p class="intro-text">
                智慧交通监控预警系统是一套基于人工智能技术的智能交通监控解决方案，专为道路交通管理设计。
                系统通过先进的计算机视觉算法，能够实时分析交通监控画面，自动识别潜在的危险驾驶行为，
                为道路交通安全提供24小时不间断的智能监控。
              </p>
              <div class="intro-features">
                <div class="feature-item">
                  <el-icon color="#059669"><CircleCheckFilled /></el-icon>
                  <span>实时AI智能分析，快速响应</span>
                </div>
                <div class="feature-item">
                  <el-icon color="#059669"><CircleCheckFilled /></el-icon>
                  <span>多场景适应，覆盖城市道路、高速公路、交叉口</span>
                </div>
                <div class="feature-item">
                  <el-icon color="#059669"><CircleCheckFilled /></el-icon>
                  <span>自动记录证据，便于事后追溯</span>
                </div>
                <div class="feature-item">
                  <el-icon color="#059669"><CircleCheckFilled /></el-icon>
                  <span>多级预警机制，确保及时响应</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="stats-card">
            <template #header>
              <div class="card-header">
                <el-icon :size="24" color="#dc2626"><TrendCharts /></el-icon>
                <h3>系统优势</h3>
              </div>
            </template>
            <div class="stats-content">
              <div class="stat-item">
                <div class="stat-number">99.2%</div>
                <div class="stat-label">识别准确率</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">&lt;500ms</div>
                <div class="stat-label">响应时间</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-label">全天候监控</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">0</div>
                <div class="stat-label">人工盲区</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 核心功能特色 -->
    <div class="core-features">
      <h3>核心功能特色</h3>
      <el-row :gutter="30">
        <el-col :span="8">
          <el-card shadow="hover" class="feature-card">
            <div class="feature-content">
              <div class="feature-icon ai-icon">
                <el-icon :size="40" color="#3b82f6"><Cpu /></el-icon>
              </div>
              <h4>AI智能识别</h4>
              <p>采用YOLO+多模态大语言模型算法，能够准确识别超速、变道违规、跟车过近等危险驾驶行为，有效降低误报率</p>
              <ul class="feature-list">
                <li>车辆行为分析</li>
                <li>驾驶模式识别</li>
                <li>交通情境智能判断</li>
              </ul>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="feature-card">
            <div class="feature-content">
              <div class="feature-icon realtime-icon">
                <el-icon :size="40" color="#10b981"><Clock /></el-icon>
              </div>
              <h4>实时预警</h4>
              <p>检测到异常情况立即发出预警，支持多种通知方式，确保相关人员第一时间获得信息</p>
              <ul class="feature-list">
                <li>即时弹窗提醒</li>
                <li>短信通知推送</li>
                <li>目标画面截取</li>
              </ul>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="feature-card">
            <div class="feature-content">
              <div class="feature-icon evidence-icon">
                <el-icon :size="40" color="#f59e0b"><FolderOpened /></el-icon>
              </div>
              <h4>证据保全</h4>
              <p>自动截取关键画面和录像片段，建立完整的事件档案，为后续处理提供可靠依据</p>
              <ul class="feature-list">
                <li>画面截取</li>
                <li>视频片段保存</li>
                <li>时间戳标记</li>
              </ul>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 安全保障 -->
    <div class="security-section">
      <el-card shadow="hover" class="security-card">
        <div class="security-content">
          <div class="security-header">
                         <el-icon :size="48" color="#fbbf24"><Setting /></el-icon>
            <div class="security-text">
              <h3>构建智慧交通，守护每一个出行者</h3>
              <p>让技术成为交通的守护者，为每一个道路使用者创造安全的出行环境</p>
            </div>
          </div>
          <div class="security-benefits">
            <div class="benefit-item">
              <strong>预防为主</strong>
              <span>通过智能监控威慑危险驾驶行为</span>
            </div>
            <div class="benefit-item">
              <strong>快速响应</strong>
              <span>缩短交通违法处理时间</span>
            </div>
            <div class="benefit-item">
              <strong>减轻负担</strong>
              <span>降低交警人工监管压力</span>
            </div>
            <div class="benefit-item">
              <strong>提升效率</strong>
              <span>优化道路交通安全管理</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Monitor, VideoCamera, Warning, User, InfoFilled, CircleCheckFilled, TrendCharts, Cpu, Clock, FolderOpened, Setting } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 用户信息
const userInfo = computed(() => userStore.userInfo)

// 当前日期
const currentDate = new Date().toLocaleDateString('zh-CN', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  weekday: 'long'
})

// 导航函数
const navigateTo = (path: string) => {
  router.push(path)
}


</script>

<style scoped>
.dashboard {
  padding: 32px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
  min-height: calc(100vh - 64px);
}

.welcome-section {
  margin-bottom: 32px;
}

.welcome-header {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #6366f1 100%);
  border-radius: 20px;
  padding: 40px;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 12px 40px rgba(30, 64, 175, 0.25);
  position: relative;
  overflow: hidden;
}

.welcome-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100"><path d="M0,0 C150,100 350,0 500,50 C650,100 850,0 1000,50 L1000,0 Z" fill="rgba(255,255,255,0.1)"/></svg>');
  background-size: cover;
  opacity: 0.3;
}

.welcome-info {
  flex: 1;
  position: relative;
  z-index: 1;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-subtitle {
  font-size: 18px;
  margin: 0 0 8px 0;
  opacity: 0.9;
}

.current-date {
  font-size: 14px;
  margin: 0;
  opacity: 0.8;
}

.welcome-icon {
  opacity: 0.3;
  position: relative;
  z-index: 1;
}

.quick-actions {
  margin-bottom: 50px;
  
  h3 {
    font-size: 20px;
    color: #1e40af;
    margin-bottom: 20px;
    font-weight: 600;
  }
}

.action-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  border-radius: 16px;
  overflow: hidden;
  
  &:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.15);
    border-color: #1e40af;
  }
}

.action-content {
  text-align: center;
  padding: 32px 24px;
  
  h4 {
    margin: 20px 0 12px 0;
    font-size: 18px;
    color: #1f2937;
    font-weight: 600;
  }
  
  p {
    margin: 0;
    color: #6b7280;
    font-size: 14px;
    line-height: 1.5;
  }
}

/* 系统介绍部分 */
.system-intro {
  margin-bottom: 40px;
}

.intro-card, .stats-card {
  height: 100%;
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  }
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  
  h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #1f2937;
  }
}

.intro-content {
  .intro-text {
    font-size: 15px;
    line-height: 1.8;
    color: #4b5563;
    margin-bottom: 24px;
  }
}

.intro-features {
  .feature-item {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
    font-size: 14px;
    color: #374151;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
}

.stats-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 16px;
  border: 1px solid rgba(59, 130, 246, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
  }
  
  .stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #1e40af;
    margin-bottom: 8px;
  }
  
  .stat-label {
    font-size: 13px;
    color: #6b7280;
    font-weight: 500;
  }
}

/* 核心功能特色 */
.core-features {
  margin-bottom: 50px;
  
  h3 {
    font-size: 20px;
    color: #1e40af;
    margin-bottom: 20px;
    font-weight: 600;
  }
}

.feature-card {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  
  &:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.12);
  }
}

.feature-content {
  text-align: center;
  padding: 32px 24px;
  
  .feature-icon {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 24px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    
    &.ai-icon {
      background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 50%, #a855f7 100%);
      color: white;
    }
    
    &.realtime-icon {
      background: linear-gradient(135deg, #0891b2 0%, #06b6d4 50%, #22d3ee 100%);
      color: white;
    }
    
    &.evidence-icon {
      background: linear-gradient(135deg, #ea580c 0%, #f97316 50%, #fb923c 100%);
      color: white;
    }
  }
  
  h4 {
    font-size: 18px;
    font-weight: 600;
    color: #1f2937;
    margin: 0 0 12px 0;
  }
  
  p {
    font-size: 14px;
    color: #6b7280;
    line-height: 1.6;
    margin: 0 0 16px 0;
  }
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
  
  li {
    font-size: 13px;
    color: #4b5563;
    padding: 4px 0;
    position: relative;
    padding-left: 16px;
    
    &:before {
      content: '•';
      color: #1e40af;
      font-weight: bold;
      position: absolute;
      left: 0;
    }
  }
}

/* 安全保障部分 */
.security-section {
  margin-bottom: 30px;
}

.security-card {
  background: linear-gradient(135deg, #fef3c7 0%, #fef7cd 100%);
  border: 1px solid #fbbf24;
  
  :deep(.el-card__body) {
    padding: 30px;
  }
}

.security-content {
  .security-header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 30px;
    
    .security-text {
      h3 {
        font-size: 24px;
        font-weight: 700;
        color: #92400e;
        margin: 0 0 8px 0;
      }
      
      p {
        font-size: 16px;
        color: #a16207;
        margin: 0;
      }
    }
  }
}

.security-benefits {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
}

.benefit-item {
  background: rgba(255, 255, 255, 0.7);
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  border: 1px solid rgba(251, 191, 36, 0.3);
  
  strong {
    display: block;
    font-size: 16px;
    color: #92400e;
    margin-bottom: 8px;
    font-weight: 600;
  }
  
  span {
    font-size: 14px;
    color: #a16207;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-content {
    grid-template-columns: 1fr;
  }
  
  .security-header {
    flex-direction: column;
    text-align: center;
    gap: 15px !important;
  }
  
  .security-benefits {
    grid-template-columns: 1fr !important;
  }
  
  .feature-icon {
    width: 60px !important;
    height: 60px !important;
  }
}
</style> 