import { Contact } from '../../store/chatStore'

interface Props {
  contact: Contact
}

export default function ContactPanel({ contact }: Props) {
  const name = [contact.first_name, contact.last_name].filter(Boolean).join(' ') || 'Unknown'
  const initials = (contact.first_name?.[0] || '') + (contact.last_name?.[0] || '') || '?'

  return (
    <div className="w-72 h-full bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 overflow-y-auto">
      <div className="p-6 text-center border-b border-gray-200 dark:border-gray-700">
        <div className="w-20 h-20 mx-auto rounded-full bg-blue-500 flex items-center justify-center text-white text-2xl font-medium">
          {contact.avatar_url ? (
            <img src={contact.avatar_url} alt="" className="w-20 h-20 rounded-full object-cover" />
          ) : (
            initials.toUpperCase()
          )}
        </div>
        <h3 className="mt-3 text-lg font-medium text-gray-900 dark:text-white">{name}</h3>
        {contact.username && (
          <p className="text-sm text-gray-500 dark:text-gray-400">@{contact.username}</p>
        )}
      </div>

      <div className="p-6 space-y-4">
        <div>
          <label className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            Telegram ID
          </label>
          <p className="text-sm text-gray-900 dark:text-white mt-1">{contact.telegram_id}</p>
        </div>

        {contact.username && (
          <div>
            <label className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
              Username
            </label>
            <p className="text-sm text-gray-900 dark:text-white mt-1">@{contact.username}</p>
          </div>
        )}

        <div>
          <label className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            First Seen
          </label>
          <p className="text-sm text-gray-900 dark:text-white mt-1">
            {new Date(contact.created_at).toLocaleDateString([], {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </p>
        </div>

        <div>
          <label className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
            Last Activity
          </label>
          <p className="text-sm text-gray-900 dark:text-white mt-1">
            {new Date(contact.last_activity_at).toLocaleString([], {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        </div>
      </div>
    </div>
  )
}
