import { Outlet } from 'react-router-dom'
import Sidebar from '../components/layout/Sidebar'
import { useWebSocket } from '../hooks/useWebSocket'
import { useAuth } from '../hooks/useAuth'

export default function DashboardLayout() {
  useAuth()
  useWebSocket()

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-900">
      <Sidebar />
      <main className="flex-1 overflow-hidden">
        <Outlet />
      </main>
    </div>
  )
}
