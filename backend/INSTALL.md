# 后端安装说明

## Python版本要求

**推荐版本**: Python 3.11 或 3.12

**注意**: Python 3.14 非常新（2024年发布），某些第三方库可能还没有完全兼容。如果遇到安装问题，建议使用Python 3.11或3.12。

## 安装步骤

### 方法1: 使用安装脚本（推荐）

```bash
cd backend
./install.sh
```

### 方法2: 手动安装

```bash
cd backend

# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 升级pip
pip install --upgrade pip setuptools wheel

# 安装依赖
pip install -r requirements.txt
```

## 已知的Python 3.14兼容性问题

如果你使用Python 3.14，可能会遇到以下问题：

1. **某些包编译失败**
   - 解决：使用`--no-binary`选项从源码安装
   - 或者降级到Python 3.11/3.12

2. **pydantic-settings导入问题**
   - 已修复：使用`pydantic_settings`（下划线）而不是`pydantic-settings`（连字符）

3. **Config类语法变化**
   - 已修复：使用`model_config = {"from_attributes": True}`而不是`class Config: from_attributes = True`

## 环境变量配置

安装完成后，配置环境变量：

```bash
# 复制示例文件
cp .env.example .env

# 编辑.env文件，修改以下配置：
# - SECRET_KEY: 生成一个随机密钥
# - JWT_SECRET: 生成JWT密钥
# - （可选）SMTP配置（用于邮件验证）
# - （可选）微信OAuth配置
```

## 初始化数据库

```bash
# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 初始化数据库
python -m app.db.init_db
```

## 运行后端服务

```bash
# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 启动服务
python run.py
```

服务将在 http://localhost:8000 启动

API文档:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 常见问题

### 问题1: pip install失败

**错误信息**: `subprocess-exited-with-error`

**解决方案**:
1. 升级pip: `pip install --upgrade pip`
2. 安装构建工具:
   - Ubuntu/Debian: `sudo apt-get install python3-dev build-essential`
   - macOS: `xcode-select --install`
3. 或使用预编译包: `pip install --only-binary :all: -r requirements.txt`

### 问题2: Python版本不兼容

**错误信息**: `No matching distribution found`

**解决方案**:
使用Python 3.11或3.12:
```bash
# 使用pyenv安装Python 3.12
pyenv install 3.12.0
pyenv local 3.12.0

# 或使用conda
conda create -n blog python=3.12
conda activate blog
```

### 问题3: SQLite WAL模式错误

**错误信息**: `sqlite3.OperationalError: database is locked`

**解决方案**:
确保使用SQLite 3.7.0或更高版本，WAL模式在3.7.0+才支持。Python 3.x通常自带SQLite 3.x，应该不会有问题。

## 使用Docker（替代方案）

如果本地安装遇到问题，可以使用Docker：

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 停止
docker-compose down
```

## 开发工具推荐

- **IDE**: PyCharm, VS Code
- **代码格式化**: Black
- **代码检查**: flake8, mypy
- **测试**: pytest

## 下一步

安装完成后：
1. 配置`.env`文件
2. 初始化数据库
3. 启动后端服务
4. 配置前端（见前端README）
5. 启动前端服务

祝开发顺利！
