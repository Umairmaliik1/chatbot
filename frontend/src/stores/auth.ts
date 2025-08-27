import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '@/services/api'
import type { User, LoginCredentials, SignupData } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value)

  const login = async (credentials: LoginCredentials) => {
    isLoading.value = true
    error.value = null
    
    try {
      // Use URLSearchParams to match the original backend expectations
      const formData = new URLSearchParams()
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)
      if (credentials.remember_me) {
        formData.append('remember_me', 'true')
      }
      
      const response = await apiService.authPost('/api/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
      
      // Set user data from successful login response
      if (response.user) {
        user.value = response.user
      }
      
      return response
    } catch (err: any) {
      error.value = err.message || 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const signup = async (data: SignupData) => {
    isLoading.value = true
    error.value = null
    
    try {
      // Use URLSearchParams to match the original backend expectations
      const formData = new URLSearchParams()
      formData.append('username', data.username)
      formData.append('password', data.password)
      formData.append('confirm_password', data.confirm_password)
      
      const response = await apiService.authPost('/api/signup', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })
      
      return response
    } catch (err: any) {
      error.value = err.message || 'Signup failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    isLoading.value = true
    
    try {
      await apiService.authGet('/logout')
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      user.value = null
      isLoading.value = false
    }
  }

  const initializeAuth = async () => {
    try {
      const response = await apiService.authGet<{ user: User }>('/auth/me')
      user.value = response.user
    } catch (err) {
      // User not authenticated
      user.value = null
    }
  }

  const updateProfile = async (data: Partial<User>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await apiService.dashboardPost<{ user: User }>('/dashboard/update-profile', data)
      user.value = response.user
      return response
    } catch (err: any) {
      error.value = err.message || 'Profile update failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const changePassword = async (data: { current_password: string; new_password: string }) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await apiService.dashboardPost<{ message: string }>('/dashboard/update-password', data)
      return response
    } catch (err: any) {
      error.value = err.message || 'Password change failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    login,
    signup,
    logout,
    initializeAuth,
    updateProfile,
    changePassword
  }
})
