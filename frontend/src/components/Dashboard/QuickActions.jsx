import './QuickActions.css'

const QuickActions = () => {
  const actions = [
    {
      icon: '➕',
      title: 'Create Project',
      description: 'Set up a new project with budget controls and spending rules',
      buttonText: 'Create Project',
    },
    {
      icon: '🤖',
      title: 'Add Agent',
      description: 'Configure an AI agent with autonomous API access',
      buttonText: 'Add Agent',
    },
    {
      icon: '🔌',
      title: 'Make API Call',
      description: 'Test an API request and see instant USDC payment',
      buttonText: 'Try API Call',
    },
    {
      icon: '💰',
      title: 'Fund Wallet',
      description: 'Add USDC to your wallet for API payments',
      buttonText: 'Fund Wallet',
    },
  ]

  return (
    <div className="actions-grid">
      {actions.map((action, index) => (
        <div key={index} className="action-card">
          <div className="action-icon">{action.icon}</div>
          <h3>{action.title}</h3>
          <p>{action.description}</p>
          <button className="btn btn-primary btn-block">{action.buttonText}</button>
        </div>
      ))}
    </div>
  )
}

export default QuickActions

