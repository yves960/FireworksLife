# 轻量级博客系统

一个简洁、快速的博客系统，支持Markdown内容、评论、点赞、多种登录方式（用户名/邮箱/微信OAuth）。

## 技术栈

### 后端
- **FastAPI** - 现代化的Python Web框架
- **SQLAlchemy** - ORM数据库操作
- **SQLite** - 轻量级数据库（支持WAL模式）
- **Pydantic** - 数据验证和序列化
- **JWT** - 认证授权
- **Passlib** - 密码哈希

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 快速的前端构建工具
- **Vue Router** - 路由管理
- **Pinia** - 状态管理
- **Axios** - HTTP客户端

## 功能特性

### 已实现
- ✅ 用户注册和登录（用户名/邮箱）
- ✅ JWT认证和权限验证
- ✅ "记住我"功能
- ✅ 文章CRUD操作
- ✅ 文章列表和分页
- ✅ 评论系统（支持嵌套回复）
- ✅ 点赞功能
- ✅ 数据库备份

### 计划中
- ⏳ 邮箱验证
- ⏳ 微信OAuth登录
- ⏳ 炫酷视觉效果（渐变背景、粒子动画等）
- ⏳ 深色模式
- ⏳ 响应式设计
- ⏳ 管理后台

## Python版本要求

**推荐版本**: Python 3.11 或 3.12

**注意**: Python 3.14 非常新，可能存在兼容性问题。详见 [backend/PYTHON_VERSION.md](backend/PYTHON_VERSION.md)

## 快速开始

### 后端

**方法1: 使用安装脚本（推荐）**
```bash
cd backend
./install.sh
```

**方法2: 手动安装**
```bash
cd backend

# 创建虚拟环境
python3.11 -m venv .venv  # 或 python3.12

# 激活虚拟环境
source .env/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置必要的参数

# 初始化数据库
python -m app.db.init_db

# 运行开发服务器
python run.py
```

后端API将在 http://localhost:8000 运行

**Docker方式（无需Python版本问题）**
```bash
docker-compose up -d
```

详见 [backend/INSTALL.md](backend/INSTALL.md)

### 前端

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑.env文件，配置API地址
```

3. 运行开发服务器：
```bash
npm run dev
```

前端应用将在 http://localhost:3000 运行

### 使用Docker

1. 构建并启动所有服务：
```bash
docker-compose up -d
```

2. 查看日志：
```bash
docker-compose logs -f
```

3. 停止服务：
```bash
docker-compose down
```

## API文档

启动后端服务后，访问以下地址查看自动生成的API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 数据库备份

手动备份数据库：
```bash
cd backend
python -m app.db.backup
```

建议设置定期备份（如使用cron job）。

## 项目结构

```
.
├── backend/              # 后端代码
│   ├── app/
│   │   ├── api/        # API路由
│   │   ├── models/     # 数据库模型
│   │   ├── schemas/    # Pydantic模型
│   │   ├── core/       # 核心配置
│   │   └── db/         # 数据库配置
│   ├── requirements.txt
│   └── run.py
├── frontend/            # 前端代码
│   ├── src/
│   │   ├── components/ # Vue组件
│   │   ├── views/      # 页面组件
│   │   ├── router/     # 路由配置
│   │   ├── store/      # 状态管理
│   │   └── api/        # API调用
│   ├── package.json
│   └── vite.config.js
└── docker-compose.yml   # Docker配置
```

## 故障排除

### 后端安装失败

**Python版本问题**
- 推荐使用Python 3.11或3.12
- Python 3.14可能不兼容，详见 [backend/PYTHON_VERSION.md](backend/PYTHON_VERSION.md)

**pip安装错误**
```bash
# 升级pip
pip install --upgrade pip setuptools wheel

# 清除缓存重新安装
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

### 依赖编译错误

**Ubuntu/Debian**
```bash
sudo apt-get install python3-dev build-essential
```

**macOS**
```bash
xcode-select --install
```

### 数据库问题

如果遇到SQLite WAL模式错误，确保SQLite版本 >= 3.7.0

```bash
# 检查SQLite版本
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

## 更多帮助

- [backend/INSTALL.md](backend/INSTALL.md) - 详细安装说明
- [backend/PYTHON_VERSION.md](backend/PYTHON_VERSION.md) - Python版本兼容性

## 许可证

MIT License
