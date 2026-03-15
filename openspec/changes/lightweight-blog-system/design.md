## Context

当前市场上的博客系统通常过于复杂，依赖众多第三方服务，性能缓慢，部署困难。我们正在构建一个轻量级、高性能的博客系统，专注于核心功能，易于部署和维护。

### 约束条件
- 必须保持最小依赖
- 支持快速部署
- 低资源消耗
- 易于扩展

## Goals / Non-Goals

**目标：**
- 构建完整的博客文章管理功能（CRUD）
- 支持Markdown格式的内容编辑
- 提供简洁的认证系统
- 实现响应式的前端界面
- 提供管理后台
- 使用轻量级数据库（SQLite）
- 支持RESTful API

**非目标：**
- 不支持复杂的权限管理
- 不集成社交媒体分享（除微信登录外）
- 不支持多用户协作
- 不包含复杂的SEO优化功能

## Decisions

### 技术栈选择

**前端框架：Vue.js**
- 理由：学习曲线平缓，生态丰富，组件化开发
- 替代方案：React（学习成本较高）、Svelte（生态较小）

**后端框架：FastAPI (Python)**
- 理由：自动生成API文档，类型安全，性能优异
- 替代方案：Express.js（Node.js）、Flask（Python）

**数据库：SQLite**
- 理由：零配置，单文件，完全够用，易于备份
- 替代方案：PostgreSQL（过于重量级）、MongoDB（文档型数据库不适合关系数据）

**静态文件服务：Nginx**
- 理由：高性能，稳定，配置简单
- 替代方案：Caddy（自动HTTPS但不成熟）、Apache（过于重量级）

### 架构设计

**前后端分离架构**
- 前端：Vue.js单页应用（SPA）
- 后端：FastAPI提供RESTful API
- 优势：独立开发和部署，易于维护

**部署方案**
- 使用Docker容器化部署
- 支持静态站点生成选项（SSG）以提升性能
- 可选的serverless部署方案

### 认证方案

**JWT Token认证**
- 理由：无状态，跨域友好，易于实现
- 存储方式：HTTP-Only Cookie防止XSS攻击
- 替代方案：Session（需要服务端存储，不适合分布式）

**多方式登录支持**
- 用户名/邮箱登录：传统密码认证
- 微信OAuth2.0登录：第三方授权登录
- 理由：提供多种便捷登录方式，提升用户体验
- 邮箱验证使用SMTP服务（如阿里云邮件推送）
- 微信OAuth使用微信公众平台开放平台能力

### 数据模型设计

**文章表（posts）**
- id (主键)
- title (标题)
- content (Markdown内容)
- author (作者)
- created_at (创建时间)
- updated_at (更新时间)
- tags (标签，JSON格式)
- status (状态：draft/published/archived)
- slug (URL友好的标识符)

**用户表（users）**
- id (主键)
- username (用户名)
- email (邮箱)
- password_hash (密码哈希)
- wechat_openid (微信OpenID，可选)
- wechat_unionid (微信UnionID，可选)
- wechat_nickname (微信昵称，可选)
- wechat_avatar (微信头像URL，可选)
- email_verified (邮箱是否验证，布尔值)
- created_at (创建时间)

**邮箱验证码表（email_verifications）**
- id (主键)
- email (邮箱)
- code (验证码)
- type (验证类型：register/bind)
- expires_at (过期时间)
- created_at (创建时间)

## Risks / Trade-offs

### 已知风险

**SQLite在高并发下的性能限制**
- 风险：SQLite在高并发写入场景下性能可能不足
- 缓解措施：使用WAL模式（Write-Ahead Logging），考虑未来迁移到PostgreSQL的路径

**单点故障**
- 风险：单服务器部署存在单点故障
- 缓解措施：定期数据库备份，使用容器编排平台（如Kubernetes）提高可用性

**Markdown渲染安全性**
- 风险：用户提交的恶意HTML可能导致XSS攻击
- 缓解措施：使用白名单过滤HTML标签，进行严格的输入验证

### 权衡

**功能完整性与开发速度**
- 权衡：优先实现核心功能，暂不包含高级特性（如评论、社交分享）
- 理由：快速交付MVP，根据用户反馈迭代

**性能与开发便利性**
- 权衡：选择SQLite而非PostgreSQL
- 理由：初期数据量不大，SQLite足够，降低部署复杂度

## Migration Plan

### 部署步骤
1. 准备服务器环境（Docker + Nginx）
2. 拉取代码并构建Docker镜像
3. 配置环境变量（数据库路径、密钥等）
4. 运行数据库迁移脚本
5. 启动后端服务
6. 构建前端静态文件
7. 配置Nginx反向代理
8. 创建管理员账户

### 回滚策略
- 保留Docker镜像版本标签，可快速回退到之前版本
- 数据库定期备份（每日）
- 使用蓝绿部署减少停机时间

## Open Questions

- 是否需要支持多语言（i18n）？
- 是否需要集成其他第三方认证（如Google OAuth、GitHub OAuth）？
- 图片存储方案：本地存储还是对象存储服务（如S3）？
- 是否需要实现全文搜索功能？
- 如何处理文章版本历史？
