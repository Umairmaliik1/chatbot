<template>
  <BaseLayout>
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Test Fine-Tuned Model</h1>
          <p class="mt-2 text-gray-600">Test your AI chatbot with real-time responses powered by Gemini AI.</p>
        </div>
        <div class="flex items-center space-x-4">
          <BaseButton variant="secondary" size="sm" @click="startNewChat">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            New Chat
          </BaseButton>
          <BaseButton variant="secondary" size="sm" @click="testAPI">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Test API
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- Chat Container -->
    <BaseCard class="h-[70vh] flex flex-col">
      <!-- Messages Area -->
      <div class="flex-1 overflow-y-auto p-6 space-y-4" ref="messagesContainer">
        <div v-if="messages.length === 0" class="text-center py-12">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Start a conversation</h3>
          <p class="text-gray-500">Ask me anything to test the AI chatbot!</p>
        </div>

        <div
          v-for="message in messages"
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
            <div class="whitespace-pre-wrap">{{ message.content }}</div>
            <div class="text-xs mt-2 opacity-70">
              {{ formatTime(message.timestamp) }}
            </div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex justify-start">
          <div class="bg-gray-100 text-gray-900 px-4 py-3 rounded-2xl">
            <div class="flex items-center space-x-1">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="border-t border-gray-200 p-6">
        <form @submit.prevent="sendMessage" class="flex items-end space-x-4">
          <div class="flex-1">
            <BaseInput
              v-model="inputMessage"
              placeholder="Type your message..."
              :disabled="isLoading"
              @keydown.enter.exact="sendMessage"
              @keydown.shift.enter="inputMessage += '\n'"
            />
          </div>
          <BaseButton
            type="submit"
            variant="primary"
            :loading="isLoading"
            :disabled="!inputMessage.trim()"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </BaseButton>
        </form>
      </div>
    </BaseCard>
  </BaseLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useToast } from '@/composables/useToast'
import BaseLayout from '@/components/BaseLayout.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import { apiService } from '@/services/api'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const { success: showSuccess, error: showError } = useToast()

const messages = ref<Message[]>([])
const inputMessage = ref('')
const isLoading = ref(false)
const isTyping = ref(false)
const currentSessionId = ref<number | null>(null)
const messagesContainer = ref<HTMLElement>()

const addMessage = (role: 'user' | 'assistant', content: string) => {
  const message: Message = {
    id: Math.random().toString(36).substr(2, 9),
    role,
    content,
    timestamp: new Date()
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

const formatTime = (date: Date) => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const startNewChat = () => {
  messages.value = []
  currentSessionId.value = null
  addMessage('assistant', "Hello! I'm powered by Gemini AI. How can I help you today?")
}

const testAPI = async () => {
  try {
    showSuccess('Testing API connectivity...')
    
    // Test basic endpoint
    const testResponse = await apiService.get('/test')
    console.log('Test endpoint response:', testResponse)
    
    // Test session creation
    const sessionResponse = await apiService.post('/chat-sessions')
    console.log('Session creation response:', sessionResponse)
    
    showSuccess('API test successful!', 'All endpoints are working correctly.')
  } catch (err: any) {
    showError('API test failed', err.message)
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isLoading.value) return

  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''
  
  // Add user message
  addMessage('user', userMessage)
  
  isLoading.value = true
  isTyping.value = true

  try {
    // Create session if needed
    if (!currentSessionId.value) {
      const sessionResponse = await apiService.post<{ session_id: number }>('/chat-sessions')
      currentSessionId.value = sessionResponse.session_id
    }

    // Send message and stream response
    let assistantResponse = ''
    const assistantMessageId = Math.random().toString(36).substr(2, 9)
    
    // Add empty assistant message
    const assistantMessage: Message = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      timestamp: new Date()
    }
    messages.value.push(assistantMessage)
    scrollToBottom()

    await apiService.stream('/chat', {
      message: userMessage,
      session_id: currentSessionId.value
    }, (chunk: string) => {
      assistantResponse += chunk
      // Update the assistant message content
      const messageIndex = messages.value.findIndex(m => m.id === assistantMessageId)
      if (messageIndex !== -1) {
        messages.value[messageIndex].content = assistantResponse
        scrollToBottom()
      }
    })

  } catch (err: any) {
    showError('Failed to send message', err.message)
    // Remove the empty assistant message if there was an error
    messages.value = messages.value.filter(m => m.content !== '')
  } finally {
    isLoading.value = false
    isTyping.value = false
  }
}

// Watch for typing state changes
watch(isTyping, (newValue) => {
  if (newValue) {
    scrollToBottom()
  }
})

onMounted(() => {
  startNewChat()
})
</script>
