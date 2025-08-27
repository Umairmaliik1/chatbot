<template>
  <BaseLayout>
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p class="mt-2 text-gray-600">Welcome back, {{ authStore.user?.username }}! Here's what's happening with your AI chatbot.</p>
        </div>
        <div class="flex items-center space-x-4">
          <select 
            v-model="selectedPeriod" 
            @change="fetchDashboardStats"
            class="form-select w-48"
          >
            <option value="7">Last 7 Days</option>
            <option value="30">Last 30 Days</option>
            <option value="90">Last 90 Days</option>
            <option value="365">Last 365 Days</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="mb-6 p-4 bg-error-50 border border-error-200 rounded-lg">
      <div class="flex">
        <svg class="w-5 h-5 text-error-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-error-700">{{ error }}</p>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 mb-8">
      <StatCard
        v-for="stat in stats"
        :key="stat.key"
        :title="stat.title"
        :value="stat.value"
        :period="stat.period"
        :loading="stat.loading"
        :icon="stat.icon"
        :trend="stat.trend"
      />
    </div>

    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Recent Chats -->
      <BaseCard title="Recent Chat Sessions" subtitle="Latest conversations with your AI assistant">
        <div v-if="recentChats.length === 0" class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No recent chats</h3>
          <p class="mt-1 text-sm text-gray-500">Start a conversation to see it here.</p>
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="chat in recentChats"
            :key="chat.id"
            class="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
            @click="$router.push('/chat-history')"
          >
            <div class="flex-shrink-0">
              <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">{{ chat.title }}</p>
              <p class="text-sm text-gray-500">{{ formatTimeAgo(chat.updated_at) }}</p>
            </div>
            <div class="flex-shrink-0">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                {{ chat.message_count }} messages
              </span>
            </div>
          </div>
        </div>
      </BaseCard>

      <!-- System Status -->
      <BaseCard title="System Status" subtitle="Current status of your AI chatbot">
        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="w-3 h-3 bg-success-400 rounded-full"></div>
              <span class="text-sm font-medium text-gray-900">AI Service</span>
            </div>
            <span class="text-sm text-success-600 font-medium">Online</span>
          </div>
          
          <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="w-3 h-3 bg-success-400 rounded-full"></div>
              <span class="text-sm font-medium text-gray-900">Database</span>
            </div>
            <span class="text-sm text-success-600 font-medium">Connected</span>
          </div>
          
          <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="w-3 h-3 rounded-full" :class="kommoStatus ? 'bg-success-400' : 'bg-warning-400'"></div>
              <span class="text-sm font-medium text-gray-900">Kommo Integration</span>
            </div>
            <span class="text-sm font-medium" :class="kommoStatus ? 'text-success-600' : 'text-warning-600'">
              {{ kommoStatus ? 'Active' : 'Not Configured' }}
            </span>
          </div>
        </div>
        
        <div class="mt-6 pt-6 border-t border-gray-200">
          <BaseButton 
            variant="primary" 
            size="sm" 
            full-width
            @click="$router.push('/test-chat')"
          >
            Test Chat Interface
          </BaseButton>
        </div>
      </BaseCard>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { apiService } from '@/services/api'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import StatCard from '@/components/StatCard.vue'
// Using simple SVG icons instead of Heroicons
const UserGroupIcon = 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z'
const ChatBubbleLeftRightIcon = 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'
const DocumentTextIcon = 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'
const ChartBarIcon = 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
const CogIcon = 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z'

const authStore = useAuthStore()

const selectedPeriod = ref('30')
const error = ref<string | null>(null)
const kommoStatus = ref(false)

const stats = ref([
  {
    key: 'total_users',
    title: 'Total Users',
    value: 0,
    period: 'All time',
    loading: true,
    icon: UserGroupIcon,
    trend: null
  },
  {
    key: 'active_users',
    title: 'Active Users',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: UserGroupIcon,
    trend: null
  },
  {
    key: 'sessions',
    title: 'Chat Sessions',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: ChatBubbleLeftRightIcon,
    trend: null
  },
  {
    key: 'messages',
    title: 'Messages Exchanged',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: DocumentTextIcon,
    trend: null
  },
  {
    key: 'knowledge_files',
    title: 'Knowledge Files',
    value: 0,
    period: 'Total indexed files',
    loading: true,
    icon: ChartBarIcon,
    trend: null
  }
])

const recentChats = ref([
  {
    id: 1,
    title: 'Customer Support Inquiry',
    updated_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    message_count: 5
  },
  {
    id: 2,
    title: 'Product Information Request',
    updated_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
    message_count: 8
  },
  {
    id: 3,
    title: 'Technical Support',
    updated_at: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString(),
    message_count: 12
  }
])

const fetchDashboardStats = async () => {
  error.value = null
  
  // Set all stats to loading
  stats.value.forEach(stat => {
    stat.loading = true
  })
  
  try {
    const response = await apiService.get(`/dashboard-stats?days=${selectedPeriod.value}`)
    
    // Update stats with response data
    stats.value.forEach(stat => {
      stat.loading = false
      stat.value = response[stat.key] || 0
      if (stat.key !== 'total_users' && stat.key !== 'knowledge_files') {
        stat.period = `In the last ${selectedPeriod.value} days`
      }
    })
  } catch (err: any) {
    error.value = err.message || 'Failed to load dashboard statistics'
    stats.value.forEach(stat => {
      stat.loading = false
    })
  }
}

const formatTimeAgo = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const seconds = Math.round((now.getTime() - date.getTime()) / 1000)
  const minutes = Math.round(seconds / 60)
  const hours = Math.round(minutes / 60)
  const days = Math.round(hours / 24)

  if (seconds < 60) return `${seconds} sec ago`
  if (minutes < 60) return `${minutes} min ago`
  if (hours < 24) return `${hours} hr ago`
  return `${days} days ago`
}

const checkKommoStatus = async () => {
  try {
    const response = await apiService.get('/kommo/integration/status')
    kommoStatus.value = response.active || false
  } catch (err) {
    kommoStatus.value = false
  }
}

onMounted(() => {
  fetchDashboardStats()
  checkKommoStatus()
})
</script>
