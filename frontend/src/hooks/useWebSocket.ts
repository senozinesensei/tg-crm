import { useEffect, useRef } from 'react'
import { useAuthStore } from '../store/authStore'
import { useChatStore } from '../store/chatStore'

export function useWebSocket() {
  const token = useAuthStore((s) => s.token)
  const addMessage = useChatStore((s) => s.addMessage)
  const addChat = useChatStore((s) => s.addChat)
  const updateChat = useChatStore((s) => s.updateChat)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeout = useRef<number | null>(null)
  const retryCount = useRef(0)

  useEffect(() => {
    if (!token) return

    function connect() {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const host = window.location.host
      const ws = new WebSocket(`${protocol}//${host}/ws?token=${token}`)
      wsRef.current = ws

      ws.onopen = () => {
        retryCount.current = 0
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          switch (data.type) {
            case 'new_message':
              addMessage(data.data)
              break
            case 'new_chat':
              addChat(data.data)
              break
            case 'chat_updated':
              updateChat(data.data.chat_id, {
                last_message_text: data.data.last_message_text,
                last_message_at: data.data.last_message_at,
                unread_count: data.data.unread_count,
              })
              break
          }
        } catch (e) {
          console.error('WebSocket message parse error:', e)
        }
      }

      ws.onclose = () => {
        const delay = Math.min(1000 * 2 ** retryCount.current, 30000)
        retryCount.current++
        reconnectTimeout.current = window.setTimeout(connect, delay)
      }

      ws.onerror = () => {
        ws.close()
      }
    }

    connect()

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current)
      }
    }
  }, [token, addMessage, addChat, updateChat])
}
