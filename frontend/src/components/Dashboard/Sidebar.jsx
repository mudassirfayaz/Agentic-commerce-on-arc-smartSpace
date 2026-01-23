import { Link, useNavigate, useLocation } from 'react-router-dom'
import { 
  HiOutlineSquares2X2, 
  HiOutlineFolder, 
  HiOutlineCpuChip, 
  HiOutlineChartBar, 
  HiOutlineCreditCard,
  HiOutlineKey,
  HiOutlineArrowRightOnRectangle
} from 'react-icons/hi2'
import SmartSpaceIcon from '../SmartSpaceIcon'
import './Sidebar.css'

const Sidebar = ({ isCollapsed }) => {
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

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: HiOutlineSquares2X2 },
    { path: '/dashboard/projects', label: 'Projects', icon: HiOutlineFolder },
    { path: '/dashboard/agents', label: 'Agents', icon: HiOutlineCpuChip },
    { path: '/dashboard/usage', label: 'Usage', icon: HiOutlineChartBar },
    { path: '/dashboard/billing', label: 'Billing', icon: HiOutlineCreditCard },
    { path: '/dashboard/api-keys', label: 'API Keys', icon: HiOutlineKey },
  ]

  return (
    <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`} aria-expanded={!isCollapsed}>
      <div className="sidebar-header">
        {!isCollapsed && (
          <Link to="/dashboard" className="sidebar-logo">
            <SmartSpaceIcon size={20} className="sidebar-logo-icon" />
            <span>SmartSpace</span>
          </Link>
        )}
        {isCollapsed && (
          <Link to="/dashboard" className="sidebar-logo-icon-only">
            <SmartSpaceIcon size={24} />
          </Link>
        )}
      </div>
      <nav className="sidebar-nav">
        {navItems.map(({ path, label, icon: Icon }) => {
          const active = isActive(path)
          return (
            <Link 
              key={path}
              to={path} 
              className={`nav-item ${active ? 'active' : ''}`}
              aria-label={label}
            >
              <span className="nav-icon">
                <Icon />
              </span>
              {!isCollapsed && <span className="nav-text">{label}</span>}
            </Link>
          )
        })}
      </nav>
      <div className="sidebar-footer">
        <button 
          onClick={handleLogout} 
          className="btn btn-outline btn-block"
          aria-label="Logout"
        >
          {!isCollapsed && <span>Logout</span>}
          {isCollapsed && <HiOutlineArrowRightOnRectangle />}
        </button>
      </div>
    </aside>
  )
}

export default Sidebar

