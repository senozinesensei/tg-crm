import { create } from 'zustand'

export interface Contact {
  id: string
  telegram_id: number
  first_name: string | null
  last_name: string | null
  username: string | null
  avatar_url: string | null
  created_at: string
  last_activity_at: string
}

export interface Chat {
  id: string
  contact_id: string
  last_message_text: string | null
  last_message_at: string | null
  unread_count: number
  created_at: string
  contact: Contact | null
}

export interface Message {
  id: string
  chat_id: string
  direction: 'incoming' | 'outgoing'
  text: string
  telegram_message_id: number | null
  sent_by_user_id: string | null
  created_at: string
}

interface ChatState {
  chats: Chat[]
  activeChat: Chat | null
  messages: Message[]
  setChats: (chats: Chat[]) => void
  setActiveChat: (chat: Chat | null) => void
  setMessages: (messages: Message[]) => void
  addMessage: (message: Message) => void
  addChat: (chat: Chat) => void
  updateChat: (chatId: string, data: Partial<Chat>) => void
}

export const useChatStore = create<ChatState>((set, get) => ({
  chats: [],
  activeChat: null,
  messages: [],
  setChats: (chats) => set({ chats }),
  setActiveChat: (chat) => set({ activeChat: chat }),
  setMessages: (messages) => set({ messages }),
  addMessage: (message) => {
    const state = get()
    if (state.activeChat && message.chat_id === state.activeChat.id) {
      set({ messages: [...state.messages, message] })
    }
  },
  addChat: (chat) => {
    set({ chats: [chat, ...get().chats] })
  },
  updateChat: (chatId, data) => {
    set({
      chats: get().chats.map((c) =>
        c.id === chatId ? { ...c, ...data } : c
      ).sort((a, b) => {
        const aTime = a.last_message_at ? new Date(a.last_message_at).getTime() : 0
        const bTime = b.last_message_at ? new Date(b.last_message_at).getTime() : 0
        return bTime - aTime
      }),
    })
  },
}))
