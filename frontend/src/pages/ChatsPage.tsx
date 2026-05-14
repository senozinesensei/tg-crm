import { useEffect, useState } from 'react'
import { useChatStore } from '../store/chatStore'
import { getChats, getChatMessages, markChatRead } from '../api/chats'
import ChatList from '../components/chat/ChatList'
import MessageArea from '../components/chat/MessageArea'
import ContactPanel from '../components/chat/ContactPanel'

export default function ChatsPage() {
  const { chats, activeChat, setChats, setActiveChat, setMessages } = useChatStore()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getChats()
      .then(setChats)
      .finally(() => setLoading(false))
  }, [setChats])

  const handleSelectChat = async (chat: typeof activeChat) => {
    setActiveChat(chat)
    if (chat) {
      const messages = await getChatMessages(chat.id)
      setMessages(messages)
      if (chat.unread_count > 0) {
        await markChatRead(chat.id)
        useChatStore.getState().updateChat(chat.id, { unread_count: 0 })
      }
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="flex h-full">
      <ChatList
        chats={chats}
        activeChat={activeChat}
        onSelectChat={handleSelectChat}
      />
      <MessageArea />
      {activeChat?.contact && <ContactPanel contact={activeChat.contact} />}
    </div>
  )
}
