# 后端微服务说明

本模块（`services/backend`）为基于 **Java 21** 和 **Spring Boot 3** 的后端服务，负责系统业务逻辑处理、数据库交互及API接口提供。

## 架构说明
本服务遵循经典的 Spring Boot 分层开发范式，确保业务逻辑与数据访问解耦：

*   **表现层 (`controller`)**: 处理 HTTP 请求与响应封装 (`Result<T>`)。
*   **业务层 (`service`)**: 核心逻辑处理，接口定义与实现 (`impl/`) 分离。
*   **数据访问层 (`mapper`)**: 基于 **MyBatis-Plus**，负责数据库交互。
*   **配置层 (`config`)**: 处理安全（Spring Security/JWT）、跨域、全局异常等。

## 核心技术栈
*   **核心框架**: Spring Boot 3.2.1
*   **编程语言**: Java 21
*   **持久化**: MyBatis Plus 3.5.5
*   **数据库**: MySQL 8.0
*   **安全**: Spring Security, JWT 0.12.5
*   **工具**: Hutool 5.8.25, Lombok 1.18.30

## 快速运行
请确保已配置好 `JDK 21+` 与 `MySQL 8.0+` 环境。

1. **数据库初始化**: 运行 `src/main/resources/sql/init.sql`。
2. **配置文件**: 根据实际环境编辑 `src/main/resources/application.yml`（配置数据库连接等）。
3. **构建与运行**:
   ```bash
   mvn clean package
   java -jar target/backend-service.jar
   ```

## 开发规范
- **代码分层**: 必须严格遵循 `Controller` -> `Service` -> `Mapper` 的调用链路。
- **业务实现**: 新业务逻辑优先在 `service/impl/` 中实现。
- **项目结构**: 详见根目录下的结构说明。

*更多开发细节请参考根目录 `AGENTS.md` 及 `docs/` 文档库。*
