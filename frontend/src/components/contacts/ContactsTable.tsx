import { Contact } from '../../store/chatStore'

interface Props {
  contacts: Contact[]
}

export default function ContactsTable({ contacts }: Props) {
  if (contacts.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500 dark:text-gray-400">
        No contacts found
      </div>
    )
  }

  return (
    <table className="w-full text-sm text-left">
      <thead className="text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-700/50">
        <tr>
          <th className="px-6 py-3">Contact</th>
          <th className="px-6 py-3">Username</th>
          <th className="px-6 py-3">Telegram ID</th>
          <th className="px-6 py-3">Last Activity</th>
        </tr>
      </thead>
      <tbody>
        {contacts.map((contact) => {
          const name = [contact.first_name, contact.last_name].filter(Boolean).join(' ') || 'Unknown'
          const initials = (contact.first_name?.[0] || '') + (contact.last_name?.[0] || '') || '?'

          return (
            <tr
              key={contact.id}
              className="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/30"
            >
              <td className="px-6 py-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-medium flex-shrink-0">
                    {contact.avatar_url ? (
                      <img src={contact.avatar_url} alt="" className="w-8 h-8 rounded-full object-cover" />
                    ) : (
                      initials.toUpperCase()
                    )}
                  </div>
                  <span className="font-medium text-gray-900 dark:text-white">{name}</span>
                </div>
              </td>
              <td className="px-6 py-4 text-gray-500 dark:text-gray-400">
                {contact.username ? `@${contact.username}` : '-'}
              </td>
              <td className="px-6 py-4 text-gray-500 dark:text-gray-400">
                {contact.telegram_id}
              </td>
              <td className="px-6 py-4 text-gray-500 dark:text-gray-400">
                {new Date(contact.last_activity_at).toLocaleString([], {
                  month: 'short',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}
