'use client'

/**
 * Floating AI Chatbot Widget
 * Modern floating chat interface integrated into dashboard
 * Author: Sharmeen Asif
 */

import { useState, useEffect, useRef } from 'react'
import { MessageCircle, X, Send, Bot, User, Sparkles, Loader2, Mic, MicOff, RotateCcw, Volume2 } from 'lucide-react'
import { getStoredToken } from '@/lib/api-client'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ChatbotStatus {
  available: boolean
  message: string
  provider?: string
  instructions?: string
}

export default function FloatingChatbot() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hi! 👋 I'm your AI task assistant. I support English & Urdu (اردو)!\n\n🎤 Use voice input by clicking the microphone button.\n💬 Type or speak naturally, and I'll help manage your tasks.\n\nTry: 'Show all tasks' or 'میرے سارے ٹاسک دکھائیں'",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [chatbotStatus, setChatbotStatus] = useState<ChatbotStatus | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const recognitionRef = useRef<any>(null)
  const speechSynthRef = useRef<SpeechSynthesisUtterance | null>(null)

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  // Check chatbot status
  useEffect(() => {
    checkChatbotStatus()
  }, [])

  // Auto-scroll to bottom
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isOpen])

  // Focus input when opened, stop speech when closed
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100)
    } else {
      stopSpeaking()
    }
  }, [isOpen])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopSpeaking()
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
    }
  }, [])

  const checkChatbotStatus = async () => {
    try {
      const token = getStoredToken()
      const response = await fetch(`${apiUrl}/api/chatbot/status`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      })

      if (response.ok) {
        const status = await response.json()
        setChatbotStatus(status)
      }
    } catch (error) {
      console.error('Failed to check chatbot status:', error)
    }
  }

  // Initialize speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition

      if (SpeechRecognition) {
        const recognition = new SpeechRecognition()
        recognition.continuous = false
        recognition.interimResults = false

        // Support both Urdu and English
        recognition.lang = 'en-US' // Default to English, can be changed

        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript
          setInput(transcript)
          setIsRecording(false)
        }

        recognition.onerror = (event: any) => {
          console.error('Speech recognition error:', event.error)
          setIsRecording(false)

          // Handle specific errors
          if (event.error === 'no-speech') {
            // User didn't speak - this is normal, just ignore it
            console.log('No speech detected, mic stopped')
          } else if (event.error === 'audio-capture') {
            alert('Microphone not found. Please check your microphone settings.')
          } else if (event.error === 'not-allowed') {
            alert('Microphone permission denied. Please allow microphone access in your browser settings.')
          }
        }

        recognition.onend = () => {
          setIsRecording(false)
        }

        recognitionRef.current = recognition
      }
    }
  }, [])

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert('Voice recognition is not supported in your browser. Please try Chrome or Edge.')
      return
    }

    if (isRecording) {
      recognitionRef.current.stop()
      setIsRecording(false)
    } else {
      // Detect if input might be Urdu (right-to-left text)
      const hasUrduText = input && /[\u0600-\u06FF]/.test(input)

      if (hasUrduText) {
        recognitionRef.current.lang = 'ur-PK' // Urdu (Pakistan)
      } else {
        recognitionRef.current.lang = 'en-US' // English
      }

      recognitionRef.current.start()
      setIsRecording(true)
    }
  }

  // Text-to-speech function with realistic voice
  const speakText = (text: string) => {
    if (!window.speechSynthesis) {
      console.log('Text-to-speech not supported')
      return
    }

    // Cancel any ongoing speech
    window.speechSynthesis.cancel()

    const utterance = new SpeechSynthesisUtterance(text)

    // Detect language for proper pronunciation
    const hasUrduText = /[\u0600-\u06FF]/.test(text)
    utterance.lang = hasUrduText ? 'ur-PK' : 'en-US'

    // Try to get the most realistic voice available
    const voices = window.speechSynthesis.getVoices()

    if (hasUrduText) {
      // Find best Urdu voice
      const urduVoice = voices.find(v => v.lang.includes('ur')) ||
                        voices.find(v => v.lang.includes('hi')) // Hindi as fallback
      if (urduVoice) utterance.voice = urduVoice
    } else {
      // Find best English voice - prefer female voices like Sara, Samantha, etc.
      const preferredVoices = ['Google US English', 'Microsoft Zira', 'Samantha', 'Sara', 'Karen', 'Victoria']
      const bestVoice = voices.find(v =>
        v.lang.includes('en-US') && preferredVoices.some(name => v.name.includes(name))
      ) || voices.find(v => v.lang.includes('en-US') && v.name.includes('Female')) ||
         voices.find(v => v.lang.includes('en-US'))

      if (bestVoice) utterance.voice = bestVoice
    }

    utterance.rate = 0.95 // Natural speaking pace
    utterance.pitch = 1.05 // Slightly higher pitch for friendliness
    utterance.volume = 1.0 // Full volume

    utterance.onstart = () => setIsSpeaking(true)
    utterance.onend = () => setIsSpeaking(false)
    utterance.onerror = () => setIsSpeaking(false)

    speechSynthRef.current = utterance
    window.speechSynthesis.speak(utterance)
  }

  // Stop speaking
  const stopSpeaking = () => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel()
      setIsSpeaking(false)
    }
  }

  // Reset chat
  const resetChat = () => {
    if (confirm('Clear all messages and start fresh?')) {
      setMessages([
        {
          role: 'assistant',
          content: "Hi! 👋 I'm your AI task assistant. I support English & Urdu (اردو)!\n\n🎤 Use voice input by clicking the microphone button.\n💬 Type or speak naturally, and I'll help manage your tasks.\n\nTry: 'Show all tasks' or 'میرے سارے ٹاسک دکھائیں'",
          timestamp: new Date(),
        },
      ])
      setInput('')
      stopSpeaking()
    }
  }

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    const wasUsingVoice = isRecording // Track if user was using voice input

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const token = getStoredToken()
      const response = await fetch(`${apiUrl}/api/chatbot/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ message: input }),
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`)
      }

      const data = await response.json()

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])

      // If user was using voice input, speak the response
      if (wasUsingVoice) {
        speakText(data.response)
      }

      // Emit event to refresh task list if tasks were modified
      // Check if the message contains task operation keywords
      const taskOperationKeywords = ['added', 'created', 'updated', 'marked', 'completed', 'deleted', 'removed']
      const messageText = data.response.toLowerCase()
      const isTaskOperation = taskOperationKeywords.some(keyword => messageText.includes(keyword))

      if (isTaskOperation) {
        // Dispatch custom event to notify dashboard
        window.dispatchEvent(new CustomEvent('taskModified', { detail: { source: 'chatbot' } }))
      }
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${
          error instanceof Error ? error.message : 'Unknown error'
        }`,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      setTimeout(() => inputRef.current?.focus(), 100)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage()
  }

  const quickCommands = [
    { label: 'Show all tasks', command: 'Show me all my tasks' },
    { label: 'Active tasks', command: 'Show me my active tasks' },
    { label: 'Add task', command: 'Add buy groceries to my list' },
    { label: 'سب ٹاسک دکھائیں', command: 'میرے سارے ٹاسک دکھائیں' },
    { label: 'ٹاسک شامل کریں', command: 'گروسری خریدنا ٹاسک میں شامل کریں' },
  ]

  return (
    <>
      {/* Chat Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full shadow-2xl hover:shadow-indigo-500/50 transition-all duration-300 hover:scale-110 flex items-center justify-center z-50 group"
      >
        {isOpen ? (
          <X className="w-7 h-7 text-white" />
        ) : (
          <div className="relative">
            <MessageCircle className="w-7 h-7 text-white" />
            {chatbotStatus?.available && (
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white animate-pulse"></span>
            )}
          </div>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-96 h-[600px] bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 flex flex-col z-50 animate-in slide-in-from-bottom-8 fade-in duration-300">
          {/* Header */}
          <div className="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-t-3xl p-5 text-white">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
                  <Bot className="w-7 h-7 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-lg flex items-center gap-2">
                    AI Assistant
                    <Sparkles className="w-4 h-4" />
                  </h3>
                  <p className="text-xs text-indigo-100">
                    {chatbotStatus?.available
                      ? `Powered by ${chatbotStatus.provider === 'openai' ? 'GPT-4' : 'AI'}`
                      : 'Not configured'}
                  </p>
                </div>
              </div>
              <button
                onClick={resetChat}
                className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                title="Reset chat"
              >
                <RotateCcw className="w-5 h-5 text-white" />
              </button>
            </div>

            {/* Status Warning */}
            {chatbotStatus && !chatbotStatus.available && (
              <div className="mt-3 p-2 bg-yellow-500/20 backdrop-blur-sm rounded-lg text-xs">
                <p className="font-medium">⚠️ {chatbotStatus.message}</p>
                {chatbotStatus.instructions && (
                  <p className="mt-1 text-indigo-100">{chatbotStatus.instructions}</p>
                )}
              </div>
            )}
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gradient-to-br from-gray-50 to-indigo-50/30">
            {messages.map((message, idx) => (
              <div
                key={idx}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl p-3 shadow-md ${
                    message.role === 'user'
                      ? 'bg-gradient-to-br from-indigo-600 to-purple-600 text-white'
                      : 'bg-white text-gray-800'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-white/20 flex items-center justify-center">
                      {message.role === 'user' ? (
                        <User className="w-4 h-4" />
                      ) : (
                        <Bot className="w-4 h-4 text-indigo-600" />
                      )}
                    </div>
                    <div className="flex-1">
                      <div
                        className="text-sm whitespace-pre-wrap break-words leading-relaxed"
                        style={{ direction: /[\u0600-\u06FF]/.test(message.content) ? 'rtl' : 'ltr' }}
                      >
                        {message.content}
                      </div>
                      <div
                        className={`flex items-center justify-between text-xs mt-1 ${
                          message.role === 'user' ? 'text-indigo-200' : 'text-gray-400'
                        }`}
                      >
                        <span>
                          {message.timestamp.toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit',
                          })}
                        </span>
                        {message.role === 'assistant' && (
                          <button
                            onClick={() => speakText(message.content)}
                            className="p-1 hover:bg-indigo-100 rounded transition-colors"
                            title="Listen to this message"
                          >
                            <Volume2 className="w-3 h-3 text-indigo-600" />
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Typing Indicator */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white rounded-2xl p-3 shadow-md">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-indigo-100 flex items-center justify-center">
                      <Bot className="w-4 h-4 text-indigo-600" />
                    </div>
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"
                        style={{ animationDelay: '0.1s' }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"
                        style={{ animationDelay: '0.2s' }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Quick Commands */}
          <div className="px-4 py-2 bg-white/80 border-t border-gray-200">
            <div className="flex gap-2 overflow-x-auto pb-1">
              {quickCommands.map((cmd, idx) => (
                <button
                  key={idx}
                  onClick={() => setInput(cmd.command)}
                  disabled={isLoading}
                  className="flex-shrink-0 px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 rounded-lg text-xs font-medium transition-colors disabled:opacity-50"
                >
                  {cmd.label}
                </button>
              ))}
            </div>
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="p-4 bg-white rounded-b-3xl border-t border-gray-200">
            <div className="flex gap-2">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isLoading || isRecording}
                className="flex-1 px-4 py-2.5 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-indigo-500 disabled:opacity-50 text-sm"
                placeholder={isRecording ? "Listening..." : "Ask me anything or click mic..."}
                style={{ direction: /[\u0600-\u06FF]/.test(input) ? 'rtl' : 'ltr' }}
              />
              <button
                type="button"
                onClick={toggleVoiceInput}
                disabled={isLoading}
                className={`px-4 py-2.5 ${
                  isRecording
                    ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                    : 'bg-gray-100 hover:bg-gray-200'
                } rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl`}
                title="Voice input (supports English and Urdu)"
              >
                {isRecording ? (
                  <MicOff className="w-5 h-5 text-white" />
                ) : (
                  <Mic className="w-5 h-5 text-gray-600" />
                )}
              </button>
              <button
                type="submit"
                disabled={isLoading || !input.trim() || isRecording}
                className="px-4 py-2.5 bg-gradient-to-br from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              🎤 Voice input • 🔊 Bot speaks back • 🔄 Reset chat button
            </p>
          </form>
        </div>
      )}
    </>
  )
}
