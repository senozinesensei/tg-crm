import { Chat } from '../../store/chatStore'

interface Props {
  chat: Chat
  isActive: boolean
  onClick: () => void
}

function formatTime(dateStr: string | null): string {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } else if (days === 1) {
    return 'Yesterday'
  } else if (days < 7) {
    return date.toLocaleDateString([], { weekday: 'short' })
  }
  return date.toLocaleDateString([], { month: 'short', day: 'numeric' })
}

function getInitials(contact: Chat['contact']): string {
  if (!contact) return '?'
  const first = contact.first_name?.[0] || ''
  const last = contact.last_name?.[0] || ''
  return (first + last).toUpperCase() || '?'
}

export default function ChatListItem({ chat, isActive, onClick }: Props) {
  const contact = chat.contact
  const name = contact
    ? [contact.first_name, contact.last_name].filter(Boolean).join(' ') || contact.username || 'Unknown'
    : 'Unknown'

  return (
    <div
      onClick={onClick}
      className={`flex items-center gap-3 px-4 py-3 cursor-pointer transition-colors border-b border-gray-100 dark:border-gray-700 ${
        isActive
          ? 'bg-blue-50 dark:bg-blue-900/20'
          : 'hover:bg-gray-50 dark:hover:bg-gray-700/50'
      }`}
    >
      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-medium">
        {contact?.avatar_url ? (
          <img src={contact.avatar_url} alt="" className="w-10 h-10 rounded-full object-cover" />
        ) : (
          getInitials(contact)
        )}
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-900 dark:text-white truncate">
            {name}
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-400 flex-shrink-0 ml-2">
            {formatTime(chat.last_message_at)}
          </span>
        </div>
        <div className="flex items-center justify-between mt-0.5">
          <span className="text-xs text-gray-500 dark:text-gray-400 truncate">
            {chat.last_message_text || 'No messages'}
          </span>
          {chat.unread_count > 0 && (
            <span className="flex-shrink-0 ml-2 inline-flex items-center justify-center w-5 h-5 text-xs font-medium text-white bg-blue-600 rounded-full">
              {chat.unread_count}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
