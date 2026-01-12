import DashboardLayout from '../components/Dashboard/DashboardLayout'
import './Billing.css'

const Billing = () => {
  return (
    <DashboardLayout title="Billing">
      <div className="billing-page">
        <div className="page-header">
          <div>
            <h1>Billing</h1>
            <p className="page-subtitle">Manage your wallet, view invoices, and payment history</p>
          </div>
          <button className="btn btn-primary">Fund Wallet</button>
        </div>

        <div className="billing-overview">
          <div className="wallet-card">
            <div className="wallet-header">
              <h2>Wallet Balance</h2>
              <span className="wallet-label">USDC</span>
            </div>
            <div className="wallet-balance-amount">$0.00</div>
            <div className="wallet-actions">
              <button className="btn btn-primary btn-block">Add Funds</button>
              <button className="btn btn-outline btn-block">Withdraw</button>
            </div>
          </div>

          <div className="billing-stats">
            <div className="billing-stat">
              <div className="stat-label">Total Spent</div>
              <div className="stat-value">$0.00</div>
            </div>
            <div className="billing-stat">
              <div className="stat-label">This Month</div>
              <div className="stat-value">$0.00</div>
            </div>
            <div className="billing-stat">
              <div className="stat-label">Transactions</div>
              <div className="stat-value">0</div>
            </div>
          </div>
        </div>

        <div className="billing-sections">
          <div className="billing-section">
            <h2>Payment History</h2>
            <div className="billing-table-card">
              <table className="billing-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Transaction Hash</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td colSpan="5">
                      <div className="empty-table">
                        <div className="empty-icon">💳</div>
                        <p>No transactions yet</p>
                        <p className="empty-subtitle">Your payment history will appear here</p>
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

export default Billing

