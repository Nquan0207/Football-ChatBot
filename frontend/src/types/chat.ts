export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
  session_id?: string
}

export interface ChatRequest {
  message: string
  session_id?: string
  use_rag?: boolean
  context?: string[]
}

export interface ChatResponse {
  message: string
  session_id: string
  timestamp: string
  sources?: string[]
  processing_time?: number
}

export interface ChatSession {
  session_id: string
  user_id?: string
  created_at: string
  last_activity: string
  message_count: number
} 