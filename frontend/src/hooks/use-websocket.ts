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
    
    // WebSocket connection logic
    const connectWebSocket = () => {
      try {
        ws.current = new WebSocket(wsUrl)
        
        ws.current.onopen = () => {
          setIsConnected(true)
        }
        
        ws.current.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data)
            setLastMessage(message)
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error)
          }
        }
        
        ws.current.onclose = () => {
          setIsConnected(false)
        }
        
        ws.current.onerror = (error) => {
          console.error('WebSocket error:', error)
          setIsConnected(false)
        }
        
        return () => {
          if (ws.current) {
            ws.current.close()
          }
        }
      } catch (error) {
        console.error('Failed to create WebSocket connection:', error)
        return () => {}
      }
    }

    const cleanup = connectWebSocket()

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