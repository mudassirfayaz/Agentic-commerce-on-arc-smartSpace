import './StatsCards.css'

const StatsCards = () => {
  const stats = [
    { icon: '📊', value: '0', label: 'Total Requests' },
    { icon: '💰', value: '$0.00', label: 'Total Spent' },
    { icon: '🤖', value: '0', label: 'Active Agents' },
    { icon: '📁', value: '0', label: 'Projects' },
  ]

  return (
    <div className="stats-grid">
      {stats.map((stat, index) => (
        <div key={index} className="stat-card">
          <div className="stat-icon">{stat.icon}</div>
          <div className="stat-content">
            <div className="stat-value">{stat.value}</div>
            <div className="stat-label">{stat.label}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default StatsCards

