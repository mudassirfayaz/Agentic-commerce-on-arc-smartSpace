import DashboardLayout from '../components/Dashboard/DashboardLayout'
import './Usage.css'

const Usage = () => {
  return (
    <DashboardLayout>
      <div className="usage-page">
        <div className="usage-stats">
          <div className="usage-stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <div className="stat-value">0</div>
              <div className="stat-label">Total Requests</div>
            </div>
          </div>
          <div className="usage-stat-card">
            <div className="stat-icon">💰</div>
            <div className="stat-content">
              <div className="stat-value">$0.00</div>
              <div className="stat-label">Total Spent</div>
            </div>
          </div>
          <div className="usage-stat-card">
            <div className="stat-icon">⚡</div>
            <div className="stat-content">
              <div className="stat-value">0</div>
              <div className="stat-label">This Month</div>
            </div>
          </div>
        </div>

        <div className="usage-content">
          <div className="usage-chart">
            <h2>Usage Over Time</h2>
            <div className="chart-placeholder">
              <div className="chart-icon">📊</div>
              <p>Usage charts will appear here</p>
            </div>
          </div>

          <div className="usage-table-section">
            <h2>Recent Activity</h2>
            <div className="usage-table-card">
              <table className="usage-table">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>API Provider</th>
                    <th>Request</th>
                    <th>Cost (USDC)</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td colSpan="5">
                      <div className="empty-table">
                        <div className="empty-icon">📋</div>
                        <p>No activity yet</p>
                        <p className="empty-subtitle">Start making API calls to see your usage logs</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

export default Usage

