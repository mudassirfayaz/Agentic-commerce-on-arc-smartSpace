import { Link, useNavigate } from 'react-router-dom'
import './Dashboard.css'
// 1. Add the import at the top
import GenChatboxAiDash from './GenChatboxAiDash'

const Dashboard = () => {
  const navigate = useNavigate()

  const handleLogout = () => {
    // TODO: Implement logout logic
    navigate('/')
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="dashboard-header-content">
          <div className="dashboard-logo">SmartSpace</div>
          <nav className="dashboard-nav">
            <Link to="/dashboard" className="nav-item active">Dashboard</Link>
            <Link to="/dashboard/projects" className="nav-item">Projects</Link>
            <Link to="/dashboard/agents" className="nav-item">Agents</Link>
            <Link to="/dashboard/usage" className="nav-item">Usage</Link>
            <Link to="/dashboard/billing" className="nav-item">Billing</Link>
          </nav>
          <div className="dashboard-actions">
            <div className="wallet-balance">
              <span className="balance-label">USDC Balance</span>
              <span className="balance-amount">$0.00</span>
            </div>
            <button className="btn btn-primary btn-sm">Fund Wallet</button>
            <button onClick={handleLogout} className="btn btn-outline btn-sm">Logout</button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="dashboard-container">
          {/* Welcome Section */}
          <section className="dashboard-section">
            <h1>Welcome to SmartSpace</h1>
            <p className="dashboard-subtitle">
              Start building with pay-per-use API access powered by USDC
            </p>
          </section>

          {/* Stats Grid */}
          <section className="dashboard-section">
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">📊</div>
                <div className="stat-content">
                  <div className="stat-value">0</div>
                  <div className="stat-label">Total Requests</div>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">💰</div>
                <div className="stat-content">
                  <div className="stat-value">$0.00</div>
                  <div className="stat-label">Total Spent</div>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">🤖</div>
                <div className="stat-content">
                  <div className="stat-value">0</div>
                  <div className="stat-label">Active Agents</div>
                </div>
              </div>
              <div className="stat-card">
                <div className="stat-icon">📁</div>
                <div className="stat-content">
                  <div className="stat-value">0</div>
                  <div className="stat-label">Projects</div>
                </div>
              </div>
            </div>
          </section>

          {/* Quick Actions */}
          <section className="dashboard-section">
            <h2>Quick Actions</h2>
            <div className="actions-grid">
              <div className="action-card">
                <div className="action-icon">➕</div>
                <h3>Create Project</h3>
                <p>Set up a new project with budget controls and spending rules</p>
                <button className="btn btn-primary btn-block">Create Project</button>
              </div>
              <div className="action-card">
                <div className="action-icon">🤖</div>
                <h3>Add Agent</h3>
                <p>Configure an AI agent with autonomous API access</p>
                <button className="btn btn-primary btn-block">Add Agent</button>
              </div>
              <div className="action-card">
                <div className="action-icon">🔌</div>
                <h3>Make API Call</h3>
                <p>Test an API request and see instant USDC payment</p>
                <button className="btn btn-primary btn-block">Try API Call</button>
              </div>
              <div className="action-card">
                <div className="action-icon">💰</div>
                <h3>Fund Wallet</h3>
                <p>Add USDC to your wallet for API payments</p>
                <button className="btn btn-primary btn-block">Fund Wallet</button>
              </div>
            </div>
          </section>

          {/* Recent Activity */}
          <section className="dashboard-section">
            <h2>Recent Activity</h2>
            <div className="activity-card">
              <table className="transaction-table">
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
                        <p className="empty-subtitle">Start making API calls to see your usage and transaction logs here</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          {/* Usage Chart */}
          <section className="dashboard-section">
            <h2>Usage Analytics</h2>
            <div className="chart-container">
              <div className="chart-placeholder">
                <div className="chart-placeholder-icon">📊</div>
                <p>Usage charts will appear here</p>
                <p className="empty-subtitle">Visualize your API usage, costs, and trends over time</p>
              </div>
            </div>
          </section>

          {/* API Call Interface */}
          <section className="dashboard-section">
            <h2>Make API Call</h2>
            <div className="api-call-interface">
              <h3>Test API Request</h3>
              <div className="api-form-group">
                <label htmlFor="api-provider">API Provider</label>
                <select id="api-provider">
                  <option>Select provider...</option>
                  <option>OpenAI GPT-4</option>
                  <option>OpenAI GPT-3.5</option>
                  <option>Anthropic Claude</option>
                  <option>Google Gemini</option>
                  <option>Anthropic Claude Sonnet</option>
                </select>
              </div>
              <div className="api-form-group">
                <label htmlFor="api-prompt">Prompt / Request</label>
                <textarea
                  id="api-prompt"
                  placeholder="Enter your API request here..."
                ></textarea>
              </div>
              <div className="api-form-group">
                <label htmlFor="max-tokens">Max Tokens (optional)</label>
                <input
                  type="number"
                  id="max-tokens"
                  placeholder="1000"
                  min="1"
                  max="8000"
                />
              </div>
              <button className="btn btn-primary btn-block">
                Execute Request (Pay with USDC)
              </button>
              <div style={{ marginTop: '16px', fontSize: '13px', color: 'var(--text-light)', textAlign: 'center' }}>
                Estimated cost will be calculated before execution
              </div>
            </div>
          </section>

          {/* Getting Started */}
          <section className="dashboard-section">
            <div className="getting-started">
              <h2>Getting Started</h2>
              <div className="steps-list">
                <div className="step-item">
                  <div className="step-number">1</div>
                  <div className="step-content">
                    <h3>Fund Your Wallet</h3>
                    <p>Add USDC to your SmartSpace wallet to start making API calls</p>
                  </div>
                </div>
                <div className="step-item">
                  <div className="step-number">2</div>
                  <div className="step-content">
                    <h3>Create a Project</h3>
                    <p>Set up a project with budget controls and spending policies</p>
                  </div>
                </div>
                <div className="step-item">
                  <div className="step-number">3</div>
                  <div className="step-content">
                    <h3>Make Your First API Call</h3>
                    <p>Test the API gateway with a simple request. Payment happens automatically.</p>
                  </div>
                </div>
                <div className="step-item">
                  <div className="step-number">4</div>
                  <div className="step-content">
                    <h3>Configure Agents</h3>
                    <p>Set up autonomous agents with spending limits and API access</p>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* 2. Add the Chatbox here (it will stay fixed to bottom right) */}
      <GenChatboxAiDash />
    </div>
  )
}

export default Dashboard

