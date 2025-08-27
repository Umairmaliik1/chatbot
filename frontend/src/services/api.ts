import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import { useAuthStore } from '@/stores/auth'

class ApiService {
  private api: AxiosInstance
  private authApi: AxiosInstance
  private dashboardApi: AxiosInstance
  private kommoApi: AxiosInstance

  constructor() {
    // Main API client for /api/* endpoints
    this.api = axios.create({
      baseURL: '/api',
      timeout: 30000,
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      }
    })

    // Auth API client for auth endpoints (no prefix)
    this.authApi = axios.create({
      baseURL: '',
      timeout: 30000,
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      }
    })

    // Dashboard API client for dashboard endpoints (no prefix)
    this.dashboardApi = axios.create({
      baseURL: '',
      timeout: 30000,
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      }
    })

    // Kommo API client for kommo endpoints (/api/kommo prefix)
    this.kommoApi = axios.create({
      baseURL: '/api/kommo',
      timeout: 30000,
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      }
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Setup interceptors for all API clients
    [this.api, this.authApi, this.dashboardApi, this.kommoApi].forEach(client => {
      // Request interceptor
      client.interceptors.request.use(
        (config) => {
          // Add any request modifications here
          return config
        },
        (error) => {
          return Promise.reject(error)
        }
      )

      // Response interceptor
      client.interceptors.response.use(
        (response: AxiosResponse) => {
          return response.data
        },
        (error) => {
          if (error.response?.status === 401) {
            // Handle unauthorized access - only redirect if not already on login page
            if (window.location.pathname !== '/login') {
              const authStore = useAuthStore()
              authStore.user = null // Clear user state directly
              window.location.href = '/login'
            }
          }
          
          // Format error message
          const message = error.response?.data?.detail || error.message || 'An error occurred'
          return Promise.reject(new Error(message))
        }
      )
    })
  }

  // Generic HTTP methods for main API (/api/*)
  async get<T>(endpoint: string, params?: any): Promise<T> {
    const response = await this.api.get(endpoint, { params })
    return response
  }

  // Direct GET method that doesn't wrap params
  async getDirect<T>(endpoint: string, params?: any): Promise<T> {
    const response = await this.api.get(endpoint, { params })
    return response.data
  }

  async post<T>(endpoint: string, data?: any, config?: any): Promise<T> {
    const response = await this.api.post(endpoint, data, config)
    return response
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    const response = await this.api.put(endpoint, data)
    return response
  }

  async delete<T>(endpoint: string): Promise<T> {
    const response = await this.api.delete(endpoint)
    return response
  }

  // Auth API methods (no prefix)
  async authGet<T>(endpoint: string, params?: any): Promise<T> {
    const response = await this.authApi.get(endpoint, { params })
    return response
  }

  async authPost<T>(endpoint: string, data?: any, config?: any): Promise<T> {
    const response = await this.authApi.post(endpoint, data, config)
    return response
  }

  async authPut<T>(endpoint: string, data?: any): Promise<T> {
    const response = await this.authApi.put(endpoint, data)
    return response
  }

  async authDelete<T>(endpoint: string): Promise<T> {
    const response = await this.authApi.delete(endpoint)
    return response
  }

  // Dashboard API methods (no prefix)
  async dashboardGet<T>(endpoint: string, params?: any): Promise<T> {
    const response = await this.dashboardApi.get(endpoint, { params })
    return response
  }

  async dashboardPost<T>(endpoint: string, data?: any, config?: any): Promise<T> {
    const response = await this.dashboardApi.post(endpoint, data, config)
    return response
  }

  async dashboardPut<T>(endpoint: string, data?: any): Promise<T> {
    const response = await this.dashboardApi.put(endpoint, data)
    return response
  }

  async dashboardDelete<T>(endpoint: string): Promise<T> {
    const response = await this.dashboardApi.delete(endpoint)
    return response
  }

  // Kommo API methods (/api/kommo prefix)
  async kommoGet<T>(endpoint: string, params?: any): Promise<T> {
    const response = await this.kommoApi.get(endpoint, { params })
    return response
  }

  async kommoPost<T>(endpoint: string, data?: any, config?: any): Promise<T> {
    const response = await this.kommoApi.post(endpoint, data, config)
    return response
  }

  async kommoPut<T>(endpoint: string, data?: any): Promise<T> {
    const response = await this.kommoApi.put(endpoint, data)
    return response
  }

  async kommoDelete<T>(endpoint: string): Promise<T> {
    const response = await this.kommoApi.delete(endpoint)
    return response
  }

  // File upload method
  async upload<T>(endpoint: string, formData: FormData, onProgress?: (progress: number) => void): Promise<T> {
    const response = await this.api.post(endpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      }
    })
    return response
  }

  // Stream response for chat
  async stream(endpoint: string, data: any, onChunk: (chunk: string) => void): Promise<void> {
    const response = await fetch(`/api${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(data)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('No response body')
    }

    const decoder = new TextDecoder()
    let buffer = ''

    try {
      while (true) {
        const { value, done } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonData = JSON.parse(line.substring(6))
              if (jsonData.content && jsonData.content !== '[DONE]') {
                onChunk(jsonData.content)
              }
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
      }
    } finally {
      reader.releaseLock()
    }
  }
}

export const apiService = new ApiService()