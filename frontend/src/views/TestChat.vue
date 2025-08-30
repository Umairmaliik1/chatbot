<template>
  <BaseLayout>
    <!-- Modern Top Navigation Bar -->
    <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-sm mb-6 overflow-hidden">
      <!-- Header Bar -->
      <div class="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 px-6 py-4 border-b border-gray-100 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900 dark:text-white">AI Chat Assistant</h1>
              <p class="text-sm text-gray-600 dark:text-gray-400">Powered by AI Bot</p>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center space-x-3">
            <div class="hidden sm:flex items-center space-x-3">
              <BaseButton 
                variant="secondary" 
                size="sm" 
                @click="testAPI"
                class="flex items-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Test API
              </BaseButton>
              <BaseButton 
                variant="primary" 
                size="sm" 
                @click="startNewChat"
                class="flex items-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                New Chat
              </BaseButton>
            </div>
            
            <!-- Session Selector Dropdown -->
            <div class="relative">
              <button 
                ref="sessionBtnEl"
                @click="toggleSessionDropdown"
                class="flex items-center space-x-2 px-4 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                :class="showSessionDropdown ? 'ring-2 ring-indigo-500 border-indigo-500' : ''"
              >
                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300 max-w-32 truncate">
                  {{ getCurrentSessionTitle() }}
                </span>
                <svg 
                  class="w-4 h-4 text-gray-400 dark:text-gray-500 transition-transform duration-200" 
                  :class="showSessionDropdown ? 'rotate-180' : ''"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- Teleported dropdown + overlay (prevents clipping by overflow) -->
              <teleport to="body">
                <!-- Click-outside overlay -->
                <div
                  v-if="showSessionDropdown"
                  class="fixed inset-0 z-[9998]"
                  @click="showSessionDropdown = false"
                ></div>

                <!-- Dropdown Menu -->
                <div
                  v-if="showSessionDropdown"
                  class="session-dropdown fixed z-[9999] w-80"
                  :style="dropdownStyle"
                >
                  <div class="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700">
                    <div class="flex items-center justify-between">
                      <h3 class="font-semibold text-gray-900 dark:text-white">Chat Sessions ({{ chatSessions.length }})</h3>
                      <button @click="loadChatSessions" class="text-xs bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600">Reload</button>
                    </div>
                  </div>
                  <div class="bg-white dark:bg-gray-800" style="min-height: 200px; max-height: 400px; overflow-y: auto;">
                    <!-- Session List -->
                    <div v-if="chatSessions && chatSessions.length > 0">
                      <div v-for="session in chatSessions" :key="session.id" 
                          class="session-item p-4 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 cursor-pointer border-b border-gray-100 dark:border-gray-700 last:border-b-0 transition-colors"
                          :class="currentSessionId === session.id ? 'bg-indigo-50 dark:bg-indigo-900/30 border-l-4 border-l-indigo-500' : ''"
                          @click="selectSession(session.id)">
                        <div class="flex items-center justify-between">
                          <div class="flex-1 min-w-0">
                            <h4 class="text-sm font-medium text-gray-900 dark:text-white truncate">
                              {{ session.title || `Session ${session.id}` }}
                            </h4>
                            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                              {{ formatDate(session.created_at) }}
                            </p>
                          </div>
                          <button
                            @click.stop="deleteSession(session.id)"
                            class="ml-2 p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-md transition-colors"
                            title="Delete session"
                          >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Empty State -->
                    <div v-else class="p-6 text-center">
                      <div class="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                        <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                        </svg>
                      </div>
                      <p class="text-sm text-gray-500">No chat sessions found</p>
                      <p class="text-xs text-gray-400 mt-1">Create your first chat to get started</p>
                    </div>
                  </div>
                </div>
              </teleport>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Session Status Bar -->
      <div class="px-6 py-3 bg-gray-50 border-b border-gray-100">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div class="w-2 h-2 rounded-full" :class="currentSessionId ? 'bg-green-400' : 'bg-gray-300'"></div>
            <span class="text-sm text-gray-600">
              {{ currentSessionId ? `Session ${currentSessionId} • ${messages.length} messages` : 'No active session' }}
            </span>
          </div>
          <div class="flex items-center space-x-2">
            <button 
              v-if="currentSessionId && messages.length > 0"
              @click="clearChat"
              class="text-xs text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
            >
              Clear Chat
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Chat Interface -->
    <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-sm overflow-hidden">
      <!-- Messages Area -->
      <div 
        class="h-[calc(100vh-280px)] min-h-[500px] overflow-y-auto px-3 sm:px-6 py-4"
        ref="messagesContainer"
      >
        <!-- Welcome State -->
        <div v-if="messages.length === 0" class="welcome-state">
          <div class="welcome-content">
            <div class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Ready to chat!</h3>
            <p class="text-gray-500 dark:text-gray-400 text-sm max-w-md mx-auto">
              {{ currentSessionId 
                ? 'Start a conversation by typing your message below.' 
                : 'Create a new chat session to begin your AI conversation.' 
              }}
            </p>
          </div>
        </div>

        <!-- Corporate Chat Thread (with date dividers) -->
        <div v-else class="max-w-3xl mx-auto">
          <template v-for="(message, index) in messagesChrono" :key="message.id">
            <!-- Date divider -->
            <div v-if="shouldShowDateDivider(messagesChrono, index)" class="flex items-center my-6">
              <div class="flex-1 h-px bg-gray-200 dark:bg-gray-600"></div>
              <div class="px-3 text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                {{ formatDateDivider(new Date(message.timestamp)) }}
              </div>
              <div class="flex-1 h-px bg-gray-200 dark:bg-gray-600"></div>
            </div>

            <!-- Message bubble row -->
            <div class="mb-4">
              <div class="flex items-end" :class="message.role === 'user' ? 'justify-end' : 'justify-start'">
                <!-- Assistant avatar (left) -->
                <div v-if="message.role === 'assistant'" class="mr-3 shrink-0">
                  <div class="assistant-avatar shadow-sm">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                  </div>
                </div>

                <!-- Bubble -->
                <div class="max-w-[85%] sm:max-w-[70%]">
                  <div
                    class="rounded-2xl px-4 py-2 text-[15px] leading-relaxed shadow-sm"
                    :class="message.role === 'user'
                      ? 'bg-indigo-600 text-white rounded-br-md'
                      : 'bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 text-gray-800 dark:text-gray-200 rounded-bl-md'"
                  >
                    {{ message.content }}
                  </div>
                  <div
                    class="mt-1 text-[11px] text-gray-500 dark:text-gray-400"
                    :class="message.role === 'user' ? 'text-right pr-1' : 'text-left pl-1'"
                  >
                    {{ formatTime(message.timestamp) }}
                  </div>
                </div>

                <!-- User avatar (right) -->
                <div v-if="message.role === 'user'" class="ml-3 shrink-0">
                  <div class="user-avatar shadow-sm">
                    <span class="user-initial">{{ userInitial }}</span>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="mb-4">
            <div class="flex items-end">
              <div class="mr-3 shrink-0">
                <div class="assistant-avatar shadow-sm">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                </div>
              </div>
              <div class="max-w-[70%]">
                <div class="rounded-2xl px-4 py-2 border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-md">
                  <div class="typing-dots flex gap-1 items-center">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                  </div>
                </div>
                <div class="mt-1 text-[11px] text-gray-500 dark:text-gray-400 pl-1">Typing…</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="border-t border-gray-100 dark:border-gray-700 bg-gradient-to-r from-gray-50 to-gray-100/50 dark:from-gray-800 dark:to-gray-700/50 p-6">
        <form @submit.prevent="sendMessage" class="space-y-4">
          <!-- Main Input Row -->
          <div class="flex items-end space-x-4">
            <div class="flex-1">
              <div class="relative">
                <BaseInput
                  v-model="inputMessage"
                  :placeholder="currentSessionId ? 'Type your message... (Enter to send)' : 'Create a new chat session first'"
                  :disabled="!currentSessionId || isLoading"
                  @keydown.enter.exact="sendMessage"
                  @keydown.shift.enter="inputMessage += '\n'"
                  class="pr-16 py-4 text-base min-h-[3rem] resize-none"
                  style="height: auto; min-height: 3rem;"
                />
                <div class="absolute right-4 top-1/2 transform -translate-y-1/2">
                  <div class="flex items-center space-x-2">
                    <span class="text-xs text-gray-400 dark:text-gray-500">
                      {{ inputMessage.length }}
                    </span>
                    <div class="w-px h-4 bg-gray-300 dark:bg-gray-600"></div>
                    <span class="text-xs text-gray-400 dark:text-gray-500">
                      {{ currentSessionId ? '↵' : '!' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Send/Action Button -->
            <div class="flex space-x-2">
              <BaseButton
                v-if="!isLoading && currentSessionId"
                type="submit"
                variant="primary"
                :disabled="!inputMessage.trim()"
                class="px-6 py-3 h-12 rounded-xl flex items-center justify-center min-w-[3rem]"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </BaseButton>
              
              <BaseButton
                v-else-if="isLoading"
                type="button"
                variant="secondary"
                @click="cancelMessage"
                class="px-6 py-3 h-12 rounded-xl flex items-center justify-center min-w-[3rem]"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </BaseButton>

              <BaseButton
                v-else
                type="button"
                variant="primary"
                @click="startNewChat"
                class="px-6 py-3 h-12 rounded-xl flex items-center justify-center whitespace-nowrap"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                New Chat
              </BaseButton>
            </div>
          </div>
          
          <!-- Helper Text -->
          <div class="flex items-center justify-between text-xs text-gray-500">
            <div class="flex items-center space-x-4">
              <span>💡 Tip: Be specific for better responses</span>
            </div>
            <div class="flex items-center space-x-2">
              <span class="hidden sm:inline">Press Shift+Enter for new line</span>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Mobile Quick Actions -->
    <div class="mt-4 sm:hidden">
      <div class="grid grid-cols-2 gap-2">
        <BaseButton 
          variant="secondary" 
          @click="startNewChat"
          class="flex items-center justify-center py-3"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          New Chat
        </BaseButton>
        <BaseButton 
          variant="secondary" 
          @click="testAPI"
          class="flex items-center justify-center py-3"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Test API
        </BaseButton>
      </div>
    </div>
    <!-- (NOTE) removed old in-component overlay; handled via teleport -->
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick, watch, computed } from 'vue'
import { useToast } from '@/composables/useToast'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import { chatService } from '@/services/chat'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ChatSession {
  id: number
  title: string
  created_at: string
  updated_at: string
}

const { success: showSuccess, error: showError } = useToast()

const messages = ref<Message[]>([])
const inputMessage = ref('')
const isLoading = ref(false)
const isTyping = ref(false)
const currentSessionId = ref<number | null>(null)
const messagesContainer = ref<HTMLElement>()
const abortController = ref<AbortController | null>(null)
const chatSessions = ref<ChatSession[]>([])
const showSessionDropdown = ref(false)

// NEW: refs & style for teleported dropdown positioning
const sessionBtnEl = ref<HTMLElement | null>(null)
const dropdownStyle = ref<Record<string, string>>({})

// Computed properties
const userInitial = computed(() => 'U') // You can get this from auth store later

const toDate = (d: unknown): Date => {
  if (d instanceof Date) return d
  const parsed = new Date(String(d))
  return isNaN(parsed.getTime()) ? new Date() : parsed
}

const formatTime = (dateLike: Date | string) => {
  const d = toDate(dateLike)
  return new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit', hour12: true }).format(d)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric' }).format(date)
}

const formatDateDivider = (d: Date) => {
  const now = new Date()
  const sameDay = (a: Date, b: Date) => a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()
  const yesterday = new Date(now); yesterday.setDate(now.getDate() - 1)
  if (sameDay(d, now)) return 'Today'
  if (sameDay(d, yesterday)) return 'Yesterday'
  return new Intl.DateTimeFormat(undefined, { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }).format(d)
}

// Ensure chronological order even if API returns newest-first
const messagesChrono = computed(() =>
  [...messages.value].sort((a, b) => toDate(a.timestamp).getTime() - toDate(b.timestamp).getTime())
)

const shouldShowDateDivider = (arr: Message[], index: number) => {
  if (index === 0) return true
  const prev = toDate(arr[index - 1].timestamp)
  const curr = toDate(arr[index].timestamp)
  return prev.toDateString() !== curr.toDateString()
}

const getCurrentSessionTitle = () => {
  if (!currentSessionId.value) return 'No Session'
  const session = chatSessions.value.find(s => s.id === currentSessionId.value)
  return session?.title || 'New Chat'
}

const positionDropdown = () => {
  const el = sessionBtnEl.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  const width = 320 // w-80 = 20rem
  const gap = 8

  let left = rect.right - width
  left = Math.min(Math.max(8, left), window.innerWidth - width - 8)
  const top = rect.bottom + gap

  dropdownStyle.value = {
    top: `${top}px`,
    left: `${left}px`,
  }
}

const selectSession = async (sessionId: number) => {
  showSessionDropdown.value = false
  try {
    await loadSession(sessionId)
  } catch (error) {
    showError('Failed to load session', 'Please try again')
  }
}

// UPDATED: toggle computes position after showing
const toggleSessionDropdown = async () => {
  showSessionDropdown.value = !showSessionDropdown.value
  if (showSessionDropdown.value) {
    await nextTick()
    positionDropdown()
  }
}

const addMessage = (role: 'user' | 'assistant', content: string, when?: Date | string) => {
  const message: Message = {
    id: Math.random().toString(36).substr(2, 9),
    role,
    content,
    timestamp: when ? toDate(when) : new Date()
  }
  messages.value.push(message)
  scrollToBottom()
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const loadChatSessions = async () => {
  try {
    const sessions = await chatService.getSessions()
    chatSessions.value = Array.isArray(sessions) ? sessions : []
  } catch (err: any) {
    showError('Failed to load sessions', err.message || 'Unknown error')
    chatSessions.value = []
  }
}

const loadSession = async (sessionId: number) => {
  try {
    currentSessionId.value = sessionId
    const history = await chatService.getChatHistory(sessionId)

    // Convert database messages to local format (use server timestamps exactly)
    if (Array.isArray(history)) {
      messages.value = history.map(msg => ({
        id: msg.id?.toString() || Math.random().toString(36).substr(2, 9),
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
        timestamp: msg.created_at ? new Date(msg.created_at) : new Date() // Add fallback for undefined
      }))
    } else {
      messages.value = []
    }
    scrollToBottom()
  } catch (err: any) {
    showError('Failed to load session', err.message || 'Unknown error')
  }
}

const deleteSession = async (sessionId: number) => {
  try {
    await chatService.deleteSession(sessionId)
    chatSessions.value = chatSessions.value.filter(s => s.id !== sessionId)
    if (currentSessionId.value === sessionId) {
      currentSessionId.value = null
      messages.value = []
    }
    showSuccess('Session deleted', 'Chat session has been removed.')
  } catch (err: any) {
    showError('Failed to delete session', err.message)
  }
}

const startNewChat = async () => {
  try {
    // Create new session
    const session = await chatService.createSession()
    currentSessionId.value = session.id
    
    // Add to sessions list
    chatSessions.value.unshift({
      id: session.id,
      title: 'New Chat',
      created_at: session.created_at,
      updated_at: session.updated_at
    })
    
    // Clear messages and add welcome message (timestamped now)
    messages.value = []
    addMessage('assistant', "Hello! I'm your AI Bot assistant. How can I help you today?", new Date())
    
    // Cancel any ongoing request
    if (abortController.value) {
      abortController.value.abort()
      abortController.value = null
    }
  } catch (err: any) {
    showError('Failed to create new chat', err.message)
  }
}

const clearChat = () => {
  if (isLoading.value) {
    showError('Cannot clear chat', 'Please wait for the current message to complete.')
    return
  }
  messages.value = []
  if (abortController.value) {
    abortController.value.abort()
    abortController.value = null
  }
  showSuccess('Chat cleared', 'All messages have been removed.')
}

const cancelMessage = () => {
  if (abortController.value) {
    abortController.value.abort()
    abortController.value = null
  }
  isLoading.value = false
  isTyping.value = false
  showError('Message cancelled', 'The message request was cancelled.')
}

const testAPI = async () => {
  try {
    showSuccess('Testing API connectivity...')
    await chatService.testConnection()
    const sessionResponse = await chatService.createSession()
    console.log('Session creation response:', sessionResponse)
    showSuccess('API test successful!', 'All endpoints are working correctly.')
  } catch (err: any) {
    showError('API test failed', err.message)
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value || !currentSessionId.value) return

  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''
  
  // Add user message (real local time)
  addMessage('user', userMessage, new Date())
  
  isLoading.value = true
  isTyping.value = true

  // Send message and stream response
  let assistantResponse = ''
  const assistantMessageId = Math.random().toString(36).substr(2, 9)
  
  // Add empty assistant message to stream into
  const assistantMessage: Message = {
    id: assistantMessageId,
    role: 'assistant',
    content: '',
    timestamp: new Date()
  }
  messages.value.push(assistantMessage)
  scrollToBottom()

  try {
    await chatService.streamMessage(userMessage, currentSessionId.value, (chunk: string) => {
      if (chunk && chunk.trim()) {
        assistantResponse += chunk
        const messageIndex = messages.value.findIndex(m => m.id === assistantMessageId)
        if (messageIndex !== -1) {
          messages.value[messageIndex].content = assistantResponse
          scrollToBottom()
        }
      }
    })

    if (!assistantResponse.trim()) {
      throw new Error('No response received from the AI')
    }

    // Update session title with first user message if it's still "New Chat"
    const currentSession = chatSessions.value.find(s => s.id === currentSessionId.value)
    if (currentSession && currentSession.title === 'New Chat') {
      const newTitle = userMessage.length > 50 ? userMessage.substring(0, 50) + '...' : userMessage
      currentSession.title = newTitle
      try {
        await chatService.updateSessionTitle(currentSessionId.value, newTitle)
      } catch (err: any) {
        console.error('Failed to update session title:', err)
      }
    }

  } catch (err: any) {
    showError('Failed to send message', err.message)
    // Remove the empty assistant message if there was an error
    messages.value = messages.value.filter(m => m.id !== assistantMessageId)  
  } finally {
    isLoading.value = false
    isTyping.value = false
  }
}

// Reposition teleported dropdown on resize/scroll while open
const onWinChange = () => {
  if (showSessionDropdown.value) positionDropdown()
}

// Watch for typing state changes
watch(isTyping, (newValue) => {
  if (newValue) {
    scrollToBottom()
  }
})

onMounted(async () => {
  window.addEventListener('resize', onWinChange)
  // capture=true to catch scrolls in nested containers
  window.addEventListener('scroll', onWinChange, true)

  await loadChatSessions()
  
  // Don't auto-create sessions - user must manually create them
  if (chatSessions.value.length === 0) {
    currentSessionId.value = null
    messages.value = []
  } else {
    await loadSession(chatSessions.value[0].id)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onWinChange)
  window.removeEventListener('scroll', onWinChange, true)
})
</script>

<style scoped>
/* Chat container base */
.welcome-state { padding: 48px 24px; text-align: center; }
.welcome-content { max-width: 768px; margin: 0 auto; }

/* Avatars */
.user-avatar {
  width: 30px; height: 30px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #fff;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}
.user-initial { font-size: 13px; font-weight: 700; }
.assistant-avatar {
  width: 30px; height: 30px; background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

/* Typing Animation */
.typing-dots .typing-dot {
  width: 6px; height: 6px; border-radius: 9999px; background: #9CA3AF; animation: typing-bounce 1.2s infinite ease-in-out;
}
.dark .typing-dots .typing-dot {
  background: #6B7280;
}
.typing-dots .typing-dot:nth-child(2) { animation-delay: .2s; }
.typing-dots .typing-dot:nth-child(3) { animation-delay: .4s; }
@keyframes typing-bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: .3; }
  40% { transform: translateY(-2px); opacity: 1; }
}

/* Scrollbar (optional polish) */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: linear-gradient(to bottom, #d1d5db, #9ca3af); border-radius: 6px; }
::-webkit-scrollbar-thumb:hover { background: linear-gradient(to bottom, #9ca3af, #6b7280); }

/* Dropdown Styling */
.session-dropdown {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15), 0 4px 6px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
  animation: dropdownSlideIn 0.2s ease-out;
}
.dark .session-dropdown {
  background: #374151;
  border-color: #4b5563;
}
.session-item:hover { background: #f0f4ff !important; }
.dark .session-item:hover { background: #4338ca40 !important; }
@keyframes dropdownSlideIn {
  from { opacity: 0; transform: translateY(-10px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* Focus */
button:focus-visible { outline: 2px solid #6366f1; outline-offset: 2px; }

/* Subtle transitions */
* { transition: color .2s ease, background-color .2s ease, border-color .2s ease, transform .2s ease, box-shadow .2s ease; }

/* Responsive tweaks */
@media (max-width: 640px) {
  .welcome-state { padding: 32px 16px; }
}
</style>
