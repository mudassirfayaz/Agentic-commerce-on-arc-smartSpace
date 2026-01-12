import Sidebar from '../components/Dashboard/Sidebar'
import Header from '../components/Dashboard/Header'
import WelcomeSection from '../components/Dashboard/WelcomeSection'
import StatsCards from '../components/Dashboard/StatsCards'
import QuickActions from '../components/Dashboard/QuickActions'
import RecentActivity from '../components/Dashboard/RecentActivity'
import UsageAnalytics from '../components/Dashboard/UsageAnalytics'
import ApiCallInterface from '../components/Dashboard/ApiCallInterface'
import GettingStarted from '../components/Dashboard/GettingStarted'
import './Dashboard.css'

const Dashboard = () => {
  return (
    <div className="dashboard">
      <Sidebar />
      <div className="dashboard-content">
        <Header />
        <main className="dashboard-main">
          <div className="dashboard-container">
            <WelcomeSection />

            <section className="dashboard-section">
              <StatsCards />
            </section>

            <section className="dashboard-section">
              <h2>Quick Actions</h2>
              <QuickActions />
            </section>

            <section className="dashboard-section">
              <h2>Recent Activity</h2>
              <RecentActivity />
            </section>

            <section className="dashboard-section">
              <h2>Usage Analytics</h2>
              <UsageAnalytics />
            </section>

            <section className="dashboard-section">
              <h2>Make API Call</h2>
              <ApiCallInterface />
            </section>

            <section className="dashboard-section">
              <GettingStarted />
            </section>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Dashboard
