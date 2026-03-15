<template>
  <div class="admin" :class="{ 'dark-mode': isDarkMode }">
    <div class="admin-header">
      <h1>管理后台</h1>
      <div class="header-actions">
        <button @click="toggleDarkMode" class="dark-toggle">
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
        <button @click="handleLogout" class="logout-btn">退出</button>
      </div>
    </div>
    
    <div class="admin-content">
      <!-- 统计卡片 -->
      <div class="stats">
        <div class="stat-card">
          <h3>📝 文章总数</h3>
          <p class="stat-number">{{ stats.posts.total }}</p>
          <p class="stat-detail">已发布: {{ stats.posts.published }} | 草稿: {{ stats.posts.draft }}</p>
        </div>
        <div class="stat-card">
          <h3>💬 评论总数</h3>
          <p class="stat-number">{{ stats.comments.total }}</p>
        </div>
        <div class="stat-card">
          <h3>❤️ 点赞总数</h3>
          <p class="stat-number">{{ stats.likes.total }}</p>
        </div>
        <div class="stat-card">
          <h3>👥 用户总数</h3>
          <p class="stat-number">{{ stats.users.total }}</p>
        </div>
      </div>
      
      <!-- 分类管理 -->
      <div class="section">
        <div class="section-header">
          <h2>📁 分类管理</h2>
          <button @click="showCategoryForm = true" class="create-btn">+ 新建分类</button>
        </div>
        
        <div v-if="showCategoryForm" class="form-modal">
          <div class="form-content">
            <h3>{{ editingCategory ? '编辑分类' : '新建分类' }}</h3>
            <form @submit.prevent="handleSaveCategory">
              <input v-model="categoryForm.name" placeholder="分类名称" class="form-input" required />
              <input v-model="categoryForm.description" placeholder="分类描述（可选）" class="form-input" />
              <div class="form-actions">
                <button type="submit" class="submit-btn">保存</button>
                <button type="button" @click="resetCategoryForm" class="cancel-btn">取消</button>
              </div>
            </form>
          </div>
        </div>
        
        <div class="categories-grid">
          <div v-for="cat in categories" :key="cat.id" class="category-card">
            <div class="category-info">
              <h4>{{ cat.name }}</h4>
              <p>{{ cat.description || '暂无描述' }}</p>
              <span class="post-count">{{ cat.post_count }} 篇文章</span>
            </div>
            <div class="category-actions">
              <button @click="editCategory(cat)" class="edit-btn">编辑</button>
              <button @click="deleteCategory(cat.id)" class="delete-btn">删除</button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 文章管理 -->
      <div class="section">
        <div class="section-header">
          <h2>📄 文章管理</h2>
          <button @click="showPostForm = true" class="create-btn">+ 新建文章</button>
        </div>
        
        <div v-if="showPostForm" class="form-modal">
          <div class="form-content large">
            <h3>{{ editingPost ? '编辑文章' : '新建文章' }}</h3>
            <form @submit.prevent="handleSavePost">
              <input v-model="postForm.title" placeholder="文章标题" class="form-input" required />
              
              <div class="form-row">
                <select v-model="postForm.category_id" class="form-select">
                  <option :value="null">选择分类（可选）</option>
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                    {{ cat.name }}
                  </option>
                </select>
                <select v-model="postForm.status" class="form-select">
                  <option value="draft">草稿</option>
                  <option value="published">发布</option>
                </select>
              </div>
              
              <textarea v-model="postForm.content" placeholder="文章内容（支持 Markdown）" class="form-textarea" rows="10" required></textarea>
              
              <div class="form-actions">
                <button type="submit" class="submit-btn">保存</button>
                <button type="button" @click="resetPostForm" class="cancel-btn">取消</button>
              </div>
            </form>
          </div>
        </div>
        
        <div class="posts-list">
          <div v-for="post in posts" :key="post.id" class="post-item">
            <div class="post-info">
              <h4>{{ post.title }}</h4>
              <p class="post-meta">
                <span>{{ formatDate(post.created_at) }}</span>
                <span v-if="post.category" class="category-tag">{{ post.category.name }}</span>
                <span :class="['status-tag', post.status]">{{ getStatusText(post.status) }}</span>
              </p>
            </div>
            <div class="post-actions">
              <button @click="editPost(post)" class="edit-btn">编辑</button>
              <button @click="deletePost(post.id)" class="delete-btn">删除</button>
            </div>
          </div>
          
          <div v-if="posts.length === 0" class="no-data">
            暂无文章
          </div>
        </div>
      </div>
      
      <!-- 最近文章 -->
      <div class="section" v-if="stats.recent_posts && stats.recent_posts.length > 0">
        <h2>🕐 最近文章</h2>
        <div class="recent-posts">
          <div v-for="post in stats.recent_posts" :key="post.id" class="recent-post-item">
            <span class="recent-title">{{ post.title }}</span>
            <span class="recent-date">{{ formatDate(post.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()

const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')
const stats = ref({
  posts: { total: 0, published: 0, draft: 0 },
  comments: { total: 0 },
  likes: { total: 0 },
  users: { total: 0 },
  recent_posts: []
})

const categories = ref([])
const posts = ref([])

const showCategoryForm = ref(false)
const showPostForm = ref(false)
const editingCategory = ref(null)
const editingPost = ref(null)

const categoryForm = reactive({ name: '', description: '' })
const postForm = reactive({ title: '', content: '', category_id: null, status: 'draft' })

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('darkMode', isDarkMode.value)
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const getStatusText = (status) => {
  const map = { 'draft': '草稿', 'published': '已发布', 'archived': '已归档' }
  return map[status] || status
}

// 加载统计数据
const loadStats = async () => {
  try {
    const response = await api.get('/api/stats/dashboard')
    stats.value = response.data
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

// 加载分类
const loadCategories = async () => {
  try {
    const response = await api.get('/api/categories')
    categories.value = response.data.categories
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

// 加载文章
const loadPosts = async () => {
  try {
    const response = await api.get('/api/posts', { params: { per_page: 50 } })
    posts.value = response.data.posts
  } catch (error) {
    console.error('加载文章失败:', error)
  }
}

// 分类操作
const editCategory = (cat) => {
  editingCategory.value = cat
  categoryForm.name = cat.name
  categoryForm.description = cat.description || ''
  showCategoryForm.value = true
}

const handleSaveCategory = async () => {
  try {
    if (editingCategory.value) {
      await api.put(`/api/categories/${editingCategory.value.id}`, categoryForm)
    } else {
      await api.post('/api/categories', categoryForm)
    }
    resetCategoryForm()
    loadCategories()
  } catch (error) {
    alert(error.response?.data?.detail || '保存失败')
  }
}

const deleteCategory = async (id) => {
  if (confirm('确定要删除这个分类吗？相关文章的分类将被清空。')) {
    try {
      await api.delete(`/api/categories/${id}`)
      loadCategories()
      loadPosts()
    } catch (error) {
      alert(error.response?.data?.detail || '删除失败')
    }
  }
}

const resetCategoryForm = () => {
  showCategoryForm.value = false
  editingCategory.value = null
  categoryForm.name = ''
  categoryForm.description = ''
}

// 文章操作
const editPost = (post) => {
  editingPost.value = post
  postForm.title = post.title
  postForm.content = posts.value.find(p => p.id === post.id)?.content || ''
  postForm.category_id = post.category?.id || null
  postForm.status = post.status
  showPostForm.value = true
}

const handleSavePost = async () => {
  try {
    if (editingPost.value) {
      await api.put(`/api/posts/${editingPost.value.id}`, postForm)
    } else {
      await api.post('/api/posts', postForm)
    }
    resetPostForm()
    loadPosts()
    loadStats()
    loadCategories()
  } catch (error) {
    alert(error.response?.data?.detail || '保存失败')
  }
}

const deletePost = async (id) => {
  if (confirm('确定要删除这篇文章吗？')) {
    try {
      await api.delete(`/api/posts/${id}`)
      loadPosts()
      loadStats()
      loadCategories()
    } catch (error) {
      alert(error.response?.data?.detail || '删除失败')
    }
  }
}

const resetPostForm = () => {
  showPostForm.value = false
  editingPost.value = null
  postForm.title = ''
  postForm.content = ''
  postForm.category_id = null
  postForm.status = 'draft'
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadStats()
  loadCategories()
  loadPosts()
})
</script>

<style scoped>
.admin {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem;
  transition: background 0.3s ease;
}

.admin.dark-mode {
  background: #1a1a2e;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dark-mode .admin-header {
  background: #2d2d44;
}

.admin-header h1 {
  margin: 0;
  color: #333;
}

.dark-mode .admin-header h1 {
  color: #e0e0e0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.dark-toggle {
  font-size: 1.2rem;
  padding: 0.5rem;
  border: none;
  background: none;
  cursor: pointer;
}

.logout-btn {
  padding: 0.5rem 1.5rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.admin-content {
  max-width: 1200px;
  margin: 0 auto;
}

/* 统计卡片 */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.dark-mode .stat-card {
  background: #2d2d44;
}

.stat-card h3 {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
}

.dark-mode .stat-card h3 {
  color: #aaa;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #667eea;
  margin: 0;
}

.stat-detail {
  font-size: 0.8rem;
  color: #999;
  margin: 0.5rem 0 0 0;
}

/* 区块 */
.section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.dark-mode .section {
  background: #2d2d44;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  margin: 0;
  color: #333;
}

.dark-mode .section-header h2 {
  color: #e0e0e0;
}

.create-btn {
  padding: 0.5rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

/* 表单弹窗 */
.form-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.form-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
}

.form-content.large {
  max-width: 600px;
}

.dark-mode .form-content {
  background: #2d2d44;
}

.form-content h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.dark-mode .form-content h3 {
  color: #e0e0e0;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

.dark-mode .form-input,
.dark-mode .form-select,
.dark-mode .form-textarea {
  background: #3d3d5c;
  border-color: #555;
  color: #e0e0e0;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-row .form-select {
  flex: 1;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.submit-btn,
.cancel-btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.submit-btn {
  background: #667eea;
  color: white;
}

.cancel-btn {
  background: #ddd;
  color: #333;
}

.dark-mode .cancel-btn {
  background: #555;
  color: #e0e0e0;
}

/* 分类网格 */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.category-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 6px;
}

.dark-mode .category-card {
  border-color: #444;
}

.category-info h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.dark-mode .category-info h4 {
  color: #e0e0e0;
}

.category-info p {
  margin: 0;
  font-size: 0.85rem;
  color: #666;
}

.dark-mode .category-info p {
  color: #aaa;
}

.post-count {
  font-size: 0.75rem;
  color: #999;
}

.category-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn,
.delete-btn {
  padding: 0.25rem 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.edit-btn {
  background: #e8f4fd;
  color: #3498db;
}

.delete-btn {
  background: #fdeaea;
  color: #e74c3c;
}

/* 文章列表 */
.posts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.post-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 6px;
}

.dark-mode .post-item {
  border-color: #444;
}

.post-info h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.dark-mode .post-info h4 {
  color: #e0e0e0;
}

.post-meta {
  display: flex;
  gap: 0.75rem;
  font-size: 0.85rem;
  color: #666;
}

.dark-mode .post-meta {
  color: #aaa;
}

.category-tag {
  background: #e8f4fd;
  color: #3498db;
  padding: 0.125rem 0.5rem;
  border-radius: 3px;
}

.status-tag {
  padding: 0.125rem 0.5rem;
  border-radius: 3px;
}

.status-tag.published {
  background: #e8f5e9;
  color: #4caf50;
}

.status-tag.draft {
  background: #fff3e0;
  color: #ff9800;
}

.post-actions {
  display: flex;
  gap: 0.5rem;
}

/* 最近文章 */
.recent-posts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.recent-post-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: #f9f9f9;
  border-radius: 4px;
}

.dark-mode .recent-post-item {
  background: #3d3d5c;
}

.recent-title {
  color: #333;
}

.dark-mode .recent-title {
  color: #e0e0e0;
}

.recent-date {
  color: #999;
  font-size: 0.85rem;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #999;
}
</style>