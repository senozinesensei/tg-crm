import { Message } from '../../store/chatStore'

interface Props {
  message: Message
}

export default function MessageBubble({ message }: Props) {
  const isOutgoing = message.direction === 'outgoing'
  const time = new Date(message.created_at).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  })

  return (
    <div className={`flex ${isOutgoing ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[70%] px-4 py-2 rounded-2xl ${
          isOutgoing
            ? 'bg-blue-600 text-white rounded-br-md'
            : 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-bl-md shadow-sm'
        }`}
      >
        <p className="text-sm whitespace-pre-wrap break-words">{message.text}</p>
        <p
          className={`text-xs mt-1 ${
            isOutgoing ? 'text-blue-200' : 'text-gray-400 dark:text-gray-500'
          }`}
        >
          {time}
        </p>
      </div>
    </div>
  )
}
