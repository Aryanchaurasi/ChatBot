import React from 'react'
import { Copy, Trophy, Scale } from 'lucide-react'
import { ChatMessage } from '../hooks/useChat'

interface MessageBubbleProps {
  message: ChatMessage
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  const getWinnerIcon = (winner: string) => {
    if (winner === 'A') return '🦒' // Gemini
    if (winner === 'B') return '🔥' // OpenAI
    return '🤝' // Tie
  }

  const getLoserIcon = (winner: string) => {
    if (winner === 'A') return '🔥' // OpenAI lost
    if (winner === 'B') return '🦒' // Gemini lost
    return '🤝' // Tie
  }

  return (
    <div className="space-y-4 p-4 border-b">
      {/* User Query */}
      <div className="bg-blue-50 p-3 rounded-lg">
        <p className="font-medium text-blue-900">Query: {message.query}</p>
      </div>

      {/* Winner Section */}
      <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
        <div className="flex items-center gap-2 mb-2">
          <Trophy className="text-green-600" size={20} />
          <span className="font-bold text-green-800">
            BEST ({Math.round(message.confidence * 100)}% confidence)
          </span>
          <span className="text-2xl">{getWinnerIcon(message.winner)}</span>
          <button
            onClick={() => copyToClipboard(message.winner_response)}
            className="ml-auto p-1 hover:bg-green-100 rounded"
          >
            <Copy size={16} />
          </button>
        </div>
        <p className="text-gray-800">{message.winner_response}</p>
      </div>

      {/* Comparison Section */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <h4 className="font-bold mb-3 flex items-center gap-2">
          <span>COMPARISON</span>
        </h4>
        
        <div className="grid md:grid-cols-2 gap-4 mb-4">
          {/* Gemini Response */}
          <div className="bg-white p-3 rounded border">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-2xl">🦒</span>
              <span className="font-medium">Gemini</span>
              <button
                onClick={() => copyToClipboard(message.gemini_response)}
                className="ml-auto p-1 hover:bg-gray-100 rounded"
              >
                <Copy size={14} />
              </button>
            </div>
            <p className="text-sm text-gray-700 line-clamp-3">{message.gemini_response}</p>
          </div>

          {/* OpenAI Response */}
          <div className="bg-white p-3 rounded border">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-2xl">🔥</span>
              <span className="font-medium">OpenAI</span>
              <button
                onClick={() => copyToClipboard(message.openai_response)}
                className="ml-auto p-1 hover:bg-gray-100 rounded"
              >
                <Copy size={14} />
              </button>
            </div>
            <p className="text-sm text-gray-700 line-clamp-3">{message.openai_response}</p>
          </div>
        </div>

        {/* Judge Reasoning */}
        <div className="bg-yellow-50 p-3 rounded border-l-4 border-yellow-400">
          <div className="flex items-center gap-2 mb-1">
            <Scale className="text-yellow-600" size={16} />
            <span className="font-medium text-yellow-800">Judge Reasoning:</span>
          </div>
          <p className="text-sm text-yellow-900">{message.judge_reason}</p>
        </div>
      </div>
    </div>
  )
}