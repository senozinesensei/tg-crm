import { Chat } from '../../store/chatStore'
import ChatListItem from './ChatListItem'

interface Props {
  chats: Chat[]
  activeChat: Chat | null
  onSelectChat: (chat: Chat) => void
}

export default function ChatList({ chats, activeChat, onSelectChat }: Props) {
  return (
    <div className="w-80 h-full flex flex-col border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Chats</h2>
      </div>
      <div className="flex-1 overflow-y-auto">
        {chats.length === 0 ? (
          <div className="p-4 text-center text-gray-500 dark:text-gray-400 text-sm">
            No chats yet. Waiting for messages...
          </div>
        ) : (
          chats.map((chat) => (
            <ChatListItem
              key={chat.id}
              chat={chat}
              isActive={activeChat?.id === chat.id}
              onClick={() => onSelectChat(chat)}
            />
          ))
        )}
      </div>
    </div>
  )
}
