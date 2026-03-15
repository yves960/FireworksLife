import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// 分类 API
export const categoryApi = {
  getCategories: () => api.get('/api/categories'),
  getCategory: (id) => api.get(`/api/categories/${id}`),
  createCategory: (data) => api.post('/api/categories', data),
  updateCategory: (id, data) => api.put(`/api/categories/${id}`, data),
  deleteCategory: (id) => api.delete(`/api/categories/${id}`)
}

// 文章 API
export const postApi = {
  getPosts: (params) => api.get('/api/posts', { params }),
  getPost: (id) => api.get(`/api/posts/${id}`),
  createPost: (data) => api.post('/api/posts', data),
  updatePost: (id, data) => api.put(`/api/posts/${id}`, data),
  deletePost: (id) => api.delete(`/api/posts/${id}`)
}

// 评论 API
export const commentApi = {
  getComments: (postId) => api.get(`/api/comments/post/${postId}`),
  createComment: (data) => api.post('/api/comments', data),
  deleteComment: (id) => api.delete(`/api/comments/${id}`)
}

// 点赞 API
export const likeApi = {
  getLikeStatus: (postId) => api.get(`/api/likes/status/${postId}`),
  toggleLike: (postId) => api.post(`/api/likes/like/${postId}`)
}

// 统计 API
export const statsApi = {
  getDashboardStats: () => api.get('/api/stats/dashboard')
}
