import { useState, useCallback } from 'react'
import { sendMessage, ChatResponse } from '../lib/utils'

export interface ChatMessage extends ChatResponse {
  id: string
  query: string
  timestamp: Date
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState<number | undefined>()

  const sendChatMessage = useCallback(async (query: string) => {
    setIsLoading(true)
    try {
      const response = await sendMessage(query, sessionId)
      
      const newMessage: ChatMessage = {
        id: Date.now().toString(),
        query,
        timestamp: new Date(),
        ...response
      }
      
      setMessages(prev => [...prev, newMessage])
      setSessionId(response.session_id)
      
      return newMessage
    } catch (error) {
      console.error('Failed to send message:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [sessionId])

  return {
    messages,
    isLoading,
    sendMessage: sendChatMessage
  }
}