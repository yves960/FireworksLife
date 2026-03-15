import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: false
  }),

  actions: {
    async login(credentials) {
      try {
        const response = await axios.post('/api/auth/login', credentials)
        this.token = response.data.access_token
        this.user = response.data.user
        this.isAuthenticated = true
        localStorage.setItem('token', this.token)
        return response.data
      } catch (error) {
        throw error.response?.data?.detail || '登录失败'
      }
    },

    async register(userData) {
      try {
        const response = await axios.post('/api/users/register', userData)
        return response.data
      } catch (error) {
        throw error.response?.data?.detail || '注册失败'
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
    },

    async fetchCurrentUser() {
      if (!this.token) return
      
      try {
        const response = await axios.get('/api/auth/me', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        this.user = response.data
        this.isAuthenticated = true
      } catch (error) {
        this.logout()
      }
    }
  }
})
