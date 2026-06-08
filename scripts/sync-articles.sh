#!/bin/bash
# sync-articles.sh - 将 articles 同步到 FireworksLife content 分支
# 用法: ./scripts/sync-articles.sh
# 
# 流程：articles push → FireworksLife sync workflow → content 分支暂存
# 发布：需在 FireworksLife 仓库手动触发 "Deploy to Netlify" workflow

ARTICLES_DIR="$HOME/Projects/self/articles"
BLOG_DIR="$HOME/Projects/self/FireworksLife/frontend/src/content/blog"

echo "📚 开始同步文章..."
echo "源目录: $ARTICLES_DIR"
echo "目标目录: $BLOG_DIR"

mkdir -p "$BLOG_DIR"

count=0

for file in "$ARTICLES_DIR"/*.md; do
  [ -f "$file" ] || continue
  
  filename=$(basename "$file")
  
  if [ "$filename" = "README.md" ]; then
    continue
  fi
  
  title=$(head -1 "$file" | sed 's/^# //' | sed 's/"/\\"/g')
  date=$(echo "$filename" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1 || echo "2026-03-30")
  
  blog_file="$BLOG_DIR/$filename"
  
  # 内容变化才同步
  if [ ! -f "$blog_file" ] || ! diff -q "$file" "$blog_file" > /dev/null 2>&1; then
    {
      echo "---"
      echo "title: \"${title}\""
      echo "description: \"${title}\""
      echo "pubDate: ${date}"
      echo "category: \"技术\""
      echo "tags: [\"AI\", \"开发\"]"
      echo "---"
      echo ""
      tail -n +2 "$file"
    } > "$blog_file"
    echo "✅ 已同步: $filename"
    count=$((count + 1))
  else
    echo "⏭️  未变化: $filename"
  fi
done

echo ""
echo "✨ 完成！共同步 $count 篇文章"
echo ""
echo "下一步:"
echo "  1. cd $HOME/Projects/self/FireworksLife"
echo "  2. git checkout content"
echo "  3. cp ~/Projects/self/articles/*.md frontend/src/content/blog/"
echo "  4. git add . && git commit && git push"
echo "  5. 在 FireworksLife 仓库触发 'Deploy to Netlify' workflow"
