<template>
  <div class="login-container">
    <div class="login-box">
      <div class="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center mx-auto mb-6">
        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </div>
      <h2>Sign In to Your Account</h2>
      
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="message" class="success-message">{{ message }}</div>
      
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="username">Username</label>
          <input 
            v-model="form.username"
            type="text" 
            id="username" 
            name="username" 
            required
            autocomplete="username"
          >
        </div>
        
        <div class="input-group">
          <label for="password">Password</label>
          <input 
            v-model="form.password"
            type="password" 
            id="password" 
            name="password" 
            required
            autocomplete="current-password"
          >
        </div>
        
        <div class="input-group" style="flex-direction: row; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
          <input 
            v-model="form.rememberMe"
            type="checkbox" 
            id="remember_me" 
            name="remember_me" 
            value="true" 
            style="width: auto; height: auto;"
          >
          <label for="remember_me" style="margin-bottom: 0; font-weight: normal; cursor: pointer;">Remember Me</label>
        </div>
        
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'Signing In...' : 'Sign In' }}
        </button>
      </form>
      
      <div class="extra-links">
        <router-link to="/forgot-password">Forgot Password?</router-link><br>
        <router-link to="/signup">Don't have an account? Sign Up</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { error: showError, success: showSuccess } = useToast()

const form = ref({
  username: '',
  password: '',
  rememberMe: false
})

const error = ref('')
const message = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    error.value = 'Please fill in all fields'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    await authStore.login({
      username: form.value.username,
      password: form.value.password,
      remember_me: form.value.rememberMe
    })
    
    showSuccess('Login successful!', 'Welcome back!')
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.message || 'Invalid username or password'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  // Check for success message from signup
  if (route.query.message) {
    message.value = route.query.message as string
  }
  
  // Redirect if already authenticated
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})
</script>