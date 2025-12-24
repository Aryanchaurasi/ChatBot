import React from 'react'
import { MessageBubble } from './MessageBubble'
import { ChatInput } from './ChatInput'
import { useChat } from '../hooks/useChat'
import { Loader2, Brain } from 'lucide-react'

export function ChatWindow() {
  const { messages, isLoading, sendMessage } = useChat()

  const handleSendMessage = async (query: string) => {
    try {
      await sendMessage(query)
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b p-4">
        <div className="flex items-center gap-3">
          <Brain className="text-blue-600" size={32} />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">DualLLM TruthBot</h1>
            <p className="text-sm text-gray-600">Gemini 🦒 vs OpenAI 🔥 with AI Judge ⚖️</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <div className="text-center">
              <Brain size={64} className="mx-auto mb-4 text-gray-300" />
              <h2 className="text-xl font-semibold mb-2">Welcome to DualLLM TruthBot</h2>
              <p className="text-sm">Ask any question and get the best answer from Gemini and OpenAI!</p>
            </div>
          </div>
        ) : (
          <div className="space-y-0">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
          </div>
        )}
        
        {isLoading && (
          <div className="flex items-center justify-center p-8">
            <div className="flex items-center gap-3 text-blue-600">
              <Loader2 className="animate-spin" size={24} />
              <span>Consulting both LLMs and judge...</span>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <ChatInput onSend={handleSendMessage} disabled={isLoading} />
    </div>
  )
}