<template>
  <BaseLayout>
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white dark:text-white">{{ dashboardTitle }}</h1>
          <p class="mt-2 text-gray-600 dark:text-gray-400 dark:text-gray-400">Welcome back, {{ authStore.user?.username }}! Here's what's happening with {{ websiteName }}.</p>
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
      />
    </div>

    <!-- System Status -->
    <div class="max-w-md">
      <!-- System Status -->
      <BaseCard title="System Status" subtitle="Current status of your AI chatbot">
        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="w-3 h-3 bg-success-400 rounded-full"></div>
              <span class="text-sm font-medium text-gray-900 dark:text-white">AI Service</span>
            </div>
            <span class="text-sm text-success-600 font-medium">Online</span>
          </div>
          
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="w-3 h-3 bg-success-400 rounded-full"></div>
              <span class="text-sm font-medium text-gray-900 dark:text-white">Database</span>
            </div>
            <span class="text-sm text-success-600 font-medium">Connected</span>
          </div>
          
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div class="flex items-center space-x-3">
              <div class="w-3 h-3 rounded-full" :class="kommoStatus ? 'bg-success-400' : 'bg-warning-400'"></div>
              <span class="text-sm font-medium text-gray-900 dark:text-white">Kommo Integration</span>
            </div>
            <span class="text-sm font-medium" :class="kommoStatus ? 'text-success-600' : 'text-warning-600'">
              {{ kommoStatus ? 'Active' : 'Not Configured' }}
            </span>
          </div>
        </div>
        
        <div class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
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


const authStore = useAuthStore()

const selectedPeriod = ref('30')
const error = ref<string | null>(null)
const kommoStatus = ref(false)

interface DashboardStat {
  key: string
  title: string
  value: number
  period: string
  loading: boolean
  icon: string
  trend: number | null
}

const stats = ref<DashboardStat[]>([
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
    key: 'active_users_in_period',
    title: 'Active Users',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: UserGroupIcon,
    trend: null
  },
  {
    key: 'sessions_in_period',
    title: 'Chat Sessions',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: ChatBubbleLeftRightIcon,
    trend: null
  },
  {
    key: 'messages_in_period',
    title: 'Messages Exchanged',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: DocumentTextIcon,
    trend: null
  },
  {
    key: 'knowledge_files_count',
    title: 'Knowledge Files',
    value: 0,
    period: 'Total indexed files',
    loading: true,
    icon: ChartBarIcon,
    trend: null
  }
])



const fetchDashboardStats = async () => {
  error.value = null
  
  // Set all stats to loading
  stats.value.forEach(stat => {
    stat.loading = true
  })
  
  try {
    const response = await apiService.get(`/dashboard-stats?days=${selectedPeriod.value}`) as any
    
    // Update stats with response data
    stats.value.forEach(stat => {
      stat.loading = false
      stat.value = response[stat.key] || 0
      if (stat.key !== 'total_users' && stat.key !== 'knowledge_files_count') {
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





const checkKommoStatus = async () => {
  try {
    const response = await apiService.get('/kommo/integration/status') as any
    kommoStatus.value = response.active || false
  } catch (err) {
    kommoStatus.value = false
  }
}

// Computed properties for dynamic titles
const websiteName = computed(() => {
  const p: any = authStore.user?.profile
  const n = p?.custom_website_name ?? p?.customWebsiteName
  return typeof n === 'string' && n.trim() ? n.trim() : 'your AI chatbot'
})

const dashboardTitle = computed(() => {
  const p: any = authStore.user?.profile
  const customName = p?.custom_website_name ?? p?.customWebsiteName
  return customName && customName.trim() ? `${customName.trim()} Dashboard` : 'Dashboard'
})

onMounted(() => {
  fetchDashboardStats()
  checkKommoStatus()
})
</script>
