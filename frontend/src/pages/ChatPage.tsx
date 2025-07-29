import React, { useState, useEffect, useRef } from 'react'
import { Trash2, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useToast } from '@/hooks/use-toast'
import ChatMessage from '@/components/ChatMessage'
import ChatInput from '@/components/ChatInput'
import { chatApi } from '@/services/api'
import { ChatMessage as ChatMessageType, ChatRequest } from '@/types/chat'
import { generateSessionId } from '@/lib/utils'

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessageType[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string>('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  useEffect(() => {
    // Generate a new session ID on component mount
    setSessionId(generateSessionId())
  }, [])

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return

    const userMessage: ChatMessageType = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
      session_id: sessionId
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const request: ChatRequest = {
        message: content,
        session_id: sessionId,
        use_rag: true
      }

      const response = await chatApi.sendMessage(request)
      
      const assistantMessage: ChatMessageType = {
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp,
        session_id: response.session_id
      }

      setMessages(prev => [...prev, assistantMessage])
      
      // Show processing time if available
      if (response.processing_time) {
        toast({
          title: "Response Generated",
          description: `Processed in ${response.processing_time.toFixed(2)}s`,
        })
      }
    } catch (error) {
      console.error('Error sending message:', error)
      toast({
        title: "Error",
        description: "Failed to send message. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleClearChat = () => {
    setMessages([])
    setSessionId(generateSessionId())
    toast({
      title: "Chat Cleared",
      description: "Conversation history has been cleared.",
    })
  }

  const handleNewChat = () => {
    setMessages([])
    setSessionId(generateSessionId())
    toast({
      title: "New Chat",
      description: "Started a new conversation.",
    })
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      {/* Chat Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <h2 className="text-lg font-semibold">Chat with AI Assistant</h2>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleNewChat}
            className="flex items-center gap-2"
          >
            <RefreshCw className="h-4 w-4" />
            New Chat
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleClearChat}
            className="flex items-center gap-2"
          >
            <Trash2 className="h-4 w-4" />
            Clear
          </Button>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-muted-foreground">
              <h3 className="text-lg font-medium mb-2">Welcome to AI Chatbot</h3>
              <p className="text-sm">
                Start a conversation by typing a message below.
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Chat Input */}
      <ChatInput
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        disabled={messages.length === 0 && isLoading}
      />
    </div>
  )
}

export default ChatPage 