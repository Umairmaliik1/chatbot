<template>
  <div class="login-container">
    <div class="login-box">
      <div class="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center mx-auto mb-6">
        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
      </div>
      <h2>Create Your Account</h2>
      
      <div v-if="error" class="error-message">{{ error }}</div>
      
      <form @submit.prevent="handleSignup">
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
            autocomplete="new-password"
          >
        </div>
        
        <div class="input-group">
          <label for="confirm_password">Confirm Password</label>
          <input 
            v-model="form.confirmPassword"
            type="password" 
            id="confirm_password" 
            name="confirm_password" 
            required
            autocomplete="new-password"
          >
        </div>
        
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'Creating Account...' : 'Sign Up' }}
        </button>
      </form>
      
      <div class="extra-links">
        <router-link to="/login">Already have an account? Sign In</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const authStore = useAuthStore()
const { error: showError, success: showSuccess } = useToast()

const form = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const error = ref('')
const isLoading = ref(false)

const handleSignup = async () => {
  // Clear previous errors
  error.value = ''

  // Validate form
  if (!form.value.username || !form.value.password || !form.value.confirmPassword) {
    error.value = 'Please fill in all fields'
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    error.value = 'Passwords do not match'
    return
  }

  if (form.value.password.length < 8) {
    error.value = 'Password must be at least 8 characters long'
    return
  }

  isLoading.value = true

  try {
    await authStore.signup({
      username: form.value.username,
      password: form.value.password,
      confirm_password: form.value.confirmPassword
    })
    
    showSuccess('Signup successful!', 'Please log in with your new account.')
    router.push('/login?message=Signup successful! Please log in.')
  } catch (err: any) {
    if (err.message.includes('already exists')) {
      error.value = 'Username already exists'
    } else {
      error.value = err.message || 'Signup failed. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  // Redirect if already authenticated
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})
</script>