import axios from 'axios'
import { ChatRequest, ChatResponse, ChatMessage } from '@/types/chat'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const chatApi = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/chat/message', request)
    return response.data
  },

  getHistory: async (sessionId: string): Promise<ChatMessage[]> => {
    const response = await api.get(`/chat/history/${sessionId}`)
    return response.data
  },

  clearHistory: async (sessionId: string): Promise<void> => {
    await api.delete(`/chat/history/${sessionId}`)
  },
}

export const ragApi = {
  uploadDocuments: async (files: File[]): Promise<{ message: string }> => {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })
    
    const response = await api.post('/rag/documents', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  getStats: async (): Promise<any> => {
    const response = await api.get('/rag/stats')
    return response.data
  },

  searchDocuments: async (query: string, k: number = 5): Promise<any> => {
    const response = await api.post('/rag/search', { query, k })
    return response.data
  },
}

export const healthApi = {
  check: async (): Promise<any> => {
    const response = await api.get('/health')
    return response.data
  },
}

export default api 