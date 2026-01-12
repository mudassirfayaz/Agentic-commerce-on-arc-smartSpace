import './GettingStarted.css'

const GettingStarted = () => {
  const steps = [
    {
      number: 1,
      title: 'Fund Your Wallet',
      description: 'Add USDC to your SmartSpace wallet to start making API calls',
    },
    {
      number: 2,
      title: 'Create a Project',
      description: 'Set up a project with budget controls and spending policies',
    },
    {
      number: 3,
      title: 'Make Your First API Call',
      description: 'Test the API gateway with a simple request. Payment happens automatically.',
    },
    {
      number: 4,
      title: 'Configure Agents',
      description: 'Set up autonomous agents with spending limits and API access',
    },
  ]

  return (
    <div className="getting-started">
      <h2>Getting Started</h2>
      <div className="steps-list">
        {steps.map((step) => (
          <div key={step.number} className="step-item">
            <div className="step-number">{step.number}</div>
            <div className="step-content">
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default GettingStarted

