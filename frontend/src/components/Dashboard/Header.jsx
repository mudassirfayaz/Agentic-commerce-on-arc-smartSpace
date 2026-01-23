import { useLocation } from 'react-router-dom'
import { HiOutlineBars3 } from 'react-icons/hi2'
import './Header.css'

const Header = ({ isCollapsed, onToggle }) => {
  const location = useLocation()

  // Map routes to page titles
  const getPageTitle = () => {
    const routeMap = {
      '/dashboard': 'Dashboard',
      '/dashboard/projects': 'Projects',
      '/dashboard/agents': 'Agents',
      '/dashboard/usage': 'Usage',
      '/dashboard/billing': 'Billing',
      '/dashboard/api-keys': 'API Keys'
    }
    return routeMap[location.pathname] || 'Dashboard'
  }

  return (
    <header className="dashboard-header">
      <div className="header-content">
        <div className="header-left">
          <button 
            className="header-toggle"
            onClick={onToggle}
            aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            aria-expanded={!isCollapsed}
          >
            <HiOutlineBars3 />
          </button>
          <div className="header-page-title">
            <h1>{getPageTitle()}</h1>
          </div>
        </div>
        <div className="header-actions">
          <div className="wallet-balance">
            <span className="balance-label">USDC Balance</span>
            <span className="balance-amount">$0.00</span>
          </div>
          <button className="btn btn-primary btn-sm">Fund Wallet</button>
        </div>
      </div>
    </header>
  )
}

export default Header

