<template>
  <BaseLayout>
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Reports & Analytics</h1>
          <p class="mt-2 text-gray-600">Comprehensive insights into your AI chatbot performance and usage patterns.</p>
        </div>
        <div class="flex items-center space-x-4">
          <select 
            v-model="selectedPeriod" 
            @change="loadReports"
            class="form-select w-48"
          >
            <option value="7">Last 7 Days</option>
            <option value="30">Last 30 Days</option>
            <option value="90">Last 90 Days</option>
            <option value="365">Last 365 Days</option>
          </select>
          <BaseButton variant="primary" size="sm" @click="exportReport">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export Report
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatCard
        v-for="stat in summaryStats"
        :key="stat.key"
        :title="stat.title"
        :value="stat.value"
        :period="stat.period"
        :loading="stat.loading"
        :icon="stat.icon"
        :trend="stat.trend"
      />
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Usage Chart -->
      <BaseCard>
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">Usage Trends</h3>
          <p class="text-sm text-gray-600 mt-1">Daily chat sessions and messages over time</p>
        </div>
        <div class="card-body">
          <div class="h-64 flex items-center justify-center">
            <div v-if="isLoadingCharts" class="text-center">
              <div class="spinner w-8 h-8 mx-auto mb-4"></div>
              <p class="text-sm text-gray-500">Loading chart data...</p>
            </div>
            <div v-else class="text-center text-gray-500">
              <svg class="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <p class="text-sm">Chart visualization will be implemented with Chart.js</p>
            </div>
          </div>
        </div>
      </BaseCard>

      <!-- Response Time Chart -->
      <BaseCard>
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">Response Times</h3>
          <p class="text-sm text-gray-600 mt-1">Average AI response time by hour</p>
        </div>
        <div class="card-body">
          <div class="h-64 flex items-center justify-center">
            <div v-if="isLoadingCharts" class="text-center">
              <div class="spinner w-8 h-8 mx-auto mb-4"></div>
              <p class="text-sm text-gray-500">Loading chart data...</p>
            </div>
            <div v-else class="text-center text-gray-500">
              <svg class="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p class="text-sm">Response time analytics will be displayed here</p>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>

    <!-- Xelence Media Reports -->
    <BaseCard v-if="xelenceCredentialsConfigured" class="mb-8">
      <div class="card-header">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Xelence Media Reports</h3>
            <p class="text-sm text-gray-600 mt-1">Media performance data from Xelence API</p>
          </div>
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <label class="text-sm font-medium text-gray-700">From:</label>
              <input
                v-model="xelenceFromDate"
                type="date"
                class="form-input w-40"
                @change="loadXelenceReports"
              />
            </div>
            <div class="flex items-center space-x-2">
              <label class="text-sm font-medium text-gray-700">To:</label>
              <input
                v-model="xelenceToDate"
                type="date"
                class="form-input w-40"
                @change="loadXelenceReports"
              />
            </div>
            <BaseButton
              variant="primary"
              size="sm"
              :loading="isLoadingXelenceReports"
              @click="loadXelenceReports"
            >
              Load Reports
            </BaseButton>
          </div>
        </div>
      </div>
      
      <div v-if="isLoadingXelenceReports" class="p-8 text-center">
        <div class="spinner w-8 h-8 mx-auto mb-4"></div>
        <p class="text-sm text-gray-500">Loading Xelence reports...</p>
      </div>
      
      <div v-else-if="xelenceReports.length === 0" class="p-8 text-center">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No Xelence reports found</h3>
        <p class="mt-1 text-sm text-gray-500">Select a date range and click "Load Reports" to fetch data.</p>
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="table">
          <thead class="table-header">
            <tr>
              <th class="table-header-cell">Date</th>
              <th class="table-header-cell">Brand</th>
              <th class="table-header-cell">Tracking Code</th>
              <th class="table-header-cell">Language</th>
              <th class="table-header-cell">Type</th>
              <th class="table-header-cell">Size</th>
              <th class="table-header-cell">Name</th>
              <th class="table-header-cell">Impressions</th>
              <th class="table-header-cell">Visitors</th>
              <th class="table-header-cell">Registrations</th>
              <th class="table-header-cell">FTD</th>
              <th class="table-header-cell">Commission</th>
            </tr>
          </thead>
          <tbody class="table-body">
            <tr v-for="report in xelenceReports" :key="`${report.Day}-${report.Brand}-${report.TrackingCode}`" class="table-row">
              <td class="table-cell">{{ report.Day || 'N/A' }}</td>
              <td class="table-cell">{{ report.Brand || 'N/A' }}</td>
              <td class="table-cell">{{ report.TrackingCode || 'N/A' }}</td>
              <td class="table-cell">{{ report.Language || 'N/A' }}</td>
              <td class="table-cell">{{ report.Type || 'N/A' }}</td>
              <td class="table-cell">{{ report.Size || 'N/A' }}</td>
              <td class="table-cell">{{ report.Name || 'N/A' }}</td>
              <td class="table-cell">{{ report.Impressions?.toLocaleString() || '0' }}</td>
              <td class="table-cell">{{ report.Visitors?.toLocaleString() || '0' }}</td>
              <td class="table-cell">{{ report.Registrations?.toLocaleString() || '0' }}</td>
              <td class="table-cell">{{ report.FTD?.toLocaleString() || '0' }}</td>
              <td class="table-cell">${{ report.Commission?.toFixed(2) || '0.00' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </BaseCard>

    <!-- Xelence Credentials Notice -->
    <BaseCard v-else class="mb-8">
      <div class="p-6 text-center">
        <svg class="mx-auto h-12 w-12 text-warning-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">Xelence Integration Required</h3>
        <p class="mt-1 text-sm text-gray-500">Configure your Xelence credentials in Settings to view media reports.</p>
        <div class="mt-6">
          <BaseButton variant="primary" @click="$router.push('/settings')">
            Go to Settings
          </BaseButton>
        </div>
      </div>
    </BaseCard>

    <!-- Detailed Reports Table -->
    <BaseCard>
      <div class="card-header">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">Chatbot Performance Reports</h3>
            <p class="text-sm text-gray-600 mt-1">Comprehensive breakdown of chatbot performance metrics</p>
          </div>
          <div class="flex items-center space-x-4">
            <BaseInput
              v-model="searchQuery"
              placeholder="Search reports..."
              size="sm"
              class="w-64"
            />
            <select v-model="selectedMetric" class="form-select w-40">
              <option value="all">All Metrics</option>
              <option value="sessions">Sessions</option>
              <option value="messages">Messages</option>
              <option value="response_time">Response Time</option>
              <option value="satisfaction">Satisfaction</option>
            </select>
          </div>
        </div>
      </div>
      
      <div class="overflow-x-auto">
        <table class="table">
          <thead class="table-header">
            <tr>
              <th class="table-header-cell">Date</th>
              <th class="table-header-cell">Sessions</th>
              <th class="table-header-cell">Messages</th>
              <th class="table-header-cell">Avg Response Time</th>
              <th class="table-header-cell">Satisfaction</th>
              <th class="table-header-cell">Actions</th>
            </tr>
          </thead>
          <tbody class="table-body">
            <tr v-if="isLoadingReports" class="table-row">
              <td colspan="6" class="table-cell text-center py-8">
                <div class="flex items-center justify-center space-x-2">
                  <div class="spinner w-5 h-5"></div>
                  <span class="text-sm text-gray-500">Loading reports...</span>
                </div>
              </td>
            </tr>
            <tr v-else-if="filteredReports.length === 0" class="table-row">
              <td colspan="6" class="table-cell text-center py-8">
                <div class="text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <h3 class="mt-2 text-sm font-medium text-gray-900">No reports found</h3>
                  <p class="mt-1 text-sm text-gray-500">Try adjusting your search or date range.</p>
                </div>
              </td>
            </tr>
            <tr v-else v-for="report in paginatedReports" :key="report.date" class="table-row">
              <td class="table-cell">
                <div class="text-sm font-medium text-gray-900">{{ formatDate(report.date) }}</div>
                <div class="text-sm text-gray-500">{{ formatDayOfWeek(report.date) }}</div>
              </td>
              <td class="table-cell">
                <div class="text-sm text-gray-900">{{ report.sessions.toLocaleString() }}</div>
                <div class="text-sm text-gray-500">{{ report.sessions_growth }}% vs prev</div>
              </td>
              <td class="table-cell">
                <div class="text-sm text-gray-900">{{ report.messages.toLocaleString() }}</div>
                <div class="text-sm text-gray-500">{{ report.messages_growth }}% vs prev</div>
              </td>
              <td class="table-cell">
                <div class="text-sm text-gray-900">{{ report.avg_response_time }}s</div>
                <div class="text-sm" :class="report.response_time_trend > 0 ? 'text-error-500' : 'text-success-500'">
                  {{ report.response_time_trend > 0 ? '+' : '' }}{{ report.response_time_trend }}% vs prev
                </div>
              </td>
              <td class="table-cell">
                <div class="flex items-center">
                  <div class="text-sm text-gray-900 mr-2">{{ report.satisfaction }}%</div>
                  <div class="w-16 bg-gray-200 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full" 
                      :class="getSatisfactionColor(report.satisfaction)"
                      :style="{ width: report.satisfaction + '%' }"
                    ></div>
                  </div>
                </div>
              </td>
              <td class="table-cell">
                <BaseButton variant="ghost" size="sm" @click="viewReportDetails(report)">
                  View Details
                </BaseButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div v-if="totalPages > 1" class="card-footer">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-700">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredReports.length) }} of {{ filteredReports.length }} results
          </div>
          <div class="flex items-center space-x-2">
            <BaseButton
              variant="secondary"
              size="sm"
              :disabled="currentPage === 1"
              @click="currentPage--"
            >
              Previous
            </BaseButton>
            <span class="text-sm text-gray-700">
              Page {{ currentPage }} of {{ totalPages }}
            </span>
            <BaseButton
              variant="secondary"
              size="sm"
              :disabled="currentPage === totalPages"
              @click="currentPage++"
            >
              Next
            </BaseButton>
          </div>
        </div>
      </div>
    </BaseCard>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useToast } from '@/composables/useToast'
import { useAuthStore } from '@/stores/auth'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import StatCard from '@/components/StatCard.vue'
import { apiService } from '@/services/api'
import { reportsService } from '@/services/reports'
// Using simple SVG icons instead of Heroicons
const ChartBarIcon = 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
const ChatBubbleLeftRightIcon = 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z'
const ClockIcon = 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'
const HeartIcon = 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z'

const { success: showSuccess, error: showError } = useToast()

const selectedPeriod = ref('30')
const searchQuery = ref('')
const selectedMetric = ref('all')
const currentPage = ref(1)
const itemsPerPage = 10

const isLoadingReports = ref(false)
const isLoadingCharts = ref(false)

// Xelence reports
const xelenceCredentialsConfigured = ref(false)
const xelenceReports = ref([])
const isLoadingXelenceReports = ref(false)
const xelenceFromDate = ref('')
const xelenceToDate = ref('')

const summaryStats = ref([
  {
    key: 'total_users',
    title: 'Total Users',
    value: 0,
    period: 'All time',
    loading: true,
    icon: HeartIcon,
    trend: null
  },
  {
    key: 'active_users_in_period',
    title: 'Active Users',
    value: 0,
    period: 'In the last 30 days',
    loading: true,
    icon: ClockIcon,
    trend: null
  },
  {
    key: 'sessions_in_period',
    title: 'Total Sessions',
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
    icon: ChartBarIcon,
    trend: null
  }
])

const reports = ref([
  {
    date: '2024-01-15',
    sessions: 145,
    sessions_growth: 12,
    messages: 892,
    messages_growth: 8,
    avg_response_time: 2.3,
    response_time_trend: -5,
    satisfaction: 87
  },
  {
    date: '2024-01-14',
    sessions: 132,
    sessions_growth: -3,
    messages: 756,
    messages_growth: 15,
    avg_response_time: 2.1,
    response_time_trend: -8,
    satisfaction: 91
  },
  {
    date: '2024-01-13',
    sessions: 128,
    sessions_growth: 5,
    messages: 689,
    messages_growth: 2,
    avg_response_time: 2.4,
    response_time_trend: 3,
    satisfaction: 84
  }
])

const filteredReports = computed(() => {
  let filtered = Array.isArray(reports.value) ? reports.value : []

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(report => 
      report.date.includes(query) ||
      report.sessions.toString().includes(query) ||
      report.messages.toString().includes(query)
    )
  }

  if (selectedMetric.value !== 'all') {
    // Filter by metric type if needed
  }

  return filtered.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
})

const totalPages = computed(() => Math.ceil(filteredReports.value.length / itemsPerPage))

const paginatedReports = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredReports.value.slice(start, end)
})

const loadXelenceReports = async () => {
  if (!xelenceFromDate.value || !xelenceToDate.value) {
    showError('Please select both from and to dates')
    return
  }

  isLoadingXelenceReports.value = true

  try {
    // Use getDirect to avoid the params wrapper issue
    const response = await apiService.getDirect('/reports', {
      fromdate: xelenceFromDate.value,
      todate: xelenceToDate.value
    })
    
    xelenceReports.value = Array.isArray(response.reports) ? response.reports : []
    
    if (xelenceReports.value.length === 0) {
      showSuccess('No data found for the selected date range')
    } else {
      showSuccess(`Loaded ${xelenceReports.value.length} Xelence reports`)
    }
  } catch (err: any) {
    if (err.response?.status === 400 && err.response?.data?.detail?.includes('credentials')) {
      showError('Xelence credentials not configured', 'Please configure your Xelence credentials in Settings')
      xelenceCredentialsConfigured.value = false
    } else if (err.response?.status === 401) {
      showError('Authentication failed', 'Please check your Xelence credentials in Settings')
    } else {
      showError('Failed to load Xelence reports', err.message)
    }
  } finally {
    isLoadingXelenceReports.value = false
  }
}

const loadReports = async () => {
  isLoadingReports.value = true
  isLoadingCharts.value = true

  try {
    // Determine date range for reports
    const to = new Date()
    const todate = to.toISOString().split('T')[0]
    const from = new Date()
    from.setDate(from.getDate() - Number(selectedPeriod.value))
    const fromdate = from.toISOString().split('T')[0]

    // Load summary stats
    const statsResponse = await reportsService.getDashboardStats(Number(selectedPeriod.value))

    summaryStats.value.forEach(stat => {
      stat.loading = false
      stat.value = statsResponse[stat.key] || 0
      stat.period = stat.key === 'total_users'
        ? 'All time'
        : `In the last ${selectedPeriod.value} days`
    })

    // Load detailed reports
    const reportsResponse = await reportsService.getReports({ fromdate, todate })
    reports.value = Array.isArray(reportsResponse) ? reportsResponse : []

  } catch (err: any) {
    showError('Failed to load reports', err.message)
  } finally {
    isLoadingReports.value = false
    isLoadingCharts.value = false
  }
}

const exportReport = async () => {
  try {
    const response = await apiService.get(`/reports/export?days=${selectedPeriod.value}`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `chatbot-report-${selectedPeriod.value}days.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    showSuccess('Report exported successfully!')
  } catch (err: any) {
    showError('Failed to export report', err.message)
  }
}

const viewReportDetails = (report: any) => {
  // Implement report details modal or navigation
  showSuccess('Report details', `Viewing details for ${report.date}`)
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

const checkXelenceCredentials = () => {
  // Use existing user data from auth store instead of making API call
  const authStore = useAuthStore()
  
  if (authStore.user?.profile) {
    const hasAffiliateId = !!authStore.user.profile.xelence_affiliateid
    const hasApiKey = !!authStore.user.profile.xelence_x_api_key
    
    xelenceCredentialsConfigured.value = hasAffiliateId && hasApiKey
  } else {
    xelenceCredentialsConfigured.value = false
  }
}

const initializeDateRange = () => {
  const today = new Date()
  const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate())
  
  xelenceToDate.value = today.toISOString().split('T')[0]
  xelenceFromDate.value = lastMonth.toISOString().split('T')[0]
}

onMounted(async () => {
  // Wait for auth store to be initialized if needed
  const authStore = useAuthStore()
  if (authStore.user === null && !authStore.isLoading) {
    await authStore.initializeAuth()
  }
  
  loadReports()
  checkXelenceCredentials()
  initializeDateRange()
})
</script>
