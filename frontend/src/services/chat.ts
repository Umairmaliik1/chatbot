import { apiService } from './api'

export interface ChatMessage {
  id?: number
  content: string
  role: 'user' | 'assistant'
  timestamp?: string
  session_id?: number
}

export interface ChatSession {
  id: number
  title: string
  created_at: string
  updated_at: string
  message_count: number
}

export interface ChatMemory {
  session_id: number
  memory_type: string
  content: string
  created_at: string
}

export class ChatService {
  // Chat API endpoints
  async sendMessage(message: string, sessionId: number): Promise<ChatMessage> {
    return await apiService.post('/chat', {
      message,
      session_id: sessionId
    })
  }

  async streamMessage(message: string, sessionId: number, onChunk: (chunk: string) => void): Promise<void> {
    return await apiService.stream('/chat', {
      message,
      session_id: sessionId
    }, onChunk)
  }

  // Chat Sessions
  async createSession(): Promise<ChatSession> {
    return await apiService.post('/chat-sessions')
  }

  async getSessions(): Promise<ChatSession[]> {
    return await apiService.get('/chat-sessions')
  }

  async deleteSession(sessionId: number): Promise<void> {
    return await apiService.delete(`/chat-sessions/${sessionId}`)
  }

  // Chat History
  async getChatHistory(sessionId: number): Promise<ChatMessage[]> {
    return await apiService.get(`/chat-history/${sessionId}`)
  }

  // Chat Memory
  async getChatMemory(sessionId: number): Promise<ChatMemory> {
    return await apiService.get(`/chat-memory/${sessionId}`)
  }

  async clearChatMemory(sessionId: number): Promise<void> {
    return await apiService.delete(`/chat-memory/${sessionId}`)
  }

  // Test endpoint
  async testConnection(): Promise<{ message: string }> {
    return await apiService.get('/test')
  }
}

export const chatService = new ChatService()

