<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="flex justify-center">
        <div class="w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
          </svg>
        </div>
      </div>
      <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">
        Reset your password
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Enter your email address and we'll send you a link to reset your password.
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <BaseCard class="py-8 px-4 shadow-strong sm:px-10">
        <form class="space-y-6" @submit.prevent="handleSubmit">
          <BaseInput
            v-model="form.email"
            type="email"
            label="Email address"
            placeholder="Enter your email"
            :error="errors.email"
            required
            autocomplete="email"
          />

          <div>
            <BaseButton
              type="submit"
              variant="primary"
              size="lg"
              :loading="isLoading"
              :disabled="!form.email.trim()"
              full-width
            >
              Send Reset Link
            </BaseButton>
          </div>
        </form>

        <div class="mt-6 text-center">
          <router-link to="/login" class="text-sm text-primary-600 hover:text-primary-500">
            Back to sign in
          </router-link>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '@/composables/useToast'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import { apiService } from '@/services/api'

const router = useRouter()
const { error: showError, success: showSuccess } = useToast()

const form = ref({
  email: ''
})

const errors = ref({
  email: ''
})

const isLoading = ref(false)

const validateForm = () => {
  errors.value = { email: '' }
  
  if (!form.value.email) {
    errors.value.email = 'Email is required'
  } else if (!/\S+@\S+\.\S+/.test(form.value.email)) {
    errors.value.email = 'Email is invalid'
  }
}

const handleSubmit = async () => {
  validateForm()
  
  if (errors.value.email) return
  
  isLoading.value = true
  
  try {
    await apiService.post('/auth/forgot-password', {
      email: form.value.email
    })
    
    showSuccess('Reset link sent!', 'Check your email for instructions to reset your password.')
    router.push('/login')
  } catch (err: any) {
    showError('Failed to send reset link', err.message)
  } finally {
    isLoading.value = false
  }
}
</script>
