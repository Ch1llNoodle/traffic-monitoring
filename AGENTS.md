# AGENTS.md (项目AI智能体开发指南)

本文档为在本项目中工作的AI智能体提供开发指南。

## 1. 项目构建、Lint和测试命令

### 1.1 前端 (Vue3 + Vite)
- **安装依赖:** `npm install`
- **开发环境:** `npm run dev`
- **构建:** `npm run build`
- **代码检查:** (如果已配置，例如 `npm run lint`)

### 1.2 后端 (Spring Boot 3 + Java 21)
- **构建:** `mvn clean package`
- **运行测试:** `mvn test`
- **运行单个测试:** `mvn test -Dtest=TestClassName`

### 1.3 算法服务 (Flask + Python)
- **安装依赖:** `pip install -r requirements.txt`
- **运行测试:** `pytest` (或 `python -m unittest discover`)
- **运行单个测试:** `pytest path/to/test_file.py`

---

## 2. 代码风格规范

### 2.1 通用规则
- **命名:** 遵循语言特定的命名约定 (Java类使用CamelCase，JS/TS/Python变量使用camelCase)。
- **注释:** 简洁明了。重点说明*为什么*，而不是*什么*。
- **导入:** 按类型分组导入 (标准库、第三方库、本地模块)。
- **安全密钥:** 严禁提交密钥或API凭证。请使用环境变量。

### 2.2 前端 (Vue/TypeScript)
- 使用 `<script setup>` 的 `Composition API`。
- 所有组件和API调用均使用 TypeScript。
- 为DTO和API响应定义明确的类型。
- 目录结构: `components/`, `views/`, `api/`, `stores/`。

### 2.3 后端 (Java/Spring Boot)
- 使用 Java 21。使用 `Lombok` 减少样板代码。
- 使用 `MyBatis-Plus` 进行数据访问。
- 架构: `Controller` -> `Service` -> `Mapper`。
- 所有API响应均使用 `Result<T>`。

### 2.4 算法服务 (Python/Flask)
- 所有函数签名均使用类型提示 (type hints)。
- 使用 `loguru` 进行日志记录。
- 确保所有AI模型调用均使用 `try-except` 块封装。
- 在 `tests/` 目录下维护单元测试。

---

## 3. 智能体工作流规则

### 3.1 提交信息 (Commit Messages)
- 遵循约定式提交: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`。
- 标题保持在50个字符以内。

### 3.2 文件操作
- **始终**在修改前验证文件是否存在。
- 创建新文件时，遵循既定的文件夹结构。
- **严禁**在未检查 `package.json`, `pom.xml` 或 `requirements.txt` 中现有库的情况下引入新库。

### 3.3 安全性
- **严禁**在代码或提交记录中暴露API密钥或凭证。
- 使用 `.env` 文件进行本地配置 (确保 `.env` 已添加到 `.gitignore` 中)。

---
<!-- AGENTS.md 结束 -->
