'use client'

import { useEffect, useRef, useState } from 'react'

interface WebSocketMessage {
  type: string
  data: any
}

export function useWebSocket(url?: string) {
  const ws = useRef<WebSocket | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null)

  useEffect(() => {
    const wsUrl = url || `${process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'}/ws`
    
    // For demo purposes, simulate WebSocket connection
    // In production, you would connect to your actual WebSocket server
    const simulateConnection = () => {
      setIsConnected(true)
      
      // Simulate receiving messages every 10 seconds
      const interval = setInterval(() => {
        const mockMessages = [
          {
            type: 'threat_detected',
            data: {
              email: 'suspicious@example.com',
              threat_level: Math.floor(Math.random() * 40) + 60, // 60-100%
              threat_type: ['Phishing', 'Malware', 'Social Engineering'][Math.floor(Math.random() * 3)],
              timestamp: new Date().toISOString(),
            }
          },
          {
            type: 'email_processed',
            data: {
              email: 'newsletter@legitimate.com',
              threat_level: Math.floor(Math.random() * 20), // 0-20%
              status: 'delivered',
              timestamp: new Date().toISOString(),
            }
          },
          {
            type: 'system_update',
            data: {
              message: 'ML models updated with latest threat patterns',
              timestamp: new Date().toISOString(),
            }
          }
        ]
        
        const randomMessage = mockMessages[Math.floor(Math.random() * mockMessages.length)]
        setLastMessage(randomMessage)
      }, 10000) // Every 10 seconds

      return () => {
        clearInterval(interval)
        setIsConnected(false)
      }
    }

    const cleanup = simulateConnection()

    return cleanup
  }, [url])

  const sendMessage = (message: WebSocketMessage) => {
    // In a real implementation, you would send the message through the WebSocket
    console.log('Sending message:', message)
  }

  return {
    isConnected,
    lastMessage,
    sendMessage,
  }
} 