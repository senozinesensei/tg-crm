import { useEffect } from 'react'
import { useAuthStore } from '../store/authStore'
import { getMe } from '../api/auth'

export function useAuth() {
  const { token, user, setAuth, logout } = useAuthStore()

  useEffect(() => {
    if (token && !user) {
      getMe()
        .then((userData) => setAuth(userData, token))
        .catch(() => logout())
    }
  }, [token, user, setAuth, logout])

  return { user, token, logout }
}
