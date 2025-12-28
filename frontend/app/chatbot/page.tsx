"use client";

/**
 * AI Chatbot Interface Page
 * Phase III Integration - Natural language task management
 * Author: Sharmeen Asif
 */

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface ChatbotStatus {
  available: boolean;
  message: string;
  instructions?: string;
}

export default function ChatbotPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello! I'm your AI task assistant. I can help you manage your todos using natural language. Try asking me to 'show all tasks' or 'add a new task'.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [chatbotStatus, setChatbotStatus] = useState<ChatbotStatus | null>(
    null
  );
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  // Check chatbot status on mount
  useEffect(() => {
    checkChatbotStatus();
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const checkChatbotStatus = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/chatbot/status`, {
        credentials: "include",
      });

      if (response.ok) {
        const status = await response.json();
        setChatbotStatus(status);
      }
    } catch (error) {
      console.error("Failed to check chatbot status:", error);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(`${apiUrl}/api/chatbot/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error("Please sign in again");
        }
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        role: "assistant",
        content: `Error: ${
          error instanceof Error ? error.message : "Unknown error"
        }`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);

      if (error instanceof Error && error.message.includes("sign in")) {
        setTimeout(() => router.push("/auth/signin"), 2000);
      }
    } finally {
      setIsLoading(false);
      // Restore focus to input field after message is sent
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage();
  };

  const handleQuickCommand = (command: string) => {
    setInput(command);
    // Focus input field after setting quick command
    setTimeout(() => inputRef.current?.focus(), 0);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                🤖 AI Task Assistant
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Phase III: Natural Language Task Management
              </p>
              {chatbotStatus && !chatbotStatus.available && (
                <div className="mt-2 p-2 bg-yellow-100 border border-yellow-300 rounded text-sm text-yellow-800">
                  ⚠️ {chatbotStatus.message}
                  {chatbotStatus.instructions && (
                    <div className="mt-1 text-xs">{chatbotStatus.instructions}</div>
                  )}
                </div>
              )}
            </div>
            <button
              onClick={() => router.push("/tasks")}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors"
            >
              Back to Tasks
            </button>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="bg-white rounded-lg shadow-md p-4 min-h-[500px] max-h-[600px] overflow-y-auto mb-4">
          <div className="space-y-4">
            {messages.map((message, idx) => (
              <div
                key={idx}
                className={`flex ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    message.role === "user"
                      ? "bg-indigo-600 text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <div className="flex-shrink-0 text-lg">
                      {message.role === "user" ? "👤" : "🤖"}
                    </div>
                    <div className="flex-1">
                      <div className="whitespace-pre-wrap break-words">
                        {message.content}
                      </div>
                      <div
                        className={`text-xs mt-1 ${
                          message.role === "user"
                            ? "text-indigo-200"
                            : "text-gray-500"
                        }`}
                      >
                        {message.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-lg p-3">
                  <div className="flex items-center gap-2">
                    <div className="text-lg">🤖</div>
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Quick Commands */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-4">
          <p className="text-sm text-gray-600 mb-2">Quick Commands:</p>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => handleQuickCommand("Show me all my tasks")}
              disabled={isLoading}
              className="px-3 py-1 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 rounded text-sm transition-colors disabled:opacity-50"
            >
              Show all tasks
            </button>
            <button
              onClick={() => handleQuickCommand("Show me my active tasks")}
              disabled={isLoading}
              className="px-3 py-1 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 rounded text-sm transition-colors disabled:opacity-50"
            >
              Active tasks
            </button>
            <button
              onClick={() => handleQuickCommand("Add buy groceries to my list")}
              disabled={isLoading}
              className="px-3 py-1 bg-green-100 hover:bg-green-200 text-green-700 rounded text-sm transition-colors disabled:opacity-50"
            >
              Add task example
            </button>
            <button
              onClick={() => handleQuickCommand("What can you help me with?")}
              disabled={isLoading}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded text-sm transition-colors disabled:opacity-50"
            >
              Help
            </button>
          </div>
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-4">
          <div className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
              placeholder="Type your message... (e.g., 'show all tasks', 'add buy milk')"
              autoFocus
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "..." : "Send"}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            💡 Try natural language: "Show my incomplete tasks", "Create a task
            for buying milk", "Mark task 1 as done"
          </p>
        </form>

        {/* Info */}
        <div className="mt-4 text-center text-sm text-gray-600">
          <p>
            Powered by Claude Sonnet 4 AI with MCP (Model Context Protocol)
          </p>
          <p className="mt-1">
            Original CLI: <code className="bg-gray-100 px-2 py-1 rounded">cd chatbot && uv run chatbot</code>
          </p>
        </div>
      </div>
    </div>
  );
}
