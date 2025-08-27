import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '@/services/api'
import type { User, LoginCredentials, SignupData, UserProfileUpdate } from '@/types/auth'

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

  const updateProfile = async (data: UserProfileUpdate) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await apiService.post('/settings', data)
      if (user.value) {
        user.value.profile = { ...(user.value.profile || {}), ...response }
      }
      return response
    } catch (err: any) {
      error.value = err.message || 'Profile update failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const changePassword = async (data: Pick<UserProfileUpdate, 'new_password' | 'confirm_password'>) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.post<{ message: string }>('/settings', data)
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
