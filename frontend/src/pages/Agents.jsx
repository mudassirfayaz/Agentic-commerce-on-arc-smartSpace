import DashboardLayout from '../components/Dashboard/DashboardLayout'
import './Agents.css'

const Agents = () => {
  const agents = []

  return (
    <DashboardLayout title="Agents">
      <div className="agents-page">
        <div className="page-header">
          <div>
            <h1>Agents</h1>
            <p className="page-subtitle">Configure AI agents with autonomous API access</p>
          </div>
          <button className="btn btn-primary">Add Agent</button>
        </div>

        {agents.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🤖</div>
            <h2>No agents configured</h2>
            <p>Add your first agent to enable autonomous API access with spending limits</p>
            <button className="btn btn-primary">Add Agent</button>
          </div>
        ) : (
          <div className="agents-grid">
            {agents.map((agent) => (
              <div key={agent.id} className="agent-card">
                <div className="agent-header">
                  <div className="agent-icon">🤖</div>
                  <div>
                    <h3>{agent.name}</h3>
                    <span className="agent-status">{agent.status}</span>
                  </div>
                </div>
                <p className="agent-description">{agent.description}</p>
                <div className="agent-stats">
                  <div className="agent-stat">
                    <span className="stat-label">Spending Limit</span>
                    <span className="stat-value">{agent.limit}</span>
                  </div>
                  <div className="agent-stat">
                    <span className="stat-label">Spent</span>
                    <span className="stat-value">{agent.spent}</span>
                  </div>
                  <div className="agent-stat">
                    <span className="stat-label">Requests</span>
                    <span className="stat-value">{agent.requests}</span>
                  </div>
                </div>
                <div className="agent-actions">
                  <button className="btn btn-outline">Configure</button>
                  <button className="btn btn-primary">Manage</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}

export default Agents

