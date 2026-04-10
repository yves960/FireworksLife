# Web 博客系统部署指南

本指南帮助你将 FireworksLife 部署到云服务器。

## 📋 准备工作

### 1. 购买云服务器

推荐配置：
- **CPU**: 1核以上
- **内存**: 1GB以上
- **硬盘**: 20GB以上
- **系统**: Ubuntu 22.04 / Debian 12 / CentOS 8

主流云服务商：
- 阿里云 ECS
- 腾讯云 CVM
- 华为云 ECS
- AWS EC2
- DigitalOcean Droplet

### 2. 域名（可选但推荐）

- 阿里云、腾讯云、Cloudflare 等都可以购买
- 配置 DNS 解析到服务器 IP

---

## 🔧 服务器配置

### 1. 连接服务器

```bash
ssh root@your-server-ip
```

### 2. 安装 Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh

# 启动 Docker
systemctl start docker
systemctl enable docker

# 安装 Docker Compose
apt install docker-compose-plugin
# 或
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 3. 创建应用目录

```bash
mkdir -p /opt/fireworkslife
cd /opt/fireworkslife
```

---

## 📦 部署应用

### 方式一：上传代码

在本地电脑打包项目：

```bash
cd /Users/sy/Projects/FireworksLife
tar -czvf fireworkslife.tar.gz \
  --exclude='node_modules' \
  --exclude='.venv' \
  --exclude='__pycache__' \
  --exclude='.git' \
  .
```

上传到服务器：

```bash
scp fireworkslife.tar.gz root@your-server-ip:/opt/fireworkslife/
```

在服务器解压：

```bash
cd /opt/fireworkslife
tar -xzvf fireworkslife.tar.gz
```

### 方式二：Git 克隆（推荐）

```bash
cd /opt
git clone https://github.com/your-username/FireworksLife.git
cd FireworksLife
```

### 配置环境变量

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置
nano .env
```

修改以下内容：
```
SECRET_KEY=随机生成的密钥
JWT_SECRET=随机生成的JWT密钥
```

生成密钥：
```bash
openssl rand -hex 32
```

### 运行部署脚本

```bash
chmod +x deploy.sh
./deploy.sh
```

### 初始化数据库

```bash
docker-compose exec backend python -m app.db.init_db
```

---

## 🌐 配置域名和 HTTPS

### 使用 Nginx + Let's Encrypt

创建 `nginx-proxy` 目录：

```bash
mkdir -p /opt/nginx-proxy
cd /opt/nginx-proxy
```

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  nginx-proxy:
    image: nginxproxy/nginx-proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./certs:/etc/nginx/certs
      - ./html:/usr/share/nginx/html
      - ./vhost:/etc/nginx/vhost.d
      - /var/run/docker.sock:/tmp/docker.sock:ro

  acme-companion:
    image: nginxproxy/acme-companion
    restart: unless-stopped
    volumes_from:
      - nginx-proxy
    volumes:
      - ./acme:/etc/acme.sh
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

启动代理：

```bash
docker-compose up -d
```

修改 FireworksLife 的 `docker-compose.yml`：

```yaml
services:
  frontend:
    # ... 其他配置
    environment:
      - VIRTUAL_HOST=your-domain.com
      - LETSENCRYPT_HOST=your-domain.com
      - LETSENCRYPT_EMAIL=your-email@example.com
    # 移除 ports 映射，让 nginx-proxy 处理
    expose:
      - "80"
```

---

## 📊 常用命令

```bash
# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh

# 更新代码后重新部署
git pull
docker-compose build
docker-compose up -d
```

---

## 🔒 安全建议

1. **修改 SSH 端口**
   ```bash
   nano /etc/ssh/sshd_config
   # Port 22 → Port 2222
   systemctl restart sshd
   ```

2. **配置防火墙**
   ```bash
   # Ubuntu (ufw)
   ufw allow 80
   ufw allow 443
   ufw allow 2222/tcp
   ufw enable
   ```

3. **定期备份数据库**
   ```bash
   # 备份 SQLite
   cp /opt/fireworkslife/backend/data/blog.db /backup/blog-$(date +%Y%m%d).db
   ```

4. **使用非 root 用户运行**
   ```bash
   adduser deploy
   usermod -aG docker deploy
   ```

---

## ❓ 常见问题

### Q: 端口被占用？

```bash
# 查看端口占用
lsof -i :80

# 修改 docker-compose.yml 中的端口映射
```

### Q: 容器启动失败？

```bash
# 查看日志
docker-compose logs

# 检查配置
docker-compose config
```

### Q: 数据库丢失？

SQLite 数据存储在 Docker volume 中，确保使用 volume 持久化：

```bash
# 查看 volume
docker volume ls

# 备份 volume
docker run --rm -v fireworkslife_backend-data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz /data
```

---

## 📞 需要帮助？

- 查看项目 README.md
- 提交 Issue 到 GitHub
- 加入社区讨论