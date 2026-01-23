import { useState, useEffect } from 'react'
import Sidebar from './Sidebar'
import Header from './Header'
import './DashboardLayout.css'

const DashboardLayout = ({ children }) => {
  // Initialize collapsed state from localStorage (default: expanded)
  const [isCollapsed, setIsCollapsed] = useState(() => {
    const saved = localStorage.getItem('sidebarCollapsed')
    return saved ? JSON.parse(saved) : false
  })

  // Persist state to localStorage
  useEffect(() => {
    localStorage.setItem('sidebarCollapsed', JSON.stringify(isCollapsed))
  }, [isCollapsed])

  const handleToggle = () => {
    setIsCollapsed(!isCollapsed)
  }

  return (
    <div className="dashboard">
      <Sidebar isCollapsed={isCollapsed} />
      <div className={`dashboard-content ${isCollapsed ? 'sidebar-collapsed' : ''}`}>
        <Header isCollapsed={isCollapsed} onToggle={handleToggle} />
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

