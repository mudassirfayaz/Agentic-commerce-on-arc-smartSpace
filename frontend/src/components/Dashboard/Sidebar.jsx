import { Link, useNavigate, useLocation } from 'react-router-dom'
import './Sidebar.css'

const Sidebar = () => {
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    navigate('/')
  }

  const isActive = (path) => {
    if (path === '/dashboard') {
      return location.pathname === '/dashboard'
    }
    return location.pathname === path
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">SmartSpace</div>
      </div>
      <nav className="sidebar-nav">
        <Link to="/dashboard" className={`nav-item ${isActive('/dashboard') ? 'active' : ''}`}>
          <span className="nav-icon">◉</span>
          <span className="nav-text">Dashboard</span>
        </Link>
        <Link to="/dashboard/projects" className={`nav-item ${isActive('/dashboard/projects') ? 'active' : ''}`}>
          <span className="nav-icon">◯</span>
          <span className="nav-text">Projects</span>
        </Link>
        <Link to="/dashboard/agents" className={`nav-item ${isActive('/dashboard/agents') ? 'active' : ''}`}>
          <span className="nav-icon">◯</span>
          <span className="nav-text">Agents</span>
        </Link>
        <Link to="/dashboard/usage" className={`nav-item ${isActive('/dashboard/usage') ? 'active' : ''}`}>
          <span className="nav-icon">◯</span>
          <span className="nav-text">Usage</span>
        </Link>
        <Link to="/dashboard/billing" className={`nav-item ${isActive('/dashboard/billing') ? 'active' : ''}`}>
          <span className="nav-icon">◯</span>
          <span className="nav-text">Billing</span>
        </Link>
      </nav>
      <div className="sidebar-footer">
        <button onClick={handleLogout} className="btn btn-outline btn-block">
          Logout
        </button>
      </div>
    </aside>
  )
}

export default Sidebar

