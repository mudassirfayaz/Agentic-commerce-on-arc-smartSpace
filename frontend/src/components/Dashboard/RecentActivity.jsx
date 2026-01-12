import './RecentActivity.css'

const RecentActivity = () => {
  return (
    <div className="activity-card">
      <table className="activity-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>API Provider</th>
            <th>Request</th>
            <th>Cost (USDC)</th>
            <th>Status</th>
            <th>Transaction Hash</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan="6">
              <div className="activity-empty">
                <div className="empty-icon">📋</div>
                <p>No activity yet</p>
                <p className="empty-subtitle">
                  Start making API calls to see your usage and transaction logs here
                </p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

export default RecentActivity

