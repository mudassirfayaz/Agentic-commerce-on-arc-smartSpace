import { useLocation } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import './DashboardLayout.css'

const DashboardLayout = ({ children, title }) => {
  const location = useLocation()
  const pageTitle = title || location.pathname.split('/').pop() || 'Dashboard'

  return (
    <div className="dashboard">
      <Sidebar />
      <div className="dashboard-content">
        <Header title={pageTitle.charAt(0).toUpperCase() + pageTitle.slice(1)} />
        <main className="dashboard-main">
          <div className="dashboard-container">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout

