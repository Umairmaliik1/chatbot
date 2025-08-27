<template>
  <BaseLayout>
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Analytics</h1>
          <p class="mt-2 text-gray-600">Deep insights into your AI chatbot's performance and user engagement.</p>
        </div>
        <div class="flex items-center space-x-4">
          <select 
            v-model="selectedPeriod" 
            @change="loadAnalytics"
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

    <!-- Key Metrics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatCard
        v-for="metric in keyMetrics"
        :key="metric.key"
        :title="metric.title"
        :value="metric.value"
        :period="metric.period"
        :loading="metric.loading"
        :icon="metric.icon"
        :trend="metric.trend"
      />
    </div>

    <!-- Charts Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Usage Trends -->
      <BaseCard>
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">Usage Trends</h3>
          <p class="text-sm text-gray-600 mt-1">Daily active users and session growth</p>
        </div>
        <div class="card-body">
          <div class="h-80 flex items-center justify-center">
            <div v-if="isLoadingCharts" class="text-center">
              <div class="spinner w-8 h-8 mx-auto mb-4"></div>
              <p class="text-sm text-gray-500">Loading chart data...</p>
            </div>
            <div v-else class="text-center text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <p class="text-sm">Interactive charts will be implemented with Chart.js</p>
            </div>
          </div>
        </div>
      </BaseCard>

      <!-- Response Quality -->
      <BaseCard>
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">Response Quality</h3>
          <p class="text-sm text-gray-600 mt-1">User satisfaction and response accuracy</p>
        </div>
        <div class="card-body">
          <div class="h-80 flex items-center justify-center">
            <div v-if="isLoadingCharts" class="text-center">
              <div class="spinner w-8 h-8 mx-auto mb-4"></div>
              <p class="text-sm text-gray-500">Loading chart data...</p>
            </div>
            <div v-else class="text-center text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p class="text-sm">Quality metrics visualization</p>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>

    <!-- Performance Metrics -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
      <!-- Response Times -->
      <BaseCard>
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">Response Times</h3>
          <p class="text-sm text-gray-600 mt-1">Average AI response time</p>
        </div>
        <div class="card-body">
          <div class="text-center">
            <div class="text-3xl font-bold text-primary-600 mb-2">2.3s</div>
            <div class="text-sm text-gray-500 mb-4">Average response time</div>
            <div class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Fast (&lt;1s)</span>
                <span class="text-success-600">45%</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Normal (1-3s)</span>
                <span class="text-primary-600">40%</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Slow (&gt;3s)</span>
                <span class="text-warning-600">15%</span>
              </div>
            </div>
          </div>
        </div>
      </BaseCard>

      <!-- User Engagement -->
      <BaseCard>
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">User Engagement</h3>
          <p class="text-sm text-gray-600 mt-1">Session duration and interaction depth</p>
        </div>
        <div class="card-body">
          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Avg Session Duration</span>
              <span class="text-sm font-medium text-gray-900">4m 32s</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Messages per Session</span>
              <span class="text-sm font-medium text-gray-900">6.8</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Return Rate</span>
              <span class="text-sm font-medium text-gray-900">23%</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Completion Rate</span>
              <span class="text-sm font-medium text-gray-900">78%</span>
            </div>
          </div>
        </div>
      </BaseCard>

      <!-- Top Topics -->
      <BaseCard>
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">Top Topics</h3>
          <p class="text-sm text-gray-600 mt-1">Most discussed topics</p>
        </div>
        <div class="card-body">
          <div class="space-y-3">
            <div v-for="topic in topTopics" :key="topic.name" class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="w-2 h-2 rounded-full" :class="topic.color"></div>
                <span class="text-sm text-gray-900">{{ topic.name }}</span>
              </div>
              <span class="text-sm font-medium text-gray-900">{{ topic.percentage }}%</span>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>

    <!-- Detailed Analytics Table -->
    <BaseCard>
      <div class="card-header">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Daily Analytics</h3>
            <p class="text-sm text-gray-600 mt-1">Detailed breakdown by day</p>
          </div>
          <div class="flex items-center space-x-4">
            <BaseInput
              v-model="searchQuery"
              placeholder="Search analytics..."
              size="sm"
              class="w-64"
            />
          </div>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="table">
          <thead class="table-header">
            <tr>
              <th class="table-header-cell">Date</th>
              <th class="table-header-cell">Sessions</th>
              <th class="table-header-cell">Users</th>
              <th class="table-header-cell">Messages</th>
              <th class="table-header-cell">Avg Response Time</th>
              <th class="table-header-cell">Satisfaction</th>
            </tr>
          </thead>
          <tbody class="table-body">
            <tr v-if="isLoadingAnalytics" class="table-row">
              <td colspan="6" class="table-cell text-center py-8">
                <div class="flex items-center justify-center space-x-2">
                  <div class="spinner w-5 h-5"></div>
                  <span class="text-sm text-gray-500">Loading analytics...</span>
                </div>
              </td>
            </tr>
            <tr v-else v-for="day in dailyAnalytics" :key="day.date" class="table-row">
              <td class="table-cell">
                <div class="text-sm font-medium text-gray-900">{{ formatDate(day.date) }}</div>
                <div class="text-sm text-gray-500">{{ formatDayOfWeek(day.date) }}</div>
              </td>
              <td class="table-cell">
                <div class="text-sm text-gray-900">{{ day.sessions.toLocaleString() }}</div>
                <div class="text-sm" :class="day.sessions_growth > 0 ? 'text-success-500' : 'text-error-500'">
                  {{ day.sessions_growth > 0 ? '+' : '' }}{{ day.sessions_growth }}%
                </div>
              </td>
              <td class="table-cell">
                <div class="text-sm text-gray-900">{{ day.users.toLocaleString() }}</div>
                <div class="text-sm" :class="day.users_growth > 0 ? 'text-success-500' : 'text-error-500'">
                  {{ day.users_growth > 0 ? '+' : '' }}{{ day.users_growth }}%
                </div>
              </td>
              <td class="table-cell">
                <div class="text-sm text-gray-900">{{ day.messages.toLocaleString() }}</div>
                <div class="text-sm" :class="day.messages_growth > 0 ? 'text-success-500' : 'text-error-500'">
                  {{ day.messages_growth > 0 ? '+' : '' }}{{ day.messages_growth }}%
                </div>
              </td>
              <td class="table-cell">
                <div class="text-sm text-gray-900">{{ day.avg_response_time }}s</div>
                <div class="text-sm" :class="day.response_time_trend < 0 ? 'text-success-500' : 'text-error-500'">
                  {{ day.response_time_trend > 0 ? '+' : '' }}{{ day.response_time_trend }}%
                </div>
              </td>
              <td class="table-cell">
                <div class="flex items-center">
                  <div class="text-sm text-gray-900 mr-2">{{ day.satisfaction }}%</div>
                  <div class="w-16 bg-gray-200 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full" 
                      :class="getSatisfactionColor(day.satisfaction)"
                      :style="{ width: day.satisfaction + '%' }"
                    ></div>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseInput from '@/components/BaseInput.vue'
import StatCard from '@/components/StatCard.vue'
import { apiService } from '@/services/api'
// Using simple SVG icons instead of Heroicons
const ChartBarIcon = 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
const UserGroupIcon = 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z'
const ChatBubbleLeftRightIcon = 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'
const ClockIcon = 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'

const { error: showError } = useToast()

const selectedPeriod = ref('30')
const searchQuery = ref('')
const isLoadingCharts = ref(false)
const isLoadingAnalytics = ref(false)

const keyMetrics = ref([
  {
    key: 'total_sessions',
    title: 'Total Sessions',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: ChatBubbleLeftRightIcon,
    trend: null
  },
  {
    key: 'unique_users',
    title: 'Unique Users',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: UserGroupIcon,
    trend: null
  },
  {
    key: 'avg_response_time',
    title: 'Avg Response Time',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: ClockIcon,
    trend: null
  },
  {
    key: 'satisfaction_score',
    title: 'Satisfaction Score',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: ChartBarIcon,
    trend: null
  }
])

const topTopics = ref([
  { name: 'General Support', percentage: 35, color: 'bg-primary-500' },
  { name: 'Product Information', percentage: 28, color: 'bg-success-500' },
  { name: 'Technical Issues', percentage: 20, color: 'bg-warning-500' },
  { name: 'Billing Questions', percentage: 12, color: 'bg-error-500' },
  { name: 'Other', percentage: 5, color: 'bg-gray-500' }
])

const dailyAnalytics = ref([
  {
    date: '2024-01-15',
    sessions: 145,
    sessions_growth: 12,
    users: 98,
    users_growth: 8,
    messages: 892,
    messages_growth: 15,
    avg_response_time: 2.3,
    response_time_trend: -5,
    satisfaction: 87
  },
  {
    date: '2024-01-14',
    sessions: 132,
    sessions_growth: -3,
    users: 89,
    users_growth: 12,
    messages: 756,
    messages_growth: 8,
    avg_response_time: 2.1,
    response_time_trend: -8,
    satisfaction: 91
  },
  {
    date: '2024-01-13',
    sessions: 128,
    sessions_growth: 5,
    users: 85,
    users_growth: -2,
    messages: 689,
    messages_growth: 2,
    avg_response_time: 2.4,
    response_time_trend: 3,
    satisfaction: 84
  }
])

const loadAnalytics = async () => {
  isLoadingCharts.value = true
  isLoadingAnalytics.value = true

  try {
    // Load key metrics
    const metricsResponse = await apiService.get(`/analytics/metrics?days=${selectedPeriod.value}`)
    
    keyMetrics.value.forEach(metric => {
      metric.loading = false
      metric.value = metricsResponse[metric.key] || 0
      metric.period = `In the last ${selectedPeriod.value} days`
    })

    // Load daily analytics
    const dailyResponse = await apiService.get(`/analytics/daily?days=${selectedPeriod.value}`)
    dailyAnalytics.value = dailyResponse

  } catch (err: any) {
    showError('Failed to load analytics', err.message)
  } finally {
    isLoadingCharts.value = false
    isLoadingAnalytics.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatDayOfWeek = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', { weekday: 'short' })
}

const getSatisfactionColor = (score: number) => {
  if (score >= 80) return 'bg-success-500'
  if (score >= 60) return 'bg-warning-500'
  return 'bg-error-500'
}

onMounted(() => {
  loadAnalytics()
})
</script>
