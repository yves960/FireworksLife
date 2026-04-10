#!/bin/bash

# ==================== FireworksLife 部署脚本 ====================

set -e

echo "🚀 开始部署 FireworksLife..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker 已安装"

# 检查 .env 文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}!${NC} .env 文件不存在，从示例创建..."
    cp .env.example .env
    echo -e "${YELLOW}!${NC} 请编辑 .env 文件配置密钥"
fi

# 生成随机密钥（如果没有）
if grep -q "your-secret-key-here" .env; then
    echo -e "${YELLOW}!${NC} 生成随机密钥..."
    SECRET_KEY=$(openssl rand -hex 32)
    JWT_SECRET=$(openssl rand -hex 32)
    
    # macOS 和 Linux 兼容的 sed
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/your-secret-key-here/$SECRET_KEY/" .env
        sed -i '' "s/your-jwt-secret-here/$JWT_SECRET/" .env
    else
        sed -i "s/your-secret-key-here/$SECRET_KEY/" .env
        sed -i "s/your-jwt-secret-here/$JWT_SECRET/" .env
    fi
    echo -e "${GREEN}✓${NC} 密钥已生成"
fi

# 停止旧容器
echo "🛑 停止旧容器..."
docker-compose down 2>/dev/null || true

# 构建镜像
echo "🔨 构建 Docker 镜像..."
docker-compose build

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查状态
echo ""
echo "📊 服务状态:"
docker-compose ps

# 初始化数据库（如果需要）
echo ""
echo -e "${YELLOW}提示: 如果是首次部署，请初始化数据库:${NC}"
echo "  docker-compose exec backend python -m app.db.init_db"

echo ""
echo -e "${GREEN}✅ 部署完成!${NC}"
echo ""
echo "🌐 访问地址:"
echo "   http://localhost"
echo ""
echo "📝 常用命令:"
echo "   查看日志:   docker-compose logs -f"
echo "   重启服务:   docker-compose restart"
echo "   停止服务:   docker-compose down"
echo "   进入后端:   docker-compose exec backend bash"