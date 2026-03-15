<template>
  <div class="post-detail" :class="{ 'dark-mode': isDarkMode }">
    <div v-if="loading" class="loading">
      <div class="skeleton-post">
        <div class="skeleton-title"></div>
        <div class="skeleton-meta"></div>
        <div class="skeleton-content"></div>
      </div>
    </div>
    <div v-else-if="post" class="post-container">
      <router-link to="/" class="back-link">← 返回首页</router-link>
      
      <h1 class="post-title">{{ post.title }}</h1>
      
      <div class="post-meta">
        <span class="post-author">作者：{{ post.author || 'Unknown' }}</span>
        <span class="post-date">{{ formatDate(post.created_at) }}</span>
        <span v-if="post.category" class="post-category">📁 {{ post.category.name }}</span>
        <span class="post-status">状态：{{ getStatusText(post.status) }}</span>
      </div>
      
      <!-- Markdown 渲染的内容 -->
      <div class="post-content markdown-body" v-html="post.rendered_content || post.content"></div>
      
      <div class="post-actions">
        <button 
          @click="handleLike" 
          :class="['like-btn', 'action-btn', { liked: likeStatus.liked, 'animate': likeAnimating }]" 
        >
          <span class="heart">{{ likeStatus.liked ? '❤️' : '🤍' }}</span>
          <span class="count">{{ formatLikeCount(likeStatus.likes_count) }}</span>
        </button>
      </div>
      
      <div class="comments-section">
        <h2>评论</h2>
        
        <form v-if="authStore.isAuthenticated" @submit.prevent="handleComment" class="comment-form">
          <textarea
            v-model="newComment"
            placeholder="发表评论..."
            class="comment-input"
            rows="3"
          ></textarea>
          <button type="submit" :disabled="!newComment.trim()" class="submit-btn">
            发表评论
          </button>
        </form>
        <div v-else class="login-prompt">
          <router-link to="/login">登录</router-link>后发表评论
        </div>
        
        <div v-if="comments.length === 0" class="no-comments">
          暂无评论
        </div>
        <div v-else class="comments-list">
          <CommentItem
            v-for="comment in comments"
            :key="comment.id"
            :comment="comment"
            @delete="handleDeleteComment"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../store/auth'
import api from '../api'
import CommentItem from '../components/CommentItem.vue'

const route = useRoute()
const authStore = useAuthStore()

const post = ref(null)
const comments = ref([])
const likeStatus = ref({ liked: false, likes_count: 0 })
const newComment = ref('')
const loading = ref(true)
const likeAnimating = ref(false)
const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusText = (status) => {
  const statusMap = {
    'draft': '草稿',
    'published': '已发布',
    'archived': '已归档'
  }
  return statusMap[status] || status
}

const formatLikeCount = (count) => {
  if (!count) return '0'
  if (count >= 10000) return (count / 10000).toFixed(1) + 'w'
  if (count >= 1000) return (count / 1000).toFixed(1) + 'k'
  return count.toString()
}

const loadPost = async () => {
  try {
    const response = await api.get(`/api/posts/${route.params.id}`)
    post.value = response.data
  } catch (error) {
    console.error('加载文章失败:', error)
  } finally {
    loading.value = false
  }
}

const loadComments = async () => {
  try {
    const response = await api.get(`/api/comments/post/${route.params.id}`)
    comments.value = response.data
  } catch (error) {
    console.error('加载评论失败:', error)
  }
}

const loadLikeStatus = async () => {
  if (!authStore.isAuthenticated) return
  
  try {
    const response = await api.get(`/api/likes/status/${route.params.id}`)
    likeStatus.value = response.data
  } catch (error) {
    console.error('加载点赞状态失败:', error)
  }
}

const handleLike = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    return
  }
  
  try {
    likeAnimating.value = true
    const response = await api.post(`/api/likes/like/${route.params.id}`)
    likeStatus.value = response.data
    setTimeout(() => {
      likeAnimating.value = false
    }, 300)
  } catch (error) {
    console.error('点赞失败:', error)
  }
}

const handleComment = async () => {
  if (!newComment.value.trim()) return
  
  try {
    await api.post('/api/comments', {
      content: newComment.value,
      post_id: parseInt(route.params.id)
    })
    newComment.value = ''
    loadComments()
  } catch (error) {
    console.error('发表评论失败:', error)
  }
}

const handleDeleteComment = async (commentId) => {
  try {
    await api.delete(`/api/comments/${commentId}`)
    loadComments()
  } catch (error) {
    console.error('删除评论失败:', error)
  }
}

onMounted(() => {
  loadPost()
  loadComments()
  loadLikeStatus()
})
</script>

<style scoped>
.post-detail {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  transition: background 0.3s ease;
}

.post-detail.dark-mode {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.loading {
  text-align: center;
  padding: 2rem;
}

.skeleton-post {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 8px;
}

.skeleton-title {
  height: 2rem;
  width: 60%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.skeleton-meta {
  height: 1rem;
  width: 40%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 2rem;
}

.skeleton-content {
  height: 10rem;
  width: 100%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.post-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dark-mode .post-container {
  background: #2d2d44;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #667eea;
  text-decoration: none;
}

.dark-mode .back-link {
  color: #9f9fef;
}

.back-link:hover {
  text-decoration: underline;
}

.post-title {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #333;
}

.dark-mode .post-title {
  color: #e0e0e0;
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  color: #666;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.dark-mode .post-meta {
  color: #aaa;
}

.post-category {
  color: #667eea;
}

/* Markdown 样式 */
.post-content {
  line-height: 1.8;
  color: #333;
  margin-bottom: 2rem;
}

.dark-mode .post-content {
  color: #d0d0d0;
}

.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4) {
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  color: #333;
}

.dark-mode .post-content :deep(h1),
.dark-mode .post-content :deep(h2),
.dark-mode .post-content :deep(h3),
.dark-mode .post-content :deep(h4) {
  color: #e0e0e0;
}

.post-content :deep(h1) { font-size: 1.8rem; }
.post-content :deep(h2) { font-size: 1.5rem; }
.post-content :deep(h3) { font-size: 1.25rem; }

.post-content :deep(p) {
  margin-bottom: 1rem;
}

.post-content :deep(code) {
  background: #f4f4f4;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9em;
}

.dark-mode .post-content :deep(code) {
  background: #3d3d5c;
}

.post-content :deep(pre) {
  background: #f8f8f8;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.dark-mode .post-content :deep(pre) {
  background: #1e1e2e;
}

.post-content :deep(pre code) {
  background: none;
  padding: 0;
}

.post-content :deep(blockquote) {
  border-left: 4px solid #667eea;
  margin: 1rem 0;
  padding-left: 1rem;
  color: #666;
}

.dark-mode .post-content :deep(blockquote) {
  color: #aaa;
  border-left-color: #9f9fef;
}

.post-content :deep(ul),
.post-content :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.post-content :deep(li) {
  margin-bottom: 0.5rem;
}

.post-content :deep(a) {
  color: #667eea;
  text-decoration: none;
}

.post-content :deep(a:hover) {
  text-decoration: underline;
}

.post-content :deep(img) {
  max-width: 100%;
  border-radius: 6px;
  margin: 1rem 0;
}

.post-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.post-content :deep(th),
.post-content :deep(td) {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
}

.dark-mode .post-content :deep(th),
.dark-mode .post-content :deep(td) {
  border-color: #444;
}

.post-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.dark-mode .post-actions {
  border-bottom-color: #444;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 20px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dark-mode .action-btn {
  background: #3d3d5c;
  border-color: #555;
  color: #e0e0e0;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.like-btn.liked {
  background: #fff0f0;
  border-color: #ffcccc;
}

.dark-mode .like-btn.liked {
  background: #4a3030;
  border-color: #663333;
}

.like-btn.animate {
  animation: like-pop 0.3s ease;
}

@keyframes like-pop {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.heart {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.like-btn:hover .heart {
  transform: scale(1.2);
}

.count {
  font-weight: 500;
}

.comments-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.dark-mode .comments-section h2 {
  color: #e0e0e0;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.comment-input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  resize: vertical;
}

.dark-mode .comment-input {
  background: #3d3d5c;
  border-color: #555;
  color: #e0e0e0;
}

.comment-input:focus {
  outline: none;
  border-color: #667eea;
}

.submit-btn {
  padding: 0.5rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.3s ease;
  align-self: flex-start;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-prompt {
  margin-bottom: 2rem;
  color: #666;
}

.dark-mode .login-prompt {
  color: #aaa;
}

.login-prompt a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.no-comments {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>