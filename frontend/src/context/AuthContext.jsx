import { createContext, useContext, useEffect, useState } from 'react'
import { jwtDecode } from '../utils/jwt'
import { getAccessToken, setAccessToken, setOnUnauthorized } from '../api/client'
import { logout as logoutApi } from '../api/auth'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = getAccessToken()
    if (token) {
      try {
        setUser(jwtDecode(token))
      } catch {
        setAccessToken(null)
      }
    }
    setLoading(false)

    setOnUnauthorized(() => {
      setUser(null)
    })
  }, [])

  const login = (accessToken) => {
    setAccessToken(accessToken)
    setUser(jwtDecode(accessToken))
  }

  const logout = async () => {
    await logoutApi()
    setUser(null)
  }

  const isAdmin = user?.role === 1

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAdmin }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
