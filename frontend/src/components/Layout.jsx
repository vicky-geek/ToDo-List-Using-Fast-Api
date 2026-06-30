import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Layout({ children }) {
  const { user, logout, isAdmin } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <h1 className="logo">ToDo</h1>
          <div className="header-right">
            <span className="user-badge">
              {user?.username}
              <span className="role-tag">{isAdmin ? 'Admin' : 'User'}</span>
            </span>
            <button type="button" className="btn btn-ghost" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </header>
      <main className="main">{children}</main>
    </div>
  )
}

export function AuthLayout({ title, subtitle, children, footer }) {
  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
        {children}
        {footer && <div className="auth-footer">{footer}</div>}
      </div>
    </div>
  )
}
