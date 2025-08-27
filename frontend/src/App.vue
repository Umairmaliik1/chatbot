<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <RouterView />
    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ToastContainer from '@/components/ToastContainer.vue'

const authStore = useAuthStore()

onMounted(() => {
  // Initialize auth state
  authStore.initializeAuth()
})
</script>