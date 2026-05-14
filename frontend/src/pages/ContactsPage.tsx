import { useEffect, useState } from 'react'
import { getContacts } from '../api/contacts'
import { Contact } from '../store/chatStore'
import ContactsTable from '../components/contacts/ContactsTable'

export default function ContactsPage() {
  const [contacts, setContacts] = useState<Contact[]>([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadContacts()
  }, [])

  const loadContacts = async (searchQuery = '') => {
    setLoading(true)
    try {
      const data = await getContacts(searchQuery)
      setContacts(data)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    loadContacts(search)
  }

  return (
    <div className="h-full flex flex-col bg-white dark:bg-gray-800">
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Contacts</h2>
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {contacts.length} contacts
          </span>
        </div>
        <form onSubmit={handleSearch} className="mt-4">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by name or username..."
            className="w-full max-w-md px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500 text-sm"
          />
        </form>
      </div>

      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <ContactsTable contacts={contacts} />
        )}
      </div>
    </div>
  )
}
