import './ApiCallInterface.css'

const ApiCallInterface = () => {
  return (
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
      <div className="api-note">
        Estimated cost will be calculated before execution
      </div>
    </div>
  )
}

export default ApiCallInterface

