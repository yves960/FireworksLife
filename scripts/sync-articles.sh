#!/bin/bash
# sync-articles.sh - 将 workspace-director/articles 同步到 FireworksLife 博客
# 用法: ./scripts/sync-articles.sh

ARTICLES_DIR="/Users/sy/.openclaw/workspace-director/articles"
BLOG_DIR="/Users/sy/Projects/self/FireworksLife/frontend/src/content/blog"

echo "📚 开始同步文章..."
echo "源目录: $ARTICLES_DIR"
echo "目标目录: $BLOG_DIR"

# 确保目标目录存在
mkdir -p "$BLOG_DIR"

# 排除的目录（子目录文章太多，暂时不处理）
EXCLUDE_DIRS="ai-assisted-dev-specs ai-replacement-series"

count=0

# 遍历顶级 markdown 文件
for file in "$ARTICLES_DIR"/*.md; do
  [ -f "$file" ] || continue
  
  filename=$(basename "$file")
  
  # 跳过 README
  if [ "$filename" = "README.md" ]; then
    continue
  fi
  
  # 检查是否已迁移
  blog_file="$BLOG_DIR/$filename"
  if [ -f "$blog_file" ]; then
    echo "⏭️  跳过（已存在）: $filename"
    continue
  fi
  
  # 提取标题和日期
  title=$(head -1 "$file" | sed 's/^# //' | sed 's/"/\\"/g')
  date=$(echo "$filename" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1 || echo "2026-03-30")
  
  # 创建带 frontmatter 的文件
  cat > "$blog_file" << FRONTMATTER
---
title: "${title}"
description: "${title}"
pubDate: ${date}
category: "技术"
tags: ["AI", "开发"]
---

FRONTMATTER
  
  # 追加内容（去掉第一个 H1）
  tail -n +2 "$file" >> "$blog_file"
  
  echo "✅ 已同步: $filename"
  count=$((count + 1))
done

echo ""
echo "✨ 完成！共同步 $count 篇文章"
echo ""
echo "下一步:"
echo "  1. cd frontend && npm run build  # 本地测试"
echo "  2. git add . && git commit -m 'chore: sync new articles'"
echo "  3. git push  # 推送到 GitHub，Netlify 自动部署"
