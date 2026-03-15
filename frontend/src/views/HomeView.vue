<template>
  <div class="home" :class="{ 'dark-mode': isDarkMode }">
    <header class="header">
      <h1 class="title">轻量级博客系统</h1>
      <nav class="nav">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link v-if="!authStore.isAuthenticated" to="/login" class="nav-link">登录</router-link>
        <router-link v-if="!authStore.isAuthenticated" to="/register" class="nav-link">注册</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/admin" class="nav-link">管理后台</router-link>
        <button v-if="authStore.isAuthenticated" @click="handleLogout" class="nav-link">退出</button>
        <button @click="toggleDarkMode" class="nav-link dark-toggle">
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
      </nav>
    </header>

    <main class="main">
      <!-- 分类筛选 -->
      <div class="category-filter">
        <button
          @click="selectCategory(null)"
          :class="['category-btn', { active: selectedCategory === null }]"
        >
          全部
        </button>
        <button
          v-for="cat in categories"
          :key="cat.id"
          @click="selectCategory(cat.id)"
          :class="['category-btn', { active: selectedCategory === cat.id }]"
        >
          {{ cat.name }}
          <span class="post-count">({{ cat.post_count }})</span>
        </button>
      </div>

      <div v-if="loading" class="loading">
        <div class="skeleton-list">
          <div v-for="i in 3" :key="i" class="skeleton-card">
            <div class="skeleton-title"></div>
            <div class="skeleton-meta"></div>
            <div class="skeleton-content"></div>
          </div>
        </div>
      </div>
      <div v-else>
        <div v-if="posts.length === 0" class="no-posts">
          暂无文章
        </div>
        <div v-for="post in posts" :key="post.id" class="post-card">
          <router-link :to="`/post/${post.id}`" class="post-link">
            <h2 class="post-title">{{ post.title }}</h2>
          </router-link>
          <p class="post-meta">
            <span class="post-author">{{ post.author }}</span>
            <span class="post-date">{{ formatDate(post.created_at) }}</span>
            <span v-if="post.category" class="post-category">
              📁 {{ post.category.name }}
            </span>
          </p>
          <p class="post-summary">{{ getSummary(post.content) }}</p>
        </div>

        <div v-if="totalPages > 1" class="pagination">
          <button
            v-for="page in totalPages"
            :key="page"
            @click="loadPage(page)"
            :class="{ active: currentPage === page }"
            class="page-btn"
          >
            {{ page }}
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import { categoryApi, postApi } from '../api'

const authStore = useAuthStore()

const posts = ref([])
const categories = ref([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(1)
const selectedCategory = ref(null)
const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const getSummary = (content) => {
  if (!content) return ''
  return content.length > 200 ? content.substring(0, 200) + '...' : content
}

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('darkMode', isDarkMode.value)
}

const loadCategories = async () => {
  try {
    const response = await categoryApi.getCategories()
    categories.value = response.data.categories
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const loadPosts = async (page = 1) => {
  loading.value = true
  try {
    const params = { page, per_page: 10 }
    if (selectedCategory.value) {
      params.category_id = selectedCategory.value
    }
    const response = await postApi.getPosts(params)
    posts.value = response.data.posts
    totalPages.value = response.data.total_pages
    currentPage.value = page
  } catch (error) {
    console.error('加载文章失败:', error)
  } finally {
    loading.value = false
  }
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  loadPosts(1)
}

const loadPage = (page) => {
  loadPosts(page)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleLogout = () => {
  authStore.logout()
}

onMounted(() => {
  authStore.fetchCurrentUser()
  loadCategories()
  loadPosts()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transition: background 0.3s ease;
}

.home.dark-mode {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.header {
  padding: 2rem;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.dark-mode .header {
  background: rgba(30, 30, 46, 0.95);
}

.dark-mode .title {
  color: #e0e0e0;
}

.title {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.nav {
  display: flex;
  gap: 1rem;
}

.nav-link {
  text-decoration: none;
  color: #333;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  background: none;
  font-size: 1rem;
}

.dark-mode .nav-link {
  color: #e0e0e0;
}

.nav-link:hover {
  background: #667eea;
  color: white;
}

.dark-toggle {
  font-size: 1.2rem;
}

.main {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.category-btn {
  padding: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.category-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.category-btn.active {
  background: white;
  color: #667eea;
  border-color: white;
}

.post-count {
  font-size: 0.8rem;
  opacity: 0.7;
}

.loading {
  text-align: center;
  padding: 2rem;
}

.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.skeleton-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 1.5rem;
  border-radius: 8px;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}

@keyframes skeleton-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton-title {
  height: 1.5rem;
  width: 60%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.skeleton-meta {
  height: 0.9rem;
  width: 40%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.skeleton-content {
  height: 3rem;
  width: 100%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes skeleton-shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.no-posts {
  text-align: center;
  padding: 3rem;
  color: white;
  font-size: 1.2rem;
}

.post-card {
  background: white;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.dark-mode .post-card {
  background: #2d2d44;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.post-link {
  text-decoration: none;
  color: inherit;
}

.post-title {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.dark-mode .post-title {
  color: #e0e0e0;
}

.post-meta {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.dark-mode .post-meta {
  color: #aaa;
}

.post-author {
  margin-right: 0.5rem;
}

.post-category {
  color: #667eea;
}

.dark-mode .post-category {
  color: #9f9fef;
}

.post-summary {
  color: #555;
  line-height: 1.6;
}

.dark-mode .post-summary {
  color: #bbb;
}

.pagination {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  margin-top: 2rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.dark-mode .page-btn {
  background: #2d2d44;
  border-color: #444;
  color: #e0e0e0;
}

.page-btn:hover {
  background: #667eea;
  color: white;
}

.page-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}
</style>