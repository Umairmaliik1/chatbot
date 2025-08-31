<template>
  <BaseLayout>
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Chat History</h1>
          <p class="mt-2 text-gray-600">View and manage your conversation history with the AI assistant.</p>
        </div>
        <BaseButton 
          v-if="sessions.length > 0"
          variant="error" 
          size="sm" 
          @click="deleteAllSessions"
          :loading="isDeletingAll"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Delete All
        </BaseButton>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 h-[calc(100vh-200px)]">
      <!-- Sessions List -->
      <BaseCard class="lg:col-span-1 flex flex-col">
        <div class="card-header">
          <h3 class="text-lg font-semibold text-gray-900">Chat Sessions</h3>
          <p class="text-sm text-gray-600 mt-1">{{ sessions.length }} total sessions</p>
        </div>
        
        <div class="flex-1 overflow-y-auto">
          <div v-if="sessions.length === 0" class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No chat sessions</h3>
            <p class="mt-1 text-sm text-gray-500">Start a conversation to see it here.</p>
          </div>
          
          <div v-else class="space-y-2 p-4">
            <div
              v-for="session in sessions"
              :key="session.id"
              class="flex items-center justify-between p-3 rounded-lg cursor-pointer transition-colors"
              :class="selectedSession?.id === session.id 
                ? 'bg-primary-50 border border-primary-200' 
                : 'hover:bg-gray-50 border border-transparent'"
              @click="selectSession(session)"
            >
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">{{ session.title }}</p>
                <p class="text-xs text-gray-500">{{ formatTimeAgo(session.updated_at) }}</p>
              </div>
              <button
                @click.stop="deleteSession(session.id)"
                class="ml-2 p-1 text-gray-400 hover:text-error-600 transition-colors"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </BaseCard>

      <!-- Chat Display -->
      <BaseCard class="lg:col-span-2 flex flex-col">
        <div v-if="!selectedSession" class="flex-1 flex items-center justify-center">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">Select a session</h3>
            <p class="mt-1 text-sm text-gray-500">Choose a chat session to view the conversation.</p>
          </div>
        </div>
        
        <div v-else class="flex flex-col h-full">
          <!-- Session Header -->
          <div class="card-header">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-semibold text-gray-900">{{ selectedSession.title }}</h3>
                <p class="text-sm text-gray-600">
                  {{ selectedMessages.length }} messages • 
                  {{ formatTimeAgo(selectedSession.updated_at) }}
                </p>
              </div>
              <BaseButton 
                variant="primary" 
                size="sm"
                @click="$router.push('/test-chat')"
              >
                Continue Chat
              </BaseButton>
            </div>
          </div>
          
          <!-- Messages -->
          <div class="flex-1 overflow-y-auto p-6 space-y-4">
            <div
              v-for="message in selectedMessages"
              :key="message.id"
              class="flex"
              :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div
                class="max-w-xs lg:max-w-md px-4 py-3 rounded-2xl"
                :class="message.role === 'user' 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-gray-100 text-gray-900'"
              >
                <div v-if="message.role === 'assistant'" class="whitespace-pre-wrap" v-html="linkify(message.content)"></div>
                <div v-else class="whitespace-pre-wrap">{{ message.content }}</div>
                <div class="text-xs mt-2 opacity-70">
                  {{ formatTime(message.timestamp) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useToast } from '@/composables/useToast'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import { apiService } from '@/services/api'
import { linkify } from '@/utils/linkify'

interface Session {
  id: number
  title: string
  created_at: string
  updated_at: string
  message_count: number
}

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

const { success: showSuccess, error: showError } = useToast()

const sessions = ref<Session[]>([])
const selectedSession = ref<Session | null>(null)
const selectedMessages = ref<Message[]>([])
const isLoading = ref(false)
const isDeletingAll = ref(false)

const loadSessions = async () => {
  try {
    const response = await apiService.get<Session[]>('/sessions')
    sessions.value = response
  } catch (err: any) {
    showError('Failed to load sessions', err.message)
  }
}

const selectSession = async (session: Session) => {
  selectedSession.value = session
  await loadSessionMessages(session.id)
}

const loadSessionMessages = async (sessionId: number) => {
  try {
    const response = await apiService.get<Message[]>(`/sessions/${sessionId}`)
    selectedMessages.value = response
  } catch (err: any) {
    showError('Failed to load messages', err.message)
  }
}

const deleteSession = async (sessionId: number) => {
  if (!confirm('Are you sure you want to delete this chat session?')) {
    return
  }
  
  try {
    await apiService.delete(`/sessions/${sessionId}`)
    sessions.value = sessions.value.filter(s => s.id !== sessionId)
    
    if (selectedSession.value?.id === sessionId) {
      selectedSession.value = null
      selectedMessages.value = []
    }
    
    showSuccess('Session deleted successfully')
  } catch (err: any) {
    showError('Failed to delete session', err.message)
  }
}

const deleteAllSessions = async () => {
  if (!confirm('Are you sure you want to delete ALL chat sessions? This action cannot be undone.')) {
    return
  }
  
  isDeletingAll.value = true
  
  try {
    await apiService.delete('/sessions/all')
    sessions.value = []
    selectedSession.value = null
    selectedMessages.value = []
    showSuccess('All sessions deleted successfully')
  } catch (err: any) {
    showError('Failed to delete all sessions', err.message)
  } finally {
    isDeletingAll.value = false
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

const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  loadSessions()
})
</script>
