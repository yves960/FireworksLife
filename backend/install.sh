#!/bin/bash

# 轻量级博客系统 - 后端依赖安装脚本

echo "开始安装后端依赖..."

# 检查Python版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "当前Python版本: $PYTHON_VERSION"

# 建议使用Python 3.11或3.12
if [[ $PYTHON_VERSION == 3.14* ]]; then
  echo "⚠️  警告: Python 3.14非常新，某些包可能还不兼容"
  echo "建议使用Python 3.11或3.12以获得最佳兼容性"
  echo ""
  read -p "是否继续安装？(y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# 创建虚拟环境
if [ ! -d ".venv" ]; then
  echo "创建虚拟环境..."
  python3 -m venv .venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source .venv/bin/activate

# 升级pip
echo "升级pip..."
pip install --upgrade pip setuptools wheel

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

echo ""
echo "✅ 依赖安装完成！"
echo ""
echo "下一步操作："
echo "1. 复制环境变量文件: cp .env.example .env"
echo "2. 编辑.env文件，配置必要的参数"
echo "3. 初始化数据库: python -m app.db.init_db"
echo "4. 运行后端服务: python run.py"
